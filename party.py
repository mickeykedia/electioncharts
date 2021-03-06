"""methods pertaining to parties"""

# Import the Flask Framework

import json
import cgi
import party_scripts


def get_landing(db,dummy):
	cursor = db.cursor()
	cursor.execute("select count(constituency_id),p.coalition_id,status from latest_results lr inner join party p on lr.party_id = p.id group by status,p.coalition_id;");
	result = {}
	congress = {"wins":0,"leads":0,"swing":0,"vote_percentage":0}
	bjp = {"wins":0,"leads":0,"swing":0,"vote_percentage":0}
	others = {"wins":0,"leads":0,"swing":0,"vote_percentage":0}
	aap = {"wins":0,"leads":0,"swing":0,"vote_percentage":0}
	for row in cursor.fetchall():
		"""
		coalition id 1 = congress

		"""
		if(row[1]==1):
			if(row[2]=='DECLARED'):
				congress['wins'] = congress['wins']+row[0]
			elif(row[2]=='COUNTING'):
				congress['leads'] = congress['leads']+row[0]
		elif(row[1]==2):
			if(row[2]=='DECLARED'):
				bjp['wins'] = bjp['wins']+row[0]
			elif(row[2]=='COUNTING'):
				bjp['leads'] =bjp['leads']+row[0]
		elif(row[1]==3):
			if(row[2]=='DECLARED'):
				others['wins'] = others['wins']+row[0]
			elif(row[2]=='COUNTING'):
				others['leads'] =others['leads']+row[0]
		elif(row[1]==4):
			if(row[2]=='DECLARED'):
				aap['wins'] = aap['wins']+row[0]
			elif(row[2]=='COUNTING'):
				aap['leads'] =aap['leads']+row[0]
		else :
			pass

	cursor.execute("""select sum(votes),coalition_id
							from results r
							inner join candidate_constituency cc
							on
								cc.candidate_id = r.candidate_id
								and
								cc.constituency_id = r.constituency_id
							inner join party p
							on
								p.id = cc.party_id
							where r.active = 1
							and cc.election = '2014'
							group by coalition_id;""");
	votecount = 0;
	rows = cursor.fetchall()
	for row in rows:
		votecount = votecount+row[0]
	for row in rows :
		if(row[1]==1):
			congress['vote_percentage'] = round((row[0]/votecount)*100,2)
		elif(row[1]==2):
			bjp['vote_percentage'] = round((row[0]/votecount)*100,2)
		elif(row[1]==3):
			others['vote_percentage'] = round((row[0]/votecount)*100,2)
		elif(row[1]==4):
			aap['vote_percentage'] = round((row[0]/votecount)*100,2)
		else:
			pass


	cursor.execute("""select count(lr.constituency_id),wp.coalition_id,ltp.coalition_id
					from last_time_winners ltw
					inner join latest_results lr on lr.constituency_id = ltw.constituency_id and lr.party_id!=ltw.party_id
					inner join party wp on lr.party_id = wp.id
					inner join party ltp on ltw.party_id = ltp.id
					group by wp.coalition_id,ltp.coalition_id
					""");
	swings = [0,0,0,0,0]
	for row in cursor.fetchall():
		swings[row[1]] = swings[row[1]]+row[0];
		swings[row[2]] = swings[row[2]]-row[0];

	congress['swing'] =swings[1]
	bjp['swing']=swings[2]
	others['swing']=swings[3]
	aap['swing']=swings[4]


	cursor.execute("select * from top_contests");
	close_contests = []
	for row in cursor.fetchall():
		cc={}
		cc['comments']=row[2]
		cc['url']=row[0]
		cc['name']=row[1]
		close_contests.append(cc)

	cursor.close()

	result = {"congress":congress,"bjp":bjp,"others":others,"aap":aap,"close_contests":close_contests}
	return json.dumps(result);


def get_party_result(db, party_id ):
	cursor = db.cursor()
	cursor.execute("""select count(constituency_id),status from latest_results lr
					where lr.party_id =%s
					group by status"""% (party_id))
	wins =0
	leads = 0
	for row in cursor.fetchall():
		if row[1]=="DECLARED":
			wins=row[0]
		elif row[1]=="COUNTING":
			leads=row[0]

	cursor.execute("""select count(lr.constituency_id),lr.party_id,ltw.party_id
					from last_time_winners ltw
					inner join latest_results lr on lr.constituency_id = ltw.constituency_id and lr.party_id!=ltw.party_id
					where lr.party_id = %s or ltw.party_id = %s
					group by lr.party_id,ltw.party_id"""% (party_id,party_id))

	swing = 0
	for row in cursor.fetchall():
		if row[1]==int(party_id):
			swing=swing+row[0]
		elif row[2]==int(party_id):
			swing=swing-row[0]

	vote_share = get_party_vote_percentage(db, party_id)

	cursor.close()

	party_result = dict([('wins', wins),
	                     ("leads", leads),
	                     ("swing", swing),
	                     ("update_time", get_latest_time(db)),
	                     ("vote_percentage", vote_share)])

	return json.dumps(party_result)

