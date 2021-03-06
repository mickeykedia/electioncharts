"""methods pertaining to candidates"""

# Import the Flask Framework

import json
import cgi

def get_constituency_list(db,param):
    cursor = db.cursor()
    cursor.execute('''Select c.id, c.name, c.constituency_code, c.state_id, 
    s.name, c.result_status from constituency c inner join state s on s.id = c.state_id;''')
    cList = []
    for row in cursor.fetchall():
        cList.append({"id": row[0], "name": cgi.escape(row[1]), \
                      "constituency_code": cgi.escape(row[2]), "state_id": row[3],\
                      "state_name": cgi.escape(row[4]),"voting_status":cgi.escape(row[5])})
        
    return json.dumps(cList)


def get_constituency_info(db,constituency_id):
    cursor = db.cursor()
    cursor.execute('''Select c.id, c.name, c.constituency_code, c.state_id, s.name, c.result_status 
        from constituency c inner join state s on s.id = c.state_id 
        where c.id = ''' + constituency_id + ''';''')
    row = cursor.fetchone()
    voting_status=cgi.escape(row[5])
    
    voting_status=voting_status.title() if (voting_status!="NOT_STARTED") else "Not Started"
    constituency = {"id": row[0], "name": row[1], \
                    "constituency_code": cgi.escape(row[2]), \
                    "state_id": row[3], "state_name": cgi.escape(row[4]),\
                    "voting_status":voting_status}
    result = get_constituency_result_1(db,constituency_id)
    for result_item in result.iterkeys():
        constituency[result_item]=result[result_item]
    return json.dumps(constituency)


def get_constituency_result_1(db,constituency_id):
    cursor = db.cursor()
    cursor.execute('''SELECT ca.id, ca.fullname, p.id, p.name, r.time_start, r.votes, p.symbol
      FROM results r, candidate_constituency c_c, candidate ca, constituency co, party p 
      where c_c.constituency_id=co.id and c_c.candidate_id=ca.id 
      and c_c.party_id=p.id and r.candidate_id=ca.id and r.constituency_id=co.id 
      and r.active=1  and c_c.election="2014" and r.constituency_id='''+ constituency_id +''' order 
      by r.votes desc;''')
    output={'total_votes':0}
    results=[]
    for row in cursor.fetchall():
        temp_map={}
        temp_map['candidate_id']=row[0]
        temp_map['candidate_name']=cgi.escape(row[1]).title()
        temp_map['party_id']=row[2]
        temp_map['party_name']=cgi.escape(row[3]).title()
        temp_map['votes']=row[5]
        temp_map['party_symbol']=row[6]
        output['total_votes']=output['total_votes']+row[5]
        results.append(temp_map)
    output['result_list']=results
    return output

def get_constituency_result(db,constituency_id):
    result = get_constituency_result_1(db,constituency_id)
    return json.dumps(result['result_list'])


def get_constituency_result_2009(db,constituency_id):
    cursor = db.cursor()
    cursor.execute('''SELECT ca.id, ca.fullname, p.id, p.name, l.votes
      FROM last_time_results l, candidate ca, constituency co, party p 
      where l.constituency_id=co.id and l.candidate_id=ca.id 
      and l.party_id=p.id and l.candidate_id=ca.id and l.constituency_id=co.id 
      and l.constituency_id='''+ constituency_id +''' order 
      by l.votes desc;''')
    results=[]
    total_votes=0
    for row in cursor.fetchall():
        temp_map={}
        temp_map['candidate_id']=row[0]
        temp_map['candidate_name']=cgi.escape(row[1]).title()
        temp_map['party_id']=row[2]
        temp_map['party_name']=cgi.escape(row[3]).title()
        temp_map['votes']=row[4]
        total_votes=total_votes+row[4]
        results.append(temp_map)
    new_results = []
    for rec in results:
        rec['total_votes']=total_votes
        new_results.append(rec)
    
    return json.dumps(new_results)