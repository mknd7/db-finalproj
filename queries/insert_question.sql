INSERT INTO Question (userid, topicid, qnwhen, title, qnbody)
	VALUES ('1', '3', NOW(), 'Why do aggregate functions not work in GROUP BY?', "When I try to use aggregate functions like sum() or count() in GROUP BY, I get a 'Misuse of aggregate function' error. How do I solve it?");
	-- the other columns are filled automatically by constraints