def get_latest_time(db):
	latest_time_cursor = db.cursor()
	latest_time_cursor.execute("select max(time_start) from results rs where active = 1 ")
	time = latest_time_cursor.fetchone()
	if time is not None:
		time = str(time[0])
	else:
		time = "No data yet"
	latest_time_cursor.close()
	return time;


def get_coalition_parties(db, coalition_id):
	cursor = db.cursor()
	cursor.execute("Select id,name,symbol,shortform from party where coalition_id = %s", coalition_id)
	results = []
	for row in cursor.fetchall():
		results.append({"party_id": row[0],
		                "symbol": row[2],
		                "name": row[1],
		                "shortform": row[3]
		})
	cursor.close()
	return json.dumps(results)

def get_coalition_state_parties(db, coalition_id,state_id):
	cursor = db.cursor()
	cursor.execute("""SELECT distinct p.* FROM candidate_constituency cc
		inner join constituency c on c.id = cc.constituency_id
		inner join party p on p.id = cc.party_id
		where c.state_id = %s and p.coalition_id =%s and cc.election = '2014';
	               """, (state_id,coalition_id))
	results = []
	for row in cursor.fetchall():
		results.append({"party_id": row[0],
		                "symbol": row[2],
		                "name": row[1],
		                "shortform": row[3]
		})
	cursor.close()
	return json.dumps(results)



def get_coalition_result(db, coalition_id):
	parties = json.loads(get_coalition_parties(db, coalition_id))

	wins = 0
	leads = 0
	swing = 0
	vote_percentage = 0
	results = []
	for party in parties:
		basic_result = json.loads(get_party_result(db, party['party_id']))
		results.append({"party_id":party['party_id'],
		                "party_name":party['name'],
		                "wins":basic_result['wins'],
						"leads":basic_result['leads'],
						"update_time":basic_result['update_time'],
		                "total_ahead":(basic_result['wins']+basic_result['leads']),
						"swing":basic_result['swing'],
						"vote_percentage":basic_result['vote_percentage']
						})
	return json.dumps(results)

def get_coalition_state_result(db, coalition_id,state_id):
	parties = json.loads(get_coalition_state_parties(db, coalition_id,state_id))

	wins = 0
	leads = 0
	swing = 0
	vote_percentage = 0
	results = []
	for party in parties:
		basic_result = json.loads(get_party_result_by_state(db, party['party_id'],state_id))
		results.append({"party_id":party['party_id'],
		                "party_name":party['name'],
		                "wins":basic_result['wins'],
		                "leads":basic_result['leads'],
		                "update_time":basic_result['update_time'],
		                "total_ahead":(basic_result['wins']+basic_result['leads']),
		                "swing":basic_result['swing'],
		                "vote_percentage":basic_result['vote_percentage']
		})
	return json.dumps(results)




def get_party_statewise_result(db, party_id):
	"""
	Summary of results as
	state,wins,leads,swing,vote_percentage,total
	:param party_id: party id
	"""
	statelist = json.loads(get_constituency_count_for_states(db))
	results = []

	for sl in statelist:
		basic_summary = json.loads(get_party_result_by_state(db, int(party_id), sl['state_id']))
		if basic_summary['vote_percentage'] > 0:
			results.append({"state": sl['state_name'],
			                "state_id": sl['state_id'],
			                "wins": basic_summary['wins'],
			                "leads": basic_summary['leads'],
			                "total_ahead": (basic_summary['wins'] + basic_summary['leads']),
			                "swing": basic_summary['swing'],
			                "vote_percentage": basic_summary['vote_percentage'],
			                "total": sl['pc_count']})
		else:
			pass
	return json.dumps(results)

