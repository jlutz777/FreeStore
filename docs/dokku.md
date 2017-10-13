# Dokku
Dokku is used for deployment on a Digital Ocean VM. This gives an environment like heroku on a VM that I can control.

## Workaround
The port for the app needed to be hard-coded in /var/lib/dokku/plugins/postgresql/pre-deploy. In my case, it is set to 5432. I am not sure why this was needed

For example:
`echo "COMMAND: docker run -v $PG_VOLUME -p 5432:$PG_PORT -d $PG_APP_IMAGE /usr/bin/start_pgsql.sh $DB_PASSWORD"
        ID=$(docker run -v $PG_VOLUME -p $PG_PORT:5432 -d $PG_APP_IMAGE /usr/bin/start_pgsql.sh $DB_PASSWORD)
        sleep 1
`