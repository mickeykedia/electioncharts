Create DATABASE resultdayanalysis;
use resultdayanalysis;

CREATE TABLE candidate_keys ( /* keys for various properties of a candidate - eg. current party, previous party, number of votes polled last time etc */
		id int NOT NULL AUTO_INCREMENT, 
		name varchar(500) NOT NULL,
		short_form varchar(10) NOT NULL,
		CONSTRAINT candidate_keys_pk PRIMARY KEY (id)
	);
CREATE TABLE candidate (
		id int NOT NULL AUTO_INCREMENT,
		fullname varchar(500) NOT NULL,
		age int, /* can be optional - baad mein fill kar sakte hain */
		first_timer boolean NOT NULL, /* whether the candidate is contesting for the first time */
		CONSTRAINT candidate_pk PRIMARY KEY (id)
	);

CREATE TABLE candidate_properties (
		id int NOT NULL AUTO_INCREMENT,
		candidate_id int NOT NULL, INDEX (candidate_id),
		key_id int NOT NULL, INDEX (candidate_id),
		value varchar(1024) NOT NULL,
		CONSTRAINT candidate_properties_pk PRIMARY KEY(id),
		CONSTRAINT candidate_properties_fk_1 FOREIGN KEY(candidate_id) REFERENCES candidate (id),
		CONSTRAINT candidate_properties_fk_2 FOREIGN KEY (key_id) REFERENCES candidate_keys (id)
	);
		

CREATE TABLE state (
		id int NOT NULL AUTO_INCREMENT, 
		name varchar(500) NOT NULL, 
		shortform varchar(10) , /* short form of the name of the state - if any */
		state_code varchar(10) NOT NULL, /* the code of the state accoding to the election commission */
		number_of_seats INT,
		CONSTRAINT state_pk PRIMARY KEY (id)
	
	);
CREATE TABLE coalition( 
		id int NOT NULL AUTO_INCREMENT, 
		name varchar(500) NOT NULL, /* name of the coalition - NDA, UPA etc */
		symbol varchar(500), /* name of the symbol image - which can be stored at some pre defined place in the app */
		shortform varchar(10) NOT NULL, /* short form of the coalition name */
		CONSTRAINT coalition_pk PRIMARY KEY (id)
	);

CREATE TABLE party ( 
		id int NOT NULL AUTO_INCREMENT,
		name varchar(500) NOT NULL,
		symbol varchar(500), /* name of the symbol image - which can be stored at some predefined place in the app */
		shortform varchar(10), /* short form of the name of the party */
		coalition_id int, INDEX(coalition_id), /* optional coalition of which the party is part of */
		colour varchar(128), /* optional coalition of which the party is part of */
		CONSTRAINT party_pk PRIMARY KEY (id),
		CONSTRAINT party_fk_1 FOREIGN KEY (coalition_id) REFERENCES coalition (id)
	);

CREATE TABLE constituency_keys ( /* keys for various properties of a constituency - eg. poll phase, poll date, voting percentage, incumbent party etc */
		id int NOT NULL AUTO_INCREMENT, 
		name varchar(500) NOT NULL,
		short_form varchar(10) NOT NULL,
		CONSTRAINT constituency_keys_pk PRIMARY KEY (id)
	);
CREATE TABLE constituency (
		id int NOT NULL AUTO_INCREMENT,
		name varchar(500) NOT NULL,
		state_id int NOT NULL,INDEX (state_id),
		constituency_code varchar(10) NOT NULL, INDEX (constituency_code), /* the constituency code as given by the election commission */
		result_status varchar(16) NOT NULL, /* the constituency code as given by the election commission */
		CONSTRAINT constituency_pk PRIMARY KEY (id),
		CONSTRAINT constituency_fk_1 FOREIGN KEY (state_id) REFERENCES state (id)
	);
CREATE TABLE constituency_properties (
		id int NOT NULL AUTO_INCREMENT,
		pc_id int NOT NULL, INDEX (pc_id),
		key_id int NOT NULL, INDEX (key_id),
		value varchar(1024) NOT NULL,
		CONSTRAINT constituency_properties_pk PRIMARY KEY(id),
		CONSTRAINT constituency_properties_fk_1 FOREIGN KEY(pc_id) REFERENCES constituency (id),
		CONSTRAINT constituency_properties_fk_2 FOREIGN KEY (key_id) REFERENCES constituency_keys (id)
	);
