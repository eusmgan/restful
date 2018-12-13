sudo cp pg_hba.conf /etc/postgresql/9.5/main/pg_hba.conf
sudo service postgresql restart
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"
psql -U postgres postgres -f db_create.sql
