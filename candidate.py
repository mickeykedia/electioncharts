"""methods pertaining to candidates"""

# Import the Flask Framework

import json
import cgi


def get_candidate_list(db,param):
    cursor = db.cursor()
    cursor.execute('''SELECT ca.id, ca.fullname, co.id, co.name, p.id, p.name 
        from candidate ca, candidate_constituency c_c, constituency co, party p 
        where ca.id=c_c.candidate_id and c_c.constituency_id=co.id and c_c.party_id=p.id ''')
    output=[]
    for row in cursor.fetchall():
        temp={}
        temp['candidate_id']=row[0]
        temp['candidate_name']=cgi.escape(row[1])
        temp['constituency_id']=row[2]
        temp['constituency_name']=cgi.escape(row[3])
        temp['party_id']=row[4]
        temp['party_name']=cgi.escape(row[5])
        output.append(temp)
    
    return json.dumps(output);



def get_candidate_info(db, candidate_id):
    cursor = db.cursor()
    cursor.execute('''SELECT c.id, c.fullname, c.age, p.id, p.name, p.symbol
            FROM candidate c, candidate_constituency c_c, party p
            WHERE c.id = c_c.candidate_id
            AND c_c.party_id = p.id
            AND c.id=''' + candidate_id + ''';''')
    row = cursor.fetchone()
    candidate = {"id": row[0], "name": cgi.escape(row[1]), "age": row[2], "party_id":row[3],"party_name":row[4],"party_symbol":row[5]}
    return json.dumps(candidate)


def get_candidate_result(db,candidate_id):
    cursor = db.cursor()
        
    """ Curate the results """
    vote_counts={}
    result_status={}
    leader = {}
    candidate_name=""
    leader_count= {}
    constituency_ids={}
    cursor.execute('''select r.constituency_id,co.name constituency_name,c.fullname candidate_name, 
        r.candidate_id, c_c.party_id,r.votes, r.time_start, 
        p.name, p.symbol, co.result_status 
        from results r,candidate c, constituency co, party p, candidate_constituency c_c 
        where p.id=c_c.party_id and r.active =1 and c.id=r.candidate_id and c.id=c_c.candidate_id
        and  r.constituency_id=co.id and co.id=c_c.constituency_id and r.constituency_id in 
        (select constituency_id from candidate_constituency 
        where candidate_id ='''+ candidate_id +''');''')
    """
    check if cc.election = '2014' also - explicitly check 'DECLARED' and 'COUNTING' - factor in - 'NOT_STARTED' as a possible option.
    """
    for row in cursor.fetchall():
        const_name = row[1];
        if not const_name in vote_counts:
            vote_counts[const_name] = {"Others":0}
            result_status[const_name] = 'DECLARED'
            leader[const_name] = [cgi.escape(row[2]),row[3],row[4],row[7]]
            leader_count[const_name] = row[5]
            constituency_ids[const_name]=row[0]
        else:
            if leader_count[const_name] < row[5]:
                leader[const_name] = [cgi.escape(row[2]),row[3],row[4],row[7],row[8]]
                leader_count[const_name] = row[5]
            
        temp_count = vote_counts[const_name]
       
        cand_name = cgi.escape(row[2]) if (str(row[3])==str(candidate_id)) else "Others"
        if not cand_name in temp_count:
            temp_count[cand_name]=0
            candidate_name = cand_name
        temp_count[cand_name] = temp_count[cand_name]+row[5]
        vote_counts[const_name] = temp_count
        """ Even if one of the status is 'counting' the status of the constituency is counting"""
        result_status[const_name] = 'Not Started' if (cgi.escape(row[9])=='NOT_STARTED') else cgi.escape(row[7]).title()
    results = []
    for constituency in vote_counts.iterkeys():
        temp = {}
        temp_list = []
        for candid_temp in vote_counts[constituency].iterkeys():
            temp_list.append({'name':candid_temp,'votes':vote_counts[constituency][candid_temp]})
        temp['vote_share_details'] = temp_list
        cand_votes=vote_counts[constituency][candidate_name];
        other_votes=vote_counts[constituency]['Others']
        temp['candidate_votes']=cand_votes
        temp['other_votes']=other_votes
        temp['counting_status'] = result_status[constituency]
        temp['leader_name'] = leader[constituency][0]
        temp['leader_id'] = leader[constituency][1]
        temp['leader_party_id'] = leader[constituency][2]
        temp['leader_party_name']=leader[constituency][3]
        temp['leader_party_symbol']=leader[constituency][4]
        temp['leader_count'] = leader_count[constituency]
        temp['constituency_name']=constituency
        temp['constituency_id']=constituency_ids[constituency]
        results.append(temp)
    return json.dumps(results)

def get_candidate_result_2009(db,candidate_id):
    cursor = db.cursor()
    vote_counts={}
    leader = {}
    candidate_name=""
    leader_count= {}
    constituency_ids={}
    cursor.execute('''SELECT ca.id, ca.fullname, co.id, co.name, p.id, p.name, 
        p.symbol,l.votes FROM last_time_results l, candidate ca, 
        constituency co, party p where p.id=l.party_id 
        and ca.id=l.candidate_id and co.id=l.constituency_id 
        and l.constituency_id in (select constituency_id from 
        last_time_results where candidate_id='''+candidate_id+''');''')
  
    for row in cursor.fetchall():
        const_name = row[3];
        if not const_name in vote_counts:
            vote_counts[const_name] = {"Others":0}
            leader[const_name] = [cgi.escape(row[1]),row[0],row[4],row[5],row[6]]
            leader_count[const_name] = row[7]
            constituency_ids[const_name]=row[2]
        else:
            if leader_count[const_name] < row[7]:
                leader[const_name] = [cgi.escape(row[1]),row[0],row[4],row[5],row[6]]
                leader_count[const_name] = row[7]
            
        temp_count = vote_counts[const_name]
       
        cand_name = cgi.escape(row[1]) if (str(row[0])==str(candidate_id)) else "Others"
        if not cand_name in temp_count:
            temp_count[cand_name]=0
            candidate_name = cand_name
        
        temp_count[cand_name] = temp_count[cand_name]+row[7]
        vote_counts[const_name] = temp_count
        """ Even if one of the status is 'counting' the status of the constituency is counting"""
        results = []
    for constituency in vote_counts.iterkeys():
        temp = {}
        temp_list = []
        for candid_temp in vote_counts[constituency].iterkeys():
            temp_list.append({'name':candid_temp,'votes':vote_counts[constituency][candid_temp]})
        temp['vote_share_details'] = temp_list
        cand_votes=vote_counts[constituency][candidate_name];
        other_votes=vote_counts[constituency]['Others']
        temp['candidate_votes']=cand_votes
        temp['other_votes']=other_votes
        temp['winner_name'] = leader[constituency][0]
        temp['winner_id'] = leader[constituency][1]
        temp['winner_party_id'] = leader[constituency][2]
        temp['winner_party_name']=leader[constituency][3]
        temp['winner_party_symbol']=leader[constituency][4]
        temp['winner_count'] = leader_count[constituency]
        temp['constituency_name']=constituency
        temp['constituency_id']=constituency_ids[constituency]
        results.append(temp)
    return json.dumps(results)
