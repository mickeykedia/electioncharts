
# Import the Flask Framework
import json
import cgi


def get_party_wins_sql_string(party_id):
	"""

    :type party_id: integer
    """
	str = """ select
        lr.candidate_id,
        c.fullname as winning_candidate,
        lr.constituency_id,
        cons.name as constituency,
        lr.party_id,
        lr.max_votes,
        (lr.max_votes-sr.votes) as lead,
        sr.candidate_id,
        loosing_candidate.fullname as runner_up,
        loosing_party.name as runner_up_party,
        sr.party_id,
        ltr.party_id
        from latest_results lr
        inner join
            latest_runners_up as sr
            on
            sr.constituency_id = lr.constituency_id
        inner join
            candidate c
            on
            c.id = lr.candidate_id
        inner join
            constituency cons
            on
            cons.id = lr.constituency_id
        inner join party loosing_party
            on
            loosing_party.id = sr.party_id
        inner join candidate loosing_candidate
            on
            loosing_candidate.id = sr.candidate_id
        inner join last_time_winners ltr
            on
            ltr.constituency_id=lr.constituency_id
        where
            lr.party_id = %s
        and
            lr.status = 'DECLARED'
        order by
            lead DESC""" % party_id
	return str;

def get_party_leads_sql_string(party_id):
	"""

    :type party_id: integer
    """
	str = """ select
        lr.candidate_id,
        c.fullname as winning_candidate,
        lr.constituency_id,
        cons.name as constituency,
        lr.party_id,
        lr.max_votes,
        (lr.max_votes-sr.votes) as lead,
        sr.candidate_id,
        loosing_candidate.fullname as runner_up,
        loosing_party.name as runner_up_party,
        sr.party_id,
        ltr.party_id
        from latest_results lr
        inner join
            latest_runners_up as sr
            on
            sr.constituency_id = lr.constituency_id
        inner join
            candidate c
            on
            c.id = lr.candidate_id
        inner join
            constituency cons
            on
            cons.id = lr.constituency_id
        inner join party loosing_party
            on
            loosing_party.id = sr.party_id
        inner join candidate loosing_candidate
            on
            loosing_candidate.id = sr.candidate_id
        inner join last_time_winners ltr
            on
            ltr.constituency_id=lr.constituency_id
        where
            lr.party_id = %s
        and
            lr.status = 'COUNTING'
        order by
            lead DESC""" % party_id
	return str;

def get_party_trails_sql_string(party_id,state):
	str = """select
        rs.constituency_id,
        cs.name as constituency,
        rs.candidate_id,
        c.fullname as candidate_name,
        (rs.votes-MY.max_votes) as trail,
        rs.votes,
        p.name as winning_party,
        MY.candidate_id,
        wc.fullname,
        MY.max_votes as max_votes,
        ltr.party_id,
        p.id
        from
            results rs
        inner join candidate c
            on
            c.id = rs.candidate_id
        inner join constituency cs
            on
            cs.id = rs.constituency_id
        inner join candidate_constituency cc
            on
			cc.candidate_id = rs.candidate_id
			and
			cc.constituency_id = rs.constituency_id
        inner join latest_results as MY
            on
            MY.constituency_id = rs.constituency_id
        inner join party p
            on
            p.id = MY.party_id
        inner join candidate wc
            on
            wc.id = MY.candidate_id
        inner join last_time_winners ltr
            on
            ltr.constituency_id=rs.constituency_id
        where
            rs.active = true
            and
            cc.party_id = %s
            and
            cc.election = '2014'
            and
            cs.result_status = '%s'
            and
            rs.candidate_id not in (select candidate_id from latest_results)
        order by
            trail desc;""" % (party_id,state)
	return str;

