MYAPACHE_HOME := $(HOME)/apache2

YO := $(shell whoami)
MYGROUP := $(shell groups | cut -d ' ' -f 1)

help:
	@echo 'make [startapache|stopapache|restartapache|setupapache]'


setupapache: $(MYAPACHE_HOME)/usr/lib/apache2/modules/mod_wsgi.so
	-mkdir -p $(MYAPACHE_HOME)/var/run/apache2
	-mkdir -p $(MYAPACHE_HOME)/var/lock
	-mkdir -p $(MYAPACHE_HOME)/var/log/apache2
	-mkdir -p $(MYAPACHE_HOME)/etc 
	-mkdir -p $(MYAPACHE_HOME)/var/www/html
	cp -pr /etc/apache2 $(MYAPACHE_HOME)/etc
	sed -i -e 's@USER=www-data@USER=$(YO)@' \
	       -e 's@GROUP=www-data@GROUP=$(MYGROUP)@' \
	       -e 's@=/var/@=$(MYAPACHE_HOME)/var/@' \
	       $(MYAPACHE_HOME)/etc/apache2/envvars
	sed -i -e 's@Listen 80@Listen 8080@' \
	       -e 's@Listen 443@Listen 8443@' \
	       $(MYAPACHE_HOME)/etc/apache2/ports.conf
	sed -i -e 's@VirtualHost .:80@VirtualHost *:8080@' \
	       -e 's@DocumentRoot /var/www/html@DocumentRoot $(MYAPACHE_HOME)/var/www/html@' \
	       $(MYAPACHE_HOME)/etc/apache2/sites-available/000-default.conf
	sed -i -e 's@Directory /var/www/@Directory $(MYAPACHE_HOME)/var/www/@' \
	       -e 's@^\tOptions Indexes FollowSymLinks@\tOptions Indexes FollowSymLinks ExecCGI\n	AddHandler wsgi-script .wsgi@' \
	       $(MYAPACHE_HOME)/etc/apache2/apache2.conf
	sed -i -e 's@wsgi_module /usr/@wsgi_module $(MYAPACHE_HOME)/usr/@' \
	       $(MYAPACHE_HOME)/etc/apache2/mods-available/wsgi.load
	sed -i -e 's@#WSGISocketPrefix /var/run/apache2/wsgi@WSGISocketPrefix $(MYAPACHE_HOME)/var/run/apache2/wsgi@' \
	       $(MYAPACHE_HOME)/etc/apache2/mods-available/wsgi.conf
	touch $(MYAPACHE_HOME)/setup.done

$(MYAPACHE_HOME)/setup.done: setupapache

$(MYAPACHE_HOME)/usr/lib/apache2/modules/mod_wsgi.so: mod_wsgi.tar.gz
	-mkdir -p $(MYAPACHE_HOME)/
	tar --directory $(MYAPACHE_HOME)/ -zxvf mod_wsgi.tar.gz

mod_wsgi.tar.gz:
	tar zcvf mod_wsgi.tar.gz /usr/lib/apache2/modules/mod_wsgi.so \
	    /usr/lib/apache2/modules/mod_wsgi.so-2.7 \
	    /etc/apache2/mods-enabled/wsgi.load \
	    /etc/apache2/mods-enabled/wsgi.conf \
	    /etc/apache2/mods-available/wsgi.load \
	    /etc/apache2/mods-available/wsgi.conf 
	       
startapache: $(MYAPACHE_HOME)/setup.done
	APACHE_CONFDIR=$(MYAPACHE_HOME)/etc/apache2 apachectl -f $(MYAPACHE_HOME)/etc/apache2/apache2.conf -k start

stopapache:  	
	APACHE_CONFDIR=$(MYAPACHE_HOME)/etc/apache2 apachectl -f $(MYAPACHE_HOME)/etc/apache2/apache2.conf -k stop

restartapache:  	
	APACHE_CONFDIR=$(MYAPACHE_HOME)/etc/apache2 apachectl -f $(MYAPACHE_HOME)/etc/apache2/apache2.conf -k restart

