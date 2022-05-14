DELIMITER $$
CREATE PROCEDURE get_relevant_qns(IN keyword VARCHAR(45))
BEGIN
    SELECT title, topicname
    FROM Question Q
    JOIN Topic T ON Q.topicid=T.topicid
    WHERE CONTAINS(title, keyword) -- or MATCH (title) AGAINST (keyword)
    ORDER BY topicname
END;
DELIMITER ;