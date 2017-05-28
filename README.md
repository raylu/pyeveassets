`/etc/postgresql/9.6/main/pg_hba.conf`, change local access from `peer` to `trust`
```
sudo -u postgres psql
> create user pyeveassets;
> create database pyeveassets;
> grant all privileges on database pyeveassets to pyeveassets;
sudo invoke-rc.d postgresql restart # pick up pg_hba.conf change
wget https://www.fuzzwork.co.uk/dump/postgres-latest.dmp.bz2
bunzip2 -c postgres-latest.dmp.bz2 | pg_restore -U pyeveassets -d pyeveassets -c -t invTypes -t staStations
psql -U pyeveassets -f schema.sql
```
copy `config.py.example` and set it up

nginx config:
```
server {
	server_name pyeveassets;

	listen 80;
	listen [::]:80;

	add_header X-Frame-Options DENY;
	add_header X-Content-Type-Options nosniff;
	add_header Content-Security-Policy "default-src none; style-src 'self'; img-src https: 'self'; script-src 'self'";
	add_header X-Xss-Protection "1; mode=block";
	charset utf-8;

	location /static {
		root /home/raylu/src/pyeveassets;
	}
	location / {
		include proxy_params;
		proxy_pass http://127.0.0.1:8000;
	}
}
```
