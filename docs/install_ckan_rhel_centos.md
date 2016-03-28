== Install CentOS 6 ==
=== Perform a minimal installation of CentOS 6 ===
After rebooting, you can optionally add the ntp package for time syncronization.

 yum install ntp
 ntpdate -s pool.ntp.org
 chkconfig ntpd on
 service ntpd start

=== Install and activate the CentOS Continuous Release (CR) Repository ===

 yum install centos-release-cr

=== Update and reboot your system ===

 yum update
 shutdown -r now

=== Install and activate the Extra Packages for Enterprise Linux (EPEL) Repository ===

 rpm -Uvh http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-7.noarch.rpm

=== Install required packages ===

 yum install xml-commons git subversion mercurial postgresql-server postgresql-devel \
 postgresql python-devel libxslt libxslt-devel libxml2 libxml2-devel python-virtualenv \
 gcc gcc-c++ make java-1.6.0-openjdk-devel java-1.6.0-openjdk tomcat6 xalan-j2 unzip \
 policycoreutils-python mod_wsgi

== Configure PostgreSQL ==
=== Enable PostgreSQL to start on system boot ===

 chkconfig postgresql on

=== Initialize the PostgreSQL database ===

 service postgresql initdb

=== Modify pg_hba.conf ===
Edit <code>/var/lib/pgsql/data/pg_hba.conf</code> so it will accept passwords for login while still allowing the local <code>postgres</code> user to manage via <code>ident</code> login.  The relevant changes to <code>pg_hba.conf</code> are as follows:

 local	 all         postgres                          ident
 local   all         all                               md5
 # IPv4 local connections:
 host    all         all         127.0.0.1/32          md5
 # IPv6 local connections:
 host    all         all         ::1/128               md5

=== Start PostgreSQL ===
 service postgresql start

=== Create a database for CKAN ===
Become the <code>postgres</code> user.
 su - postgres
Create a PostgreSQL database user named <code>ckanuser</code> with a password of <code>pass</code>.
 $ createuser -S -D -R -P ckanuser
Create a PostgreSQL database named <code>ckantest</code> with <code>ckanuser</code> as the owner.
 $ createdb -O ckanuser ckantest
Exit the <code>postgres</code> user environment.
 $ exit

