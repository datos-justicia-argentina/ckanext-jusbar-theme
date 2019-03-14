


# init docker
docker start postgres-dev solrckan

# stop jetty
/etc/init.d/jetty9 stop

# activate environment
cd /usr/lib/ckan/default 
. bin/activate.fish 

# setting vars
no_proxy for solr:
export no_proxy="localhost, 172.17.0.3"

# run
paster serve /home/nuxion/Projects/ckan/development.ini

