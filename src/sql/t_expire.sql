CREATE TRIGGER %(trigger_name)s
    AFTER INSERT ON %(table_name)s
    EXECUTE PROCEDURE %(function_name)s();