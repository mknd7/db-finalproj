DELIMITER $$
CREATE TRIGGER calc_status
	AFTER UPDATE ON Answer
    FOR EACH ROW
BEGIN
	DECLARE total_upvotes INT;
	SELECT sum(A.upvotes) INTO total_upvotes
		FROM Answer A
		JOIN User ON A.userid=User.userid
		WHERE NEW.userid=A.userid;
	UPDATE User U
    SET U.status=(CASE
                  WHEN total_upvotes < 8 THEN 'beginner'
                  WHEN total_upvotes BETWEEN 8 AND 23 THEN 'intermediate'
                  WHEN total_upvotes BETWEEN 24 AND 79 THEN 'advanced'
                  WHEN total_upvotes >= 80 THEN 'expert'
                  END)
    WHERE NEW.userid=U.userid;
END;
DELIMITER ;