def get_party_wins_sql_string_for_state(party_id,state_id):
	"""

    :type party_id: integer
    """
	str = """ select
        lr.candidate_id,
        c.fullname as winning_candidate,
        lr.constituency_id,
        cons.name as constituency,
        lr.party_id,
        lr.max_votes,
        (lr.max_votes-sr.votes) as lead,
        sr.candidate_id,
        loosing_candidate.fullname as runner_up,
        loosing_party.name as runner_up_party,
        sr.party_id,
        ltr.party_id
        from latest_results lr
        inner join
            latest_runners_up as sr
            on
            sr.constituency_id = lr.constituency_id
        inner join
            candidate c
            on
            c.id = lr.candidate_id
        inner join
            constituency cons
            on
            cons.id = lr.constituency_id
        inner join party loosing_party
            on
            loosing_party.id = sr.party_id
        inner join candidate loosing_candidate
            on
            loosing_candidate.id = sr.candidate_id
        inner join last_time_winners ltr
            on
            ltr.constituency_id=lr.constituency_id
        where
            lr.party_id = %s
        and
            lr.status = 'DECLARED'
        and
            cons.state_id = %s
        order by
            lead DESC""" % (party_id,state_id)
	return str;

def get_party_leads_sql_string_for_state(party_id, state_id):
	"""

	:type party_id: integer
	"""
	str = """ select
        lr.candidate_id,
        c.fullname as winning_candidate,
        lr.constituency_id,
        cons.name as constituency,
        lr.party_id,
        lr.max_votes,
        (lr.max_votes-sr.votes) as lead,
        sr.candidate_id,
        loosing_candidate.fullname as runner_up,
        loosing_party.name as runner_up_party,
        sr.party_id,
        ltr.party_id
        from latest_results lr
        inner join
            latest_runners_up as sr
            on
            sr.constituency_id = lr.constituency_id
        inner join
            candidate c
            on
            c.id = lr.candidate_id
        inner join
            constituency cons
            on
            cons.id = lr.constituency_id
        inner join party loosing_party
            on
            loosing_party.id = sr.party_id
        inner join candidate loosing_candidate
            on
            loosing_candidate.id = sr.candidate_id
        inner join last_time_winners ltr
            on
            ltr.constituency_id=lr.constituency_id
        where
            lr.party_id = %s
		and
			cons.state_id = %s
        and
            lr.status = 'COUNTING'
        order by
            lead DESC""" % (party_id, state_id)
	return str;


def get_party_trails_sql_string_for_state(party_id, state_id,state):
	str = """select
        rs.constituency_id,
        cs.name as constituency,
        rs.candidate_id,
        c.fullname as candidate_name,
        (rs.votes-MY.max_votes) as trail,
        rs.votes,
        p.name as winning_party,
        MY.candidate_id,
        wc.fullname,
        MY.max_votes as max_votes,
        ltr.party_id,
        p.id
        from
            results rs
        inner join candidate c
            on
            c.id = rs.candidate_id
        inner join constituency cs
            on
            cs.id = rs.constituency_id
        inner join candidate_constituency cc
            on
			cc.candidate_id = rs.candidate_id
			and
			cc.constituency_id = rs.constituency_id
        inner join latest_results MY
            on
            MY.constituency_id = rs.constituency_id
        inner join party p
            on
            p.id = MY.party_id
        inner join candidate wc
            on
            wc.id = MY.candidate_id
        inner join last_time_winners ltr
            on
            ltr.constituency_id=rs.constituency_id
        where
            rs.active = true
            and
            cc.party_id = %s
            and
            cc.election = '2014'
            and
            cs.result_status = '%s'
            and
            cs.state_id = %s
            and
            rs.candidate_id not in (select candidate_id from latest_results)
        order by
            trail desc;""" % (party_id, state,state_id)
	return str;


