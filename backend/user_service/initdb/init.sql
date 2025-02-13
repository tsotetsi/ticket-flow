-- Create UserSrvice database.
CREATE DATABASE ${POSTGRES_DB};

-- Connect to the new database.
\c {POSTGRES_DB};

-- Create a user with a password.
CREATE USER ${POSTGRES_USER} WITH PASSWORD '${POSTGRES_PASSWORD}';

-- Grant all privileges on the database to the user.
GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO ${POSTGRES_USER};