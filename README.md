`/etc/postgresql/9.6/main/pg_hba.conf`, change local access from `peer` to `trust`
```
sudo -u postgres psql
> create user pyeveassets;
> create database pyeveassets;
> grant all privileges on database pyeveassets to pyeveassets;
sudo invoke-rc.d postgresql restart # pick up pg_hba.conf change
```
