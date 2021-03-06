"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, make_response
import os
import cgi
import jinja2
import MySQLdb
import json
import sys
import pickle
import datetime
import candidate
import constituency
import party
from google.appengine.api import memcache
from random import random

# Configure the Jinja2 environment.
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    autoescape=True,
    extensions=['jinja2.ext.autoescape'])

# Define your production Cloud SQL instance information.
_INSTANCE_NAME = 'indiaelectiontracker:ls14'

app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


def get_data_multiple_params(fnname, param1,param2):
    key = fnname + ":" + param1+":"+param2
    data = cache_store(key)
    if data is not None:
        return data
    else:
        data = getattr(sys.modules[__name__], fnname)(param1,param2)
        cache_retrieve(key, data, 300)
        return data


def get_data_multiple_params_ex(module_name,fnname, param1,param2):
    key = module_name+":"+fnname + ":" + param1+":"+param2
    data = cache_retrieve(key)
    if data is not None:
        return data
    else:
        data = getattr(sys.modules[module_name], fnname)(get_db(),param1,param2)
        cache_store(key, data, 300)
        return data


def get_data(fnname, param):
    key = fnname + ":" + param
    data = cache_retrieve(key)
    if data is not None:
        return data
    else:
        data = getattr(sys.modules[__name__], fnname)(param)
        cache_store(key, data, 300)
        return data


