-- INTENTIONALLY VULNERABLE - Checkmarx One demo only.
CREATE OR REPLACE PROCEDURE get_user(p_name IN VARCHAR2) AS
  v_sql VARCHAR2(500);
BEGIN
  v_sql := 'SELECT * FROM users WHERE name = ''' || p_name || '''';  -- VULN-240 SQLi
  EXECUTE IMMEDIATE v_sql;
  EXECUTE IMMEDIATE 'GRANT DBA TO ' || p_name;                       -- VULN-241 privilege escalation
END;
/
CREATE USER app IDENTIFIED BY "admin123";                            -- VULN-242 hardcoded weak password