CREATE TABLE candidate_constituency (
		id int NOT NULL AUTO_INCREMENT,
		election enum('2014','2009') NOT NULL,
		candidate_id int NOT NULL, INDEX (candidate_id),
		constituency_id int NOT NULL, INDEX (constituency_id),
		party_id int NOT NULL, INDEX (party_id),
		CONSTRAINT candidate_constituency_pk PRIMARY KEY (id),
		CONSTRAINT candidate_constituency_fk_1 FOREIGN KEY (candidate_id) REFERENCES candidate(id),
		CONSTRAINT candidate_constituency_fk_2 FOREIGN KEY (constituency_id) references constituency(id),
		CONSTRAINT candidate_constituency_fk_3 FOREIGN KEY (party_id) references party(id),
		CONSTRAINT candidate_constituency_uk_1 UNIQUE(candidate_id,constituency_id,election)
	);

CREATE TABLE results (
		id int NOT NULL AUTO_INCREMENT,
		constituency_id int NOT NULL,INDEX (constituency_id),
		candidate_id int NOT NULL, INDEX (candidate_id),
		votes int NOT NULL,
		active boolean, /* if this is the latest result as of now */
		time_start datetime, /* the first time this row was polled from the ec website */
		primary key (id), 
		CONSTRAINT results_fk_1 FOREIGN KEY (constituency_id) REFERENCES constituency (id),
		CONSTRAINT results_fk_2 FOREIGN KEY (candidate_id) REFERENCES candidate (id)		
	);	
/**
*
* @TODO - create a new table for constituency_status. 
*/


CREATE TABLE last_time_results (
		candidate_id int NOT NULL,INDEX (candidate_id),
		constituency_id int NOT NULL, INDEX (constituency_id),
		votes int NOT NULL,
		party_id int, INDEX (party_id),
		CONSTRAINT last_time_results_fk_1 FOREIGN KEY (constituency_id) REFERENCES constituency (id),
		CONSTRAINT last_time_results_fk_2 FOREIGN KEY (candidate_id) REFERENCES candidate (id),
		CONSTRAINT last_time_results_fk_3 FOREIGN KEY (party_id) REFERENCES party (id)
	);

CREATE TABLE top_contests (
	url TEXT,
	name TEXT,
	comments TEXT
);



Create view latest_results 
	AS 
	SELECT rs1.constituency_id,rs1.candidate_id,cc.party_id as party_id,rs1.votes as max_votes,cs.result_status as status
	FROM 
		resultdayanalysis.results rs1 
	inner join 
		candidate_constituency cc 
		on 
			cc.candidate_id = rs1.candidate_id 
			and 
			cc.constituency_id = rs1.constituency_id
	inner join constituency cs
		on 
			cs.id = rs1.constituency_id
    LEFT JOIN 
		results rs2 
		on 
			rs1.constituency_id = rs2.constituency_id 
			and 
			rs1.votes < rs2.votes 
	WHERE 
		rs2.constituency_id IS NULL 
		and 
		rs1.active = 1 
		and 
		cc.election = '2014' ;

create view last_time_winners 
	AS 
	SELECT rs1.constituency_id,rs1.candidate_id,rs1.party_id as party_id,rs1.votes as max_votes
	FROM 
	resultdayanalysis.last_time_results rs1 
	LEFT JOIN  
	last_time_results rs2 on rs1.constituency_id = rs2.constituency_id and rs1.votes < rs2.votes
	WHERE rs2.constituency_id IS NULL ;

create view candidates_not_winners
	as 
		select * from results 
		where 
			candidate_id not in 
				(select candidate_id from latest_results )
			and active = 1;


create view latest_runners_up
	AS
		select rs1.*,cc.party_id from results rs1 
			inner join 
				candidate_constituency cc 
			on 
				cc.candidate_id = rs1.candidate_id 
				and 
				cc.constituency_id = rs1.constituency_id
			left join 
				candidates_not_winners rs2 
			on 
				rs1.constituency_id = rs2.constituency_id 
				and rs1.votes < rs2.votes
			where 
				rs1.candidate_id not in
				(select candidate_id from latest_results) 
				and rs1.active = 1
				and rs2.constituency_id is null
				and cc.election = '2014'
			order by
				constituency_id,
				votes DESC
		;
create view major_states 
	as 
			select s.*,count(c.id) 
				from state s inner join constituency c on c.state_id = s.id 
			group by s.id having count(c.id) > 3

		;
create view major_parties_in_major_states 
	as 
		select count(cc.id) as num_contesting_seats,p.id as party_id,p.name as party_name,c.state_id,ms.name 
			from party p 
			inner join candidate_constituency cc on cc.party_id = p.id 
			inner join constituency c on c.id = cc.constituency_id
			inner join major_states ms on ms.id = c.state_id
		where party_id !=6 and election ='2014'group by p.id,c.state_id having count(cc.id) > 5
		order by state_id
	;