def get_coalition_wins_sql_string(coalition_id):

	"""

    :type coalition_id: integer
    """
	str = """ select
        lr.candidate_id,
        c.fullname as winning_candidate,
        lr.constituency_id,
        cons.name as constituency,
        lr.party_id,
        lr.max_votes,
        (lr.max_votes-sr.votes) as lead,
        sr.candidate_id,
        loosing_candidate.fullname as runner_up,
        loosing_party.name as runner_up_party,
        sr.party_id,
        winning_party.name,
        ltw.party_id
        from latest_results lr
        inner join
            latest_runners_up as sr
            on
            sr.constituency_id = lr.constituency_id
        inner join
            candidate c
            on
            c.id = lr.candidate_id
        inner join
            constituency cons
            on
            cons.id = lr.constituency_id
		inner join party winning_party
			on
			lr.party_id = winning_party.id
        inner join party loosing_party
            on
            loosing_party.id = sr.party_id
        inner join candidate loosing_candidate
            on
            loosing_candidate.id = sr.candidate_id
		inner join last_time_winners ltw
			on
			ltw.constituency_id = lr.constituency_id
        where
            winning_party.coalition_id = %s
        and
            lr.status = 'DECLARED'
        order by
            lead DESC""" % coalition_id
	return str;

def get_coalition_leads_sql_string(coalition_id):

	"""

    :type coalition_id: integer
    """
	str = """ select
        lr.candidate_id,
        c.fullname as winning_candidate,
        lr.constituency_id,
        cons.name as constituency,
        lr.party_id,
        lr.max_votes,
        (lr.max_votes-sr.votes) as lead,
        sr.candidate_id,
        loosing_candidate.fullname as runner_up,
        loosing_party.name as runner_up_party,
        sr.party_id,
        lead_party.name as party_name,
        ltw.party_id as last_time_party_id
        from latest_results lr
        inner join
            latest_runners_up as sr
            on
            sr.constituency_id = lr.constituency_id
        inner join
            candidate c
            on
            c.id = lr.candidate_id
        inner join
            constituency cons
            on
            cons.id = lr.constituency_id
        inner join party loosing_party
            on
            loosing_party.id = sr.party_id
        inner join candidate loosing_candidate
            on
            loosing_candidate.id = sr.candidate_id
		inner join party lead_party
			on
			lead_party.id = lr.party_id
		inner join last_time_winners ltw
			on
			ltw.constituency_id = lr.constituency_id
        where
            lead_party.coalition_id = %s
        and
            lr.status = 'COUNTING'
        order by
            lead DESC""" % coalition_id
	return str;


def get_coalition_trails_sql_string(coalition_id,state):
	str = """select
        rs.constituency_id,
        cs.name as constituency,
        rs.candidate_id,
        c.fullname as candidate_name,
        (rs.votes-MY.max_votes) as trail,
        rs.votes,
        p.name as winning_party,
        MY.candidate_id,
        wc.fullname,
        MY.max_votes as max_votes,
        loosing_party.name as party_name,
        cc.party_id,
        ltw.party_id
        from
            results rs
        inner join candidate c
            on
            c.id = rs.candidate_id
        inner join constituency cs
            on
            cs.id = rs.constituency_id
        inner join candidate_constituency cc
            on
			cc.candidate_id = rs.candidate_id
			and
			cc.constituency_id = rs.constituency_id
        inner join latest_results as MY
            on
            MY.constituency_id = rs.constituency_id
        inner join party p
            on
            p.id = MY.party_id
        inner join candidate wc
            on
            wc.id = MY.candidate_id
        inner join party loosing_party
            on
            loosing_party.id = cc.party_id
		inner join last_time_winners ltw
			on
			ltw.constituency_id = rs.constituency_id
        where
            rs.active = true
            and
            loosing_party.coalition_id = %s
            and
            cc.election = '2014'
            and
            cs.result_status = '%s'
            and
            rs.candidate_id not in (select candidate_id from latest_results)
        order by
            trail desc;""" % (coalition_id,state)
	return str;

