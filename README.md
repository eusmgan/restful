https://pythonspot.com/python-database-postgresql/

change the following line
# Database administrative login by Unix domain socket
local   all             postgres                                trust
in /etc/postgresql/9.5/main/pg_hba.conf

sh create_database.sh