def get_coalition_statewise_result(db,coalition_id):
	parties = json.loads(get_coalition_parties(db, coalition_id))

	statelist = json.loads(get_constituency_count_for_states(db))
	results = []
	for sl in statelist:
		wins =0
		leads = 0
		swing =0
		vote_percentage = 0
		for party in parties:
			partystatewiseResults = json.loads(get_party_result_by_state(db,party['party_id'],sl['state_id']))
			wins =wins+ partystatewiseResults['wins']
			leads =leads+ partystatewiseResults['leads']
			swing = swing+partystatewiseResults['swing']
			vote_percentage=vote_percentage+float(partystatewiseResults['vote_percentage'])
		if vote_percentage > 0:
			results.append({"state": sl['state_name'],
							"state_id": sl['state_id'],
							"wins": wins,
							"leads": leads,
							"total_ahead": (wins+leads),
							"swing": swing,
							"vote_percentage": round(vote_percentage,2),
							"total": sl['pc_count']})
		else:
			pass

	return json.dumps(results)




def get_party_result_by_state(db, party_id, state_id):
	cursor = db.cursor()
	cursor.execute("""select count(constituency_id),status from latest_results lr
					inner join constituency c on c.id = lr.constituency_id
					and lr.party_id =%s
					and c.state_id=%s
					group by status"""% (party_id,state_id))
	wins =0
	leads = 0
	for row in cursor.fetchall():
		if row[1]=="DECLARED":
			wins=row[0]
		elif row[1]=="COUNTING":
			leads=row[0]

	cursor.execute("""select count(lr.constituency_id),lr.party_id,ltw.party_id
					from last_time_winners ltw
					inner join latest_results lr on lr.constituency_id = ltw.constituency_id and lr.party_id!=ltw.party_id
					inner join constituency c on c.id = lr.constituency_id
					where c.state_id = %s
					and (lr.party_id = %s or ltw.party_id = %s)
					group by lr.party_id,ltw.party_id"""% (state_id,party_id,party_id))

	swing = 0
	for row in cursor.fetchall():
		if row[1]==int(party_id):
			swing=swing+row[0]
		elif row[2]==int(party_id):
			swing=swing-row[0]

	vote_percentage = json.loads(get_vote_percentage_for_party_state(db, party_id, state_id))
	party_result = dict([('wins', wins),
	                     ("leads", leads),
	                     ("swing", swing),
	                     ("update_time", get_latest_time(db)),
	                     ("vote_percentage", vote_percentage)])
	cursor.close()

	return json.dumps(party_result)


def get_vote_percentage_for_party_state(db, party_id, state_id):
	cursor = db.cursor()
	cursor.execute("""select sum(r.votes),cc.party_id from results as r
        inner join constituency c on c.id = r.constituency_id
        inner join candidate_constituency cc
        on cc.candidate_id = r.candidate_id and cc.constituency_id = r.constituency_id
        where c.state_id = %s and r.active = 1 and cc.election = '2014' group by cc.party_id""" % (state_id))
	temp_result = cursor.fetchall()
	cursor.close()
	return aggregate_vote_share_for_query_result(temp_result, party_id)


def get_party_vote_percentage(db, party_id):
	cursor = db.cursor()
	cursor.execute("""select sum(r.votes),cc.party_id from results as r inner join
candidate_constituency cc on cc.candidate_id = r.candidate_id and cc.constituency_id = r.constituency_id
where r.active = 1 and cc.election = '2014' group by cc.party_id""")
	temp_result = cursor.fetchall();
	cursor.close()
	return aggregate_vote_share_for_query_result(temp_result, party_id)


def get_party_list(db, dummy):
	cursor = db.cursor()
	cursor.execute('SELECT id, name, shortform from party')
	partyList = []
	for row in cursor.fetchall():
		partyList.append(dict([('id', row[0]),
		                       ('name', cgi.escape(row[1])),
		                       ('shortform', row[2])]))
	cursor.close()
	return json.dumps(partyList)

def get_coalition(db,coalition_id):
	cursor = db.cursor()
	cursor.execute(
		"SELECT p.id, p.name, p.shortform,p.symbol from coalition p  where p.id = %s;",coalition_id)
	row = cursor.fetchone()
	coalition = dict([('id', row[0]),
	              ('name', cgi.escape(row[1])),
	              ('symbol', row[3]),
	              ('shortform', cgi.escape(row[2]))])
	cursor.close()
	return json.dumps(coalition)


