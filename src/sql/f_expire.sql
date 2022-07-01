CREATE FUNCTION %(function_name)s() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  DELETE FROM %(table_name)s WHERE %(time_field)s < NOW() - INTERVAL '%(expire_sec)d seconds';
  RETURN NEW;
END;
$$;