def cache_store(key, value, time=30, chunksize=950000):
    serialized = pickle.dumps(value, 2)
    values = {}
    for i in xrange(0, len(serialized), chunksize):
        values['%s.%s' % (key, i//chunksize)] = serialized[i : i+chunksize]
    memcache.set_multi(values,time)


def cache_retrieve(key):
    result = memcache.get_multi(['%s.%s' % (key, i) for i in xrange(32)])
    serialized = ''.join([v for k, v in sorted(result.items()) if v is not None])
    if serialized=='':
        return None
    return pickle.loads(serialized)


""" This is a slightly modified version of get_data, which also takes the module name, and 
passes the db object to the data model function"""
def get_data_ex(module_name,fnname, param, expiry_time=300):
    key = module_name+":"+fnname + ":" + param
    data = cache_retrieve(key)
    if data is not None:
        return data
    else:
        data = getattr(sys.modules[module_name], fnname)(get_db(),param)
        cache_store(key, data, expiry_time)
        return data


@app.route('/')
@app.route('/party')
@app.route('/party/<id>')
@app.route('/coalition/<id>')
@app.route('/coalition/state/<id>/<id2>')
@app.route('/party/state/<id>/<id2>')
@app.route('/constituency')
@app.route('/constituency/<id>')
@app.route('/state')
@app.route('/state/<id>')
@app.route('/candidate/<id>')
@app.route('/aboutus')
def default_route(id=None,id2=None):
    return make_response(open('templates/index.html').read())


@app.route('/api/party')
def api_party_list():
    output = get_data_ex('party','get_party_list', '')
    return output;


@app.route('/api/party/<party_id>')
def api_party(party_id):
    output = get_data_ex('party','get_party', party_id)
    return output;


@app.route('/api/coalition/<coalition_id>')
def api_coalition(coalition_id):
    output = get_data_ex('party','get_coalition', coalition_id)
    return output;

@app.route('/api/landing')
def api_landing():
    output = get_data_ex('party','get_landing','')
    return output;


@app.route('/api/party/detailed_result_declared/<party_id>')
def api_party_detailed_result_declared(party_id):
    output = get_data_ex('party','get_party_detailed_result_declared', party_id)
    return output;

@app.route('/api/party/detailed_result_undeclared/<party_id>')
def api_party_detailed_result_undeclared(party_id):
    output = get_data_ex('party','get_party_detailed_result_undeclared', party_id)
    return output

@app.route('/api/coalition/state/detailed_result_declared/<coalition_id>/<state_id>')
def api_coalition_state_detailed_result_declared(coalition_id,state_id):
    output = get_data_multiple_params_ex('party','get_coalition_state_detailed_result_declared', coalition_id,state_id)
    return output

@app.route('/api/coalition/state/detailed_result_undeclared/<coalition_id>/<state_id>')
def api_coalition_state_detailed_result_undeclared(coalition_id,state_id):
    output = get_data_multiple_params_ex('party','get_coalition_state_detailed_result_undeclared', coalition_id,state_id)
    return output

@app.route('/api/coalition/detailed_result_declared/<coalition_id>')
def api_coalition_detailed_result_declared(coalition_id):
    output = get_data_ex('party','get_coalition_detailed_result_declared', coalition_id)
    return output

@app.route('/api/coalition/detailed_result_declared_1/<coalition_id>')
def api_coalition_detailed_result_declared(coalition_id):
    output = get_data_ex('party','get_coalition_detailed_result_declared_1', coalition_id)
    return output

@app.route('/api/coalition/detailed_result_undeclared/<coalition_id>')
def api_coalition_detailed_result_undeclared(coalition_id):
    output = get_data_ex('party','get_coalition_detailed_result_undeclared', coalition_id)
    return output

@app.route('/api/party/state/detailed_result_declared/<party_id>/<state_id>')
def api_party_state_detailed_result_declared(party_id,state_id):
    output = get_data_multiple_params_ex('party','get_party_state_detailed_result_declared', party_id,state_id)
    return output

@app.route('/api/party/state/detailed_result_undeclared/<party_id>/<state_id>')
def api_party_state_detailed_result_undeclared(party_id,state_id):
    output = get_data_multiple_params_ex('party','get_party_state_detailed_result_undeclared', party_id,state_id)
    return output

@app.route('/api/party/statewise_result/<party_id>')
def api_party_statewise_result(party_id):
    return get_data_ex('party','get_party_statewise_result',party_id,300)

@app.route('/api/coalition/statewise_result/<coalition_id>')
def api_coalition_statewise_result(coalition_id):
    return get_data_ex('party','get_coalition_statewise_result',coalition_id,300)

@app.route('/api/party/result/<party_id>')
def api_party_result(party_id):
    return get_data_ex('party','get_party_result',party_id)

@app.route('/api/coalition/state/result/<coalition_id>/<state_id>')
def api_coalition_state_result(coalition_id,state_id):
    return get_data_multiple_params_ex('party','get_coalition_state_result',coalition_id,state_id)

@app.route('/api/coalition/result/<coalition_id>')
def api_coalition_result(coalition_id):
    return get_data_ex('party','get_coalition_result',coalition_id)

@app.route('/api/coalition/parties/<coalition_id>')
def api_coalition_parties(coalition_id):
    return get_data_ex('party','get_coalition_parties',coalition_id)

@app.route('/api/coalition/state/parties/<coalition_id>/<state_id>')
def api_coalition_state_parties(coalition_id,state_id):
    return get_data_multiple_params_ex('party','get_coalition_state_parties',coalition_id,state_id)

@app.route('/api/party/state/result/<party_id>/<state_id>')
def api_party_state_result(party_id,state_id):
    return get_data_multiple_params_ex('party','get_party_result_by_state',party_id,state_id)

@app.route('/api/party/vote_percentage/<party_id>')
def api_party_vote_percentage(party_id):
    return get_data_ex('party','get_party_vote_percentage',party_id)


@app.route('/api/party/vote_percentage/<party_id>/<state_id>')
def api_party_vote_percentage_state(party_id,state_id):
    return get_data_multiple_params_ex('party','get_vote_percentage_for_party_state',party_id,state_id)
#@app.route('/api/party/result_summary/<partyId>')
#def get_party_result_summary(partyId):

@app.route('/api/state')
def api_state_list():
    output = get_data('get_state_list', '')
    return output;


def get_state_list(param):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('select count(c.id),s.* from constituency c inner join state s on s.id = c.state_id group by c.state_id;')
    statelist = []
    for row in cursor.fetchall():
        statelist.append(dict([('id', row[1]),
                               ('name', row[2]),
                               ('number_of_seats', row[0]),
                               ('shortform', cgi.escape(row[3])),
                               ('state_code', cgi.escape(row[4]))]))
    cursor.close()

    return json.dumps(statelist)

@app.route('/api/state/<state_id>')
def api_state(state_id):
    output = get_data('get_state', state_id)
    return output;

def get_state(state_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id, name, shortform, state_code FROM state where id = ' + state_id + ';')
    row = cursor.fetchone();
    state = dict([('id', row[0]),
                  ('name', cgi.escape(row[1])),
                  ('shortform', cgi.escape(row[2])),
                  ('state_code', cgi.escape(row[3]))])
    cursor.close()
    return json.dumps(state)


@app.route('/api/state/constituency_list/<state_id>')
def api_constituency_list_for_state(state_id):
    output = get_data('get_constituency_list_for_state', state_id)
    return output;


def get_constituency_list_for_state(state_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('Select c.id, c.name, c.constituency_code, c.state_id, s.name from constituency c inner join state s on s.id = c.state_id where s.id = ' + state_id + ';')
    cList = []
    for row in cursor.fetchall():
        cList.append({"id": row[0], "name": cgi.escape(row[1]), "constituency_code": cgi.escape(row[2]), "state_id": row[3], "state_name": cgi.escape(row[4])})
    cursor.close()
    return json.dumps(cList)


@app.route('/api/state/result/<state_id>')
def api_state_result(state_id):
    output = get_data('get_state_result', state_id)
    return output;


def get_state_result(state_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("select count(constituency_id),p.id,status from latest_results lr inner join party p on lr.party_id = p.id inner join constituency c on c.id = lr.constituency_id where c.state_id = %s group by status,p.id;",state_id);

    party_wins_leads = {}
    for row in cursor.fetchall():
        if str(row[1]) not in party_wins_leads:
            party_wins_leads[str(row[1])]={'wins':0,'leads':0}
        else:
            pass
        if(row[2]=='DECLARED'):
            party_wins_leads[str(row[1])]['wins']=str(row[0])
        elif(row[2]=='COUNTING'):
            party_wins_leads[str(row[1])]['leads']=str(row[0])

    cursor.execute(
        """select p.id, p.name, p.symbol, p.shortform, sum(rs.votes) as votes from results rs inner join candidate_constituency cc on cc.constituency_id = rs.constituency_id and cc.candidate_id = rs.candidate_id inner join party p on cc.party_id = p.id inner join constituency cs on cs.id = rs.constituency_id where cs.state_id = %s and cc.election = '2014' and rs.active = 1 group by cc.party_id order by votes desc;""", (state_id))


    results = []
    for row in cursor.fetchall():
        party_id = str(row[0])
        result = {"party_id": party_id, "party_name": row[1], "party_symbol": row[2],
                  "party_shortform": row[3], "votes": str(row[4])}
        if party_id in party_wins_leads:
            result["wins"] = party_wins_leads[party_id]["wins"]
            result["leads"] = party_wins_leads[party_id]["leads"]
        else:
            result["wins"] = str(0)
            result["leads"] = str(0)
        results.append(result)
    cursor.close()
    return json.dumps(results)


@app.route('/api/constituency')
def api_constituency_list():
    '''longish expiry time'''
    output = get_data_ex('constituency','get_constituency_list', '',5000) 
    return output;


@app.route('/api/constituency/<constituency_id>')
def api_constituency(constituency_id):
    output = get_data_ex('constituency','get_constituency_info', constituency_id)
    return output;


@app.route('/api/constituency/result/<constituency_id>')
def api_constituency_result(constituency_id):
    output = get_data_ex('constituency','get_constituency_result', constituency_id)
    return output;


@app.route('/api/constituency/result2009/<constituency_id>')
def api_constituency_result_2009(constituency_id):
    '''longish expiry time because this data doesn't change'''
    output = get_data_ex('constituency','get_constituency_result_2009', constituency_id, 5000) 
    return output;


@app.route('/api/candidate')
def api_candidate_list():
    '''longish expiry time'''
    output = get_data_ex('candidate','get_candidate_list', "ALL",300) 
    return output;


@app.route('/api/candidate/<candidate_id>')
def api_candidate(candidate_id):
    output = get_data_ex('candidate','get_candidate_info', candidate_id,1000) 
    return output;


@app.route('/api/candidate/result/<candidate_id>')
def api_candidate_result(candidate_id):
    output = get_data_ex('candidate','get_candidate_result', candidate_id)
    return output;


"""
def populate_dirty_candidate_constituency():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("select rs.candidate_id,rs.constituency_id,rs.status,rs.party_id from results rs")
    for row in cursor.fetchall():
        curs = db.cursor()
        curs.execute("insert into candidate_constituency (election,candidate_id,constituency_id,party_id) values ('%s',%s,%s,%s)"% ("2014",row[0],row[1],row[3]))
        curs.execute("update constituency set result_status = '%s'"% row[2])
        db.commit()
        curs.close()
"""

@app.route('/api/candidate/result2009/<candidate_id>')
def api_candidate_result_2009(candidate_id):
    output = get_data_ex('candidate', 'get_candidate_result_2009', candidate_id)
    return output;


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def page_not_found(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500


def connect_db():
    """Connects to the specific database."""
    if (os.getenv('SERVER_SOFTWARE') and
            os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
        db = MySQLdb.connect(unix_socket='/cloudsql/' + _INSTANCE_NAME, db='resultdayanalysis', user='ls14',
                             passwd='')
    else:
        db = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='resultdayanalysis')
        # Alternately, connect to a Google Cloud SQL instance using:
        # db = MySQLdb.connect(host='ip-address-of-google-cloud-sql-instance', port=3306, user='root')
    return db


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'mysql_db'):
        g.mysql_db = connect_db()
    return g.mysql_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'mysql_db'):
        g.mysql_db.close()




#if __name__ == '__main__':
#	app.run(debug=True)