def get_party(db, party_id):
	cursor = db.cursor()
	cursor.execute(
		'SELECT p.id, p.name, p.shortform,p.symbol,c.name as coalition,p.colour from party p inner join coalition c on c.id = p.coalition_id where p.id = ' + party_id + ';')
	row = cursor.fetchone()
	party = dict([('id', row[0]),
	              ('name', cgi.escape(row[1])),
	              ('symbol', row[3]),
	              ('coalition', cgi.escape(row[4])),
	              ('colour', row[5]),
	              ('shortform', cgi.escape(row[2]))])
	cursor.close()
	return json.dumps(party)


def get_constituency_count_for_states(db):
	"""
	:rtype : JSON object with array of {state_id:"value",state_name:"value",pc_count="value"}
	"""
	cursor = db.cursor()
	cursor.execute(
		'select count(c.id),s.name,s.id from constituency c inner join state s on s.id = c.state_id group by s.id order by count(c.id);');
	rsults = []
	for row in cursor.fetchall():
		rsults.append({"state_id": row[2], "state_name": row[1], "pc_count": row[0]})
	cursor.close()
	return json.dumps(rsults);



def get_party_state_detailed_result_undeclared(db, party_id, state_id):
	results = []
	cursor = db.cursor()
	cursor.execute(party_scripts.get_party_leads_sql_string_for_state(party_id, state_id))
	for row in cursor.fetchall():
		results.append({
		"candidate_id": row[0],
		"candidate_name": row[1],
		"constituency_name": row[3],
		"constituency_id": row[2],
		"votes": row[5],
		"lead": row[6],
		"loosing_candidate_name": row[8],
		"loosing_party_name": row[9],
		"status": "LEAD",
		"party_id":int(party_id),
		"last_time_party_id":row[11]
		})

	cursor.execute(party_scripts.get_party_trails_sql_string_for_state(party_id, state_id,"COUNTING"))

	for row in cursor.fetchall():
		results.append({
		"constituency_id": row[0],
		"constituency_name": row[1],
		"candidate_id": row[2],
		"candidate_name": row[3],
		"votes": row[5],
		"lead": row[4],
		"winning_party_name": row[6],
		"winning_candidate_name": row[8],
		"status": "TRAIL",
		"party_id":int(party_id),
		"last_time_party_id":row[10]
		})
	cursor.close()
	return json.dumps(results)


def get_party_state_detailed_result_declared(db, party_id, state_id):
	results = []
	cursor= db.cursor()
	cursor.execute(party_scripts.get_party_wins_sql_string_for_state(party_id,state_id))

	for row in cursor.fetchall():
		results.append({
		"candidate_id":row[0],
		"candidate_name":row[1],
		"constituency_name":row[3],
		"constituency_id":row[2],
		"votes":row[5],
		"lead":row[6],
		"loosing_candidate_name":row[8],
		"loosing_party_name":row[9],
		"status":"WIN",
		"party_id":int(party_id),
		"last_time_party_id":row[11]
		})

	cursor.execute(party_scripts.get_party_trails_sql_string_for_state(party_id, state_id,"DECLARED"))

	for row in cursor.fetchall():
		results.append({
		"constituency_id": row[0],
		"constituency_name": row[1],
		"candidate_id": row[2],
		"candidate_name": row[3],
		"votes": row[5],
		"lead": row[4],
		"winning_party_name": row[6],
		"winning_candidate_name": row[8],
		"status": "LOST",
		"party_id":int(party_id),
		"last_time_party_id":row[10]
		})

	return json.dumps(results)

def get_coalition_state_detailed_result_undeclared(db,coalition_id,state_id):
	results = []
	cursor = db.cursor()
	cursor.execute(party_scripts.get_coalition_leads_sql_string_for_state(coalition_id,state_id))

	for row in cursor.fetchall():
		results.append({
		"candidate_id": row[0],
		"candidate_name": row[1],
		"constituency_name": row[3],
		"constituency_id": row[2],
		"votes": row[5],
		"lead": row[6],
		"loosing_candidate_name": row[8],
		"loosing_party_name": row[9],
		"status": "LEAD",
		"party_name":row[11],
		"party_id":row[4],
		"last_time_party_id":row[12]
		})

	cursor.execute(party_scripts.get_coalition_trails_sql_string_for_state(coalition_id,state_id,"COUNTING"))

	for row in cursor.fetchall():
		results.append({
		"constituency_id": row[0],
		"constituency_name": row[1],
		"candidate_id": row[2],
		"candidate_name": row[3],
		"votes": row[5],
		"lead": row[4],
		"winning_party_name": row[6],
		"winning_candidate_name": row[8],
		"status": "TRAIL",
		"party_name":row[10],
		"party_id":row[11],
		"last_time_party_id":row[12]
		})

	cursor.close()
	return json.dumps(results)

