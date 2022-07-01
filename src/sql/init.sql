CREATE DATABASE ziem;
CREATE USER zuser;

DO
$do$
BEGIN
    IF EXISTS (SELECT FROM pg_database WHERE datname = 'ziem') THEN
        ALTER USER zuser WITH PASSWORD '%s';
    END IF;
END
$do$;

GRANT ALL PRIVILEGES ON DATABASE ziem TO zuser;