def get_coalition_wins_sql_string_for_state(coalition_id,state_id):

	"""

    :type party_id: integer
    """
	str = """ select
        lr.candidate_id,
        c.fullname as winning_candidate,
        lr.constituency_id,
        cons.name as constituency,
        lr.party_id,
        lr.max_votes,
        (lr.max_votes-sr.votes) as lead,
        sr.candidate_id,
        loosing_candidate.fullname as runner_up,
        loosing_party.name as runner_up_party,
        sr.party_id,
        winning_party.name,
        ltw.party_id
        from latest_results lr
        inner join
            latest_runners_up as sr
            on
            sr.constituency_id = lr.constituency_id
        inner join
            candidate c
            on
            c.id = lr.candidate_id
        inner join
            constituency cons
            on
            cons.id = lr.constituency_id
		inner join party winning_party
			on
			lr.party_id = winning_party.id
        inner join party loosing_party
            on
            loosing_party.id = sr.party_id
        inner join candidate loosing_candidate
            on
            loosing_candidate.id = sr.candidate_id
		inner join last_time_winners ltw
			on
			ltw.constituency_id = lr.constituency_id
        where
            winning_party.coalition_id = %s
        and
            cons.state_id = %s
        and
            lr.status = 'DECLARED'
        order by
            lead DESC""" % (coalition_id,state_id)
	return str;

def get_coalition_leads_sql_string_for_state(coalition_id,state_id):

	"""

    :type party_id: integer
    """
	str = """ select
        lr.candidate_id,
        c.fullname as winning_candidate,
        lr.constituency_id,
        cons.name as constituency,
        lr.party_id,
        lr.max_votes,
        (lr.max_votes-sr.votes) as lead,
        sr.candidate_id,
        loosing_candidate.fullname as runner_up,
        loosing_party.name as runner_up_party,
        sr.party_id as runners_up,
        lead_party.name as party_name,
        ltw.party_id
        from latest_results lr
        inner join
            latest_runners_up as sr
            on
            sr.constituency_id = lr.constituency_id
        inner join
            candidate c
            on
            c.id = lr.candidate_id
        inner join
            constituency cons
            on
            cons.id = lr.constituency_id
        inner join party loosing_party
            on
            loosing_party.id = sr.party_id
        inner join candidate loosing_candidate
            on
            loosing_candidate.id = sr.candidate_id
		inner join party lead_party
			on
			lead_party.id = lr.party_id
		inner join last_time_winners ltw
			on
			ltw.constituency_id = lr.constituency_id
        where
            lead_party.coalition_id = %s
        and
            cons.state_id = %s
        and
            lr.status = 'COUNTING'
        order by
            lead DESC""" % (coalition_id,state_id)
	return str;

def get_coalition_trails_sql_string_for_state(coalition_id,state_id,state):
	str = """select
        rs.constituency_id,
        cs.name as constituency,
        rs.candidate_id,
        c.fullname as candidate_name,
        (rs.votes-MY.max_votes) as trail,
        rs.votes,
        p.name as winning_party,
        MY.candidate_id,
        wc.fullname,
        MY.max_votes as max_votes,
        loosing_party.name as party_name,
        cc.party_id as party_id,
        ltw.party_id as last_time_party_id
        from
            results rs
        inner join candidate c
            on
            c.id = rs.candidate_id
        inner join constituency cs
            on
            cs.id = rs.constituency_id
        inner join candidate_constituency cc
            on
			cc.candidate_id = rs.candidate_id
			and
			cc.constituency_id = rs.constituency_id
        inner join latest_results as MY
            on
            MY.constituency_id = rs.constituency_id
        inner join party p
            on
            p.id = MY.party_id
        inner join candidate wc
            on
            wc.id = MY.candidate_id
        inner join party loosing_party
            on
            loosing_party.id = cc.party_id
		inner join last_time_winners ltw
			on
			ltw.constituency_id = rs.constituency_id
        where
            rs.active = true
            and
            loosing_party.coalition_id = %s
            and
            cs.result_status = '%s'
            and
            cc.election = '2014'
            and
            cs.state_id = %s
            and
            rs.candidate_id not in (select candidate_id from latest_results)
        order by
            trail desc;""" % (coalition_id,state,state_id)
	return str;

"""
 script to check swing for parties in a any state etc.
select count(lr.constituency_id),lr.party_id,ltw.party_id
from last_time_winners ltw
inner join latest_results lr on lr.constituency_id = ltw.constituency_id and lr.party_id!=ltw.party_id

group by lr.party_id,ltw.party_id
"""