def get_coalition_detailed_result_undeclared(db,coalition_id):
	results = []
	cursor = db.cursor()
	cursor.execute(party_scripts.get_coalition_leads_sql_string(coalition_id))

	for row in cursor.fetchall():
		results.append({
		"candidate_id": row[0],
		"candidate_name": row[1],
		"constituency_name": row[3],
		"constituency_id": row[2],
		"votes": row[5],
		"lead": row[6],
		"loosing_candidate_name": row[8],
		"loosing_party_name": row[9],
		"status": "LEAD",
		"party_name":row[11],
		"party_id":row[4],
		"last_time_party_id":row[12]
		})

	cursor.execute(party_scripts.get_coalition_trails_sql_string(coalition_id,"COUNTING"))

	for row in cursor.fetchall():
		results.append({
		"constituency_id": row[0],
		"constituency_name": row[1],
		"candidate_id": row[2],
		"candidate_name": row[3],
		"votes": row[5],
		"lead": row[4],
		"winning_party_name": row[6],
		"winning_candidate_name": row[8],
		"status": "TRAIL",
		"party_name":row[10],
		"party_id":row[11],
		"last_time_party_id":row[12]
		})
	cursor.close()

	return json.dumps(results)

def get_coalition_state_detailed_result_declared(db,coalition_id,state_id):
	results = []

	cursor= db.cursor()
	cursor.execute(party_scripts.get_coalition_wins_sql_string_for_state(coalition_id,state_id))

	for row in cursor.fetchall():
		results.append({
		"candidate_id":row[0],
		"candidate_name":row[1],
		"constituency_name":row[3],
		"constituency_id":row[2],
		"votes":row[5],
		"lead":row[6],
		"loosing_candidate_name":row[8],
		"loosing_party_name":row[9],
		"status":"WIN",
		"party_name":row[11],
		"party_id":row[4],
		"last_time_party_id":row[12]
		})

	cursor.execute(party_scripts.get_coalition_trails_sql_string_for_state(coalition_id,state_id,"DECLARED"))

	for row in cursor.fetchall():
		results.append({
		"constituency_id": row[0],
		"constituency_name": row[1],
		"candidate_id": row[2],
		"candidate_name": row[3],
		"votes": row[5],
		"lead": row[4],
		"winning_party_name": row[6],
		"winning_candidate_name": row[8],
		"status": "LOST",
		"party_name":row[10],
		"party_id":row[11],
		"last_time_party_id":row[12]
		})
	cursor.close()
	return json.dumps(results)

def get_coalition_detailed_result_declared(db,coalition_id):
	results = []

	cursor= db.cursor()
	cursor.execute(party_scripts.get_coalition_wins_sql_string(coalition_id))

	for row in cursor.fetchall():
		results.append({
		"candidate_id":row[0],
		"candidate_name":row[1],
		"constituency_name":row[3],
		"constituency_id":row[2],
		"votes":row[5],
		"lead":row[6],
		"loosing_candidate_name":row[8],
		"loosing_party_name":row[9],
		"status":"WIN",
		"party_name":row[11],
		"party_id":row[4],
		"last_time_party_id":row[12]
		})

	cursor.execute(party_scripts.get_coalition_trails_sql_string(coalition_id,"DECLARED"))

	for row in cursor.fetchall():
		results.append({
		"constituency_id": row[0],
		"constituency_name": row[1],
		"candidate_id": row[2],
		"candidate_name": row[3],
		"votes": row[5],
		"lead": row[4],
		"winning_party_name": row[6],
		"winning_candidate_name": row[8],
		"status": "LOST",
		"party_name":row[10],
		"party_id":row[11],
		"last_time_party_id":row[12]
		})
	cursor.close()
	return json.dumps(results)