== Install CKAN ==
''**Note: In the following instructions, replace [DNS] with the actual DNS name of your machine, ex: demo.ckan.net''
=== Create a CKAN User ===
The <code>ckan</code> user is created with a shell of <code>/sbin/nologin</code> and a home directory of <code>/usr/local/[DNS]</code> to mirror what is shown in the [http://docs.ckan.org/en/latest/deployment.html CKAN Deployment] documentation.
 useradd -m -s /sbin/nologin -d /usr/local/[DNS] -c "CKAN User" ckan
Open the newly created directory up for read access so that the content will eventually be able to be served out via <code>httpd</code>.
 chmod 755 /usr/local/[DNS]
=== Adjust the SELinux file contexts ===
Modify the defaults and the current file context of the newly created directory such that it is able to be served out via <code>httpd</code>.
 semanage fcontext --add --ftype -- --type httpd_sys_content_t "/usr/local/[DNS](/.*)?"
 semanage fcontext --add --ftype -d --type httpd_sys_content_t "/usr/local/[DNS](/.*)?"
 restorecon -vR /usr/local/[DNS]
=== Download and install CKAN ===
Become the <code>ckan</code> user.
 su -s /bin/bash - ckan
Install an isolated Python environment, called <code>pyenv</code>, to host CKAN from.
 $ virtualenv pyenv
Activate the newly installed Python environment.
 $ . pyenv/bin/activate
Download and install version 2.0 of CKAN.
 (pyenv)$ pip install --ignore-installed -e git+https://github.com/okfn/ckan.git@ckan-2.0#egg=ckan
Download and install the necessary Python modules to run CKAN into the isolated Python environment.
 (pyenv)$ pip install --ignore-installed -r pyenv/src/ckan/pip-requirements.txt
Deactivate and then activate the isolated Python environment to start using the added modules.
 (pyenv)$ deactivate
 $ . pyenv/bin/activate
=== Initial CKAN Configuration ===
Change to the <code>pyenv/src/ckan</code> directory and create an initial configuration file.
 (pyenv)$ cd pyenv/src/ckan
 (pyenv)$ paster make-config ckan development.ini
Edit the newly created <code>development.ini</code> file, changing the following lines as indicated.
 host = [DNS]
 sqlalchemy.url = postgresql://ckanuser:pass@localhost/ckantest
 ckan.site_url = [DNS]
 ckan.site_id = [DNS]
 ckan.plugins = stats synchronous_search
 solr_url = http://127.0.0.1:8080/solr/ckan-schema-2.0
Exit from running as the <code>ckan</code> user.
 $ exit
== Install Apache SOLR ==
''CKAN can not use the latest version of Apache SOLR and requires version 1.4.1.''
=== Download and extract Apache SOLR ===
 curl http://archive.apache.org/dist/lucene/solr/1.4.1/apache-solr-1.4.1.tgz | tar xzf -
=== Configure Apache SOLR ===
Create directories to hold multiple SOLR cores.
 mkdir -p /usr/share/solr/core0 /usr/share/solr/core1 /var/lib/solr/data/core0 \
 /var/lib/solr/data/core1 /etc/solr/core0 /etc/solr/core1
Copy the Apache SOLR war to the desired location.
 cp apache-solr-1.4.1/dist/apache-solr-1.4.1.war /usr/share/solr
Copy the example Apache SOLR configuration to the core0 directory.
 cp -r apache-solr-1.4.1/example/solr/conf /etc/solr/core0
Edit the configuration file, <code>/etc/solr/core0/conf/solrconfig.xml</code>, as follows:
 <dataDir>${dataDir}</dataDir>
Copy the <code>core0</code> configuration to <code>core1</code>.
 cp -r /etc/solr/core0/conf /etc/solr/core1
Create a symbolic link between the configurations in <code>/etc</code> and <code>/usr</code>.
 ln -s /etc/solr/core0/conf /usr/share/solr/core0/conf
 ln -s /etc/solr/core1/conf /usr/share/solr/core1/conf
=== Add CKAN Schema to Apache SOLR ===
Remove the provided schema from the two configured cores and link the schema files in the CKAN source.
 rm -f /etc/solr/core0/conf/schema.xml
 ln -s /usr/local/[DNS]/pyenv/src/ckan/ckan/config/solr/schema-2.0.xml /etc/solr/core0/conf/schema.xml
 rm -f /etc/solr/core1/conf/schema.xml
 ln -s /usr/local/[DNS]/pyenv/src/ckan/ckan/config/solr/schema-1.4.xml /etc/solr/core1/conf/schema.xml
== Configure Tomcat 6 ==
=== Create Apache SOLR XML configuration files ===
Create a new file, called <code>/etc/tomcat6/Catalina/localhost/solr.xml</code>, with the following contents:
 <Context docBase="/usr/share/solr/apache-solr-1.4.1.war" debug="0" privileged="true" allowLinking="true" crossContext="true">
   <Environment name="solr/home" type="java.lang.String" value="/usr/share/solr" override="true" />
 </Context>
Create a new file, called <code>/usr/share/solr/solr.xml</code>, with the following contents:
 <solr persistent="true" sharedLib="lib">
     <cores adminPath="/admin/cores">
         <core name="ckan-schema-2.0" instanceDir="core0">
             <property name="dataDir" value="/var/lib/solr/data/core0" />
         </core>
         <core name="ckan-schema-1.4" instanceDir="core1">
             <property name="dataDir" value="/var/lib/solr/data/core1" />
         </core>
     </cores>
 </solr>
=== Set Permissions ===
Make <code>tomcat</code> the owner of the SOLR directories.
 chown -R tomcat:tomcat /usr/share/solr /var/lib/solr
=== Enable Tomcat 6 ===
Configure Tomcat 6 to start on system boot.
 chkconfig tomcat6 on
Start Tomcat 6.
 service tomcat6 start
== Final CKAN Configuration ==
''Now that Apache SOLR is being served via Tomcat 6, the final steps of the CKAN configuration can now be performed''
=== Initialize CKAN Database ===
Switch back to running as the <code>ckan</code> user, activate the isolated Python environment, and change to the CKAN source directory.
 su -s /bin/bash - ckan
 $ . pyenv/bin/activate
 (pyenv)$ cd pyenv/src/ckan
Initialize the CKAN database.
 (pyenv)$ paster --plugin=ckan db init
Add a user named <code>admin</code> to the CKAN database.
 (pyenv)$ paster --plugin=ckan user add admin --config=development.ini
Grant the <code>admin</code> user <code>sysadmin</code> rights.
 (pyenv)$ paster --plugin=ckan sysadmin add admin --config=development.ini
=== Configure CKAN for Deployment via httpd ===
Edit <code>/usr/local/[DNS]/pyenv/src/ckan/development.ini</code> and change its log location as follows:
 args = ("/var/log/ckan/[DNS]/ckan.log", "a", 20000000, 9)
Create a Python script called <code>/usr/local/[DNS]/pyenv/bin/[DNS].py</code> to run via <code>mod_wsgi</code> with the following contents:
 import os
 instance_dir = '/usr/local/[DNS]'
 config_file = '/usr/local/[DNS]/pyenv/src/ckan/development.ini'
 pyenv_bin_dir = os.path.join(instance_dir, 'pyenv', 'bin')
 activate_this = os.path.join(pyenv_bin_dir, 'activate_this.py')
 execfile(activate_this, dict(__file__=activate_this))
 from paste.deploy import loadapp
 config_filepath = os.path.join(instance_dir, config_file)
 from paste.script.util.logging_config import fileConfig
 fileConfig(config_filepath)
 application = loadapp('config:%s' % config_filepath)
Exit running as the <code>ckan</code> user.
 $ exit
Make the following directories and modify the permissions such that the <code>apache</code> user can write to them.
 mkdir -p /usr/local/[DNS]/pyenv/src/ckan/data /usr/local/[DNS]/pyenv/src/ckan/sstore /var/log/ckan/[DNS]
 chmod g+w /usr/local/[DNS]/pyenv/src/ckan/data /usr/local/[DNS]/pyenv/src/ckan/sstore /var/log/ckan/[DNS]
 chown apache:apache /usr/local/[DNS]/pyenv/src/ckan/data /usr/local/[DNS]/pyenv/src/ckan/sstore /var/log/ckan/[DNS]
== Configure httpd ==
=== Create Virtual Host ===
Edit the file <code>/etc/httpd/conf.d/wsgi.conf</code> and add the following contents:
 <VirtualHost *:80>
 	ServerName [DNS]
 	ServerAlias [DNS]
 	WSGIScriptAlias / /usr/local/[DNS]/pyenv/bin/[DNS].py
 	WSGIPassAuthorization On
 	ErrorLog /var/log/httpd/[DNS].log
 	CustomLog /var/log/httpd/[DNS].custom.log combined
 </VirtualHost>
=== Enable httpd to make network connections ===
 setsebool -P httpd_can_network_connect 1
=== Enable httpd to start on system boot ===
 chkconfig httpd on
=== Start httpd ===
 service httpd start
== Configure iptables ==
=== Enable port 80 ===
Edit the file <code>/etc/sysconfig/iptables</code> by inserting the following line near the middle of the file:
 -A INPUT -m state --state NEW -m tcp -p tcp --dport 80 -j ACCEPT
=== Restart iptables ===
 service iptables restart
== Connect to CKAN ==
Start your web browser and head to [DNS] and you should see CKAN running.  Login as the username <code>admin</code> as created previously.