def get_coalition_detailed_result_declared_1(db,coalition_id):
	results = []

	cursor= db.cursor()
	cursor.execute(party_scripts.get_coalition_wins_sql_string(coalition_id))

	for row in cursor.fetchall():
		results.append({
		"candidate_id":row[0],
		"candidate_name":row[1],
		"constituency_name":row[3],
		"constituency_id":row[2],
		"votes":row[5],
		"lead":row[6],
		"loosing_candidate_name":row[8],
		"loosing_party_name":row[9],
		"status":"WIN",
		"party_name":row[11],
		"party_id":row[4],
		"last_time_party_id":row[12]
		})

	cursor.execute(party_scripts.get_coalition_trails_sql_string(coalition_id,"DECLARED"))

	for row in cursor.fetchall():
		results.append({
		"constituency_id": row[0],
		"constituency_name": row[1],
		"candidate_id": row[2],
		"candidate_name": row[3],
		"votes": row[5],
		"lead": row[4],
		"winning_party_name": row[6],
		"winning_candidate_name": row[8],
		"status": "LOST",
		"party_name":row[10],
		"party_id":row[11],
		"last_time_party_id":row[12]
		})
	cursor.close()
	return json.dumps(results)


def get_party_detailed_result_declared(db, party_id):
	results = []

	cursor= db.cursor()
	cursor.execute(party_scripts.get_party_wins_sql_string(party_id))

	for row in cursor.fetchall():
		results.append({
		"candidate_id":row[0],
		"candidate_name":row[1],
		"constituency_name":row[3],
		"constituency_id":row[2],
		"votes":row[5],
		"lead":row[6],
		"loosing_candidate_name":row[8],
		"loosing_party_name":row[9],
		"status":"WIN",
		"party_id":int(party_id),
		"last_time_party_id":row[11]
		})


	cursor.execute(party_scripts.get_party_trails_sql_string(party_id,"DECLARED"))

	for row in cursor.fetchall():
		results.append({
		"constituency_id": row[0],
		"constituency_name": row[1],
		"candidate_id": row[2],
		"candidate_name": row[3],
		"votes": row[5],
		"lead": row[4],
		"winning_party_name": row[6],
		"winning_candidate_name": row[8],
		"status": "LOST",
		"party_id":int(party_id),
		"last_time_party_id":row[10]
		})
	cursor.close()

	return json.dumps(results)

def get_party_detailed_result_undeclared(db, party_id):
	results = []

	cursor = db.cursor()
	cursor.execute(party_scripts.get_party_leads_sql_string(party_id))

	for row in cursor.fetchall():
		results.append({
			"candidate_id": row[0],
			"candidate_name": row[1],
			"constituency_name": row[3],
			"constituency_id": row[2],
			"votes": row[5],
			"lead": row[6],
			"loosing_candidate_name": row[8],
			"loosing_party_name": row[9],
			"status": "LEAD",
			"party_id":int(party_id),
			"last_time_party_id":row[11]
		})

	cursor.execute(party_scripts.get_party_trails_sql_string(party_id,"COUNTING"))

	for row in cursor.fetchall():
		results.append({
			"constituency_id": row[0],
			"constituency_name": row[1],
			"candidate_id": row[2],
			"candidate_name": row[3],
			"votes": row[5],
			"lead": row[4],
			"winning_party_name": row[6],
			"winning_candidate_name": row[8],
			"status": "TRAIL",
			"party_id":int(party_id),
			"last_time_party_id":row[10]
		})
	cursor.close()

	return json.dumps(results)


def aggregate_party_result_from_query_result(rows, party_id):
	"""

    Takes the results for a region and calculates wincount, leadcount and swing for that region.
    :param rows:
    :param party_id:
    :return:
    """
	wincount = 0
	leadcount = 0
	swingcount = 0

	for row in rows:

		if row[1] == 0:
			if row[3] == 'DECLARED':
				wincount = wincount + 1
			elif row[3]=='COUNTING':
				leadcount = leadcount + 1

			# if the party is winning/leading now, but hasn't won the last time - then the swing count will get added by one.
			if row[5] != long(party_id):
				swingcount = swingcount + 1
			else:
				pass
		else:
			# if the party isn't leading/winning now - and won the last time, then swing count will reduce by 1
			if row[5] == long(party_id):
				swingcount -= 1
			else:
				pass
	result = []
	result.append({'wins': wincount, 'leads': leadcount, 'swing': swingcount})
	return json.dumps(result)


def aggregate_vote_share_for_query_result(rows, party_id):
	"""

        Totals the votes received for the extent of the query and
        gives the voting percentage for a particular party.
    :param rows:
    :param party_id:
    :return:
    """
	totalvotes = 0
	party_vote = 0
	for row in rows:
		totalvotes = totalvotes + row[0]
		if row[1] == long(party_id):
			party_vote = row[0]
		else:
			pass
	if totalvotes != 0:
		vote_share = (party_vote / totalvotes) * 100
		return str(round(vote_share, 2))
	else:
		return '0'
