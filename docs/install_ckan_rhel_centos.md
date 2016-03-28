- [Topologia actual de webapp ** CKAN **](#topologia-actual-de-webapp-ckan-)
  - [Tareas a realizar dentro del servidor de la webapp](#tareas-a-realizar-dentro-del-servidor-de-la-webapp)
    - [Instalar EPEL (Extra Packages for Enterprise Linux)](#instalar-epel-extra-packages-for-enterprise-linux)
    - [instalar paquetes requeridos mediante el comando "yum"](#instalar-paquetes-requeridos-mediante-el-comando-yum)
  - [Crear y Activar un entorno virtual dentro del que "correra" CKAN](#crear-y-activar-un-entorno-virtual-dentro-del-que-correra-ckan)
  - [Instalar CKAN 2.5 en el virtualenv](#instalar-ckan-25-en-el-virtualenv)
  - [Crear una configuracion para CKAN](#crear-una-configuracion-para-ckan)
  - [Customizar development.ini](#customizar-developmentini)
  - [Inicializar Base de Datos de CKAN](#inicializar-base-de-datos-de-ckan)
  - [Crear link a who.ini](#crear-link-a-whoini)
- [Correr por primera vez CKAN](#correr-por-primera-vez-ckan)
  - [Crear usuario Administrador para CKAN](#crear-usuario-administrador-para-ckan)
  - [Tareas a realizar dentro del servidor de la base de datos.](#tareas-a-realizar-dentro-del-servidor-de-la-base-de-datos)
    - [Instalacion y configuracion de servidor Postgres:](#instalacion-y-configuracion-de-servidor-postgres)
    - [Activar el inicio de postgres en el arranque del OS.](#activar-el-inicio-de-postgres-en-el-arranque-del-os)
    - [Inicializar base de datos PostgreSQL](#inicializar-base-de-datos-postgresql)
    - [Modificar el archivo <code>pg_hba.conf</code>, deberia quedar de la siguiente manera:](#modificar-el-archivo-codepghbaconfcode-deberia-quedar-de-la-siguiente-manera)
    - [Iniciar el postgres como servicio](#iniciar-el-postgres-como-servicio)
    - [Crear base de datos <code>default</code> y un usuario para CKAN](#crear-base-de-datos-codedefaultcode-y-un-usuario-para-ckan)
    - [Instalación y configuración de Apache Tomcat 6 + SOLR 1.4.1.](#instalacin-y-configuracin-de-apache-tomcat-6-solr-141)
    - [Instalar tomcat6 y java6](#instalar-tomcat6-y-java6)
    - [Chequear que la versión de java por default sea la 1.6:](#chequear-que-la-versin-de-java-por-default-sea-la-16)
    - [Bajar y descomprimir solr en /opt:](#bajar-y-descomprimir-solr-en-opt)
    - [Crear los directorios:](#crear-los-directorios)
    - [Copiar la estructura multicore y los archivos de conf en cada core:](#copiar-la-estructura-multicore-y-los-archivos-de-conf-en-cada-core)
    - [Modificar solrconfig.xml de los cores:](#modificar-solrconfigxml-de-los-cores)
    - [Borrar archivos innecesarios:](#borrar-archivos-innecesarios)
    - [Modificar /usr/share/solr/solr.xml:](#modificar-usrsharesolrsolrxml)
  - [Setear permisos:](#setear-permisos)
  - [Copiar solr.war para tomcat:](#copiar-solrwar-para-tomcat)
  - [Crear xml de solr para tomcat:](#crear-xml-de-solr-para-tomcat)
    - [Pegar al final del archivo:](#pegar-al-final-del-archivo)
  - [Reemplazar los archivos de esquema](#reemplazar-los-archivos-de-esquema)
  - [Levantar el servicio de Tomcat:](#levantar-el-servicio-de-tomcat)
  - [Autostart tomcat6](#autostart-tomcat6)
    - [Permisos para datastore:](#permisos-para-datastore)



## Topologia actual de webapp ** CKAN **

```
INTERNET +─────────────────────┐
                               │
                             ──┴──
                            Gateway &
                          vFirewall <──┐       
                            -----------┼----------┤VPN SS
                                       │
       ElasticWebApp <──--+  ┌─────────┴─────────┐     +--──> ElasticDB   
                             │                   │
                         ────┴────           ────┴────
                       WebApp: CKAN        DB Server: PGSQL
                       OS: RHEL 7.0          OS: RHEL 6.0
```

*Para la implementacion de la aplicacion <code>CKAN 2.5</code> en modo produccion, se propone tener instancias separadas entre webapp & database.
Por esta razon y a continuacion, se describen los pasos que se deben realizar en los diferentes servidores(webapp & db)*
### Tareas a realizar dentro del servidor de la webapp


#### Instalar EPEL (Extra Packages for Enterprise Linux)

    rpm -Uvh http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-7.noarch.rpm

#### instalar paquetes requeridos mediante el comando "yum"

    yum install xml-commons git subversion mercurial postgresql-server \
    postgresql-devel postgresql python-devel libxslt libxslt-devel libxml2 \
    libxml2-devel python-virtualenv gcc gcc-c++ make xalan-j2 unzip \
    policycoreutils-python mod_wsgi

*NOTA: los paquetes de postgresql, solo seran requeridos si la base de datos se encuentra dentro de la misma VM en la que vamos a instalaremos CKAN*


### Crear y Activar un entorno virtual dentro del que "correra" CKAN

    sudo mkdir -p /usr/lib/ckan/default
    sudo chown `whoami` /usr/lib/ckan/default
    virtualenv --no-site-packages /usr/lib/ckan/default
    . /usr/lib/ckan/default/bin/activate

### Instalar CKAN 2.5 en el virtualenv
*Es importante que chequear que el virtualenv esta activado, antes de ejecutar el comando de pip.
tomara un par de minutos dependiendo de la velocidad transferencia con la que se cuente.*

    pip install -e 'git+https://github.com/ckan/ckan.git@ckan-2.5.1#egg=ckan'

*Asi mismo, incluiremos los <code>requirements</code> a la instalacion*

      pip install -r /usr/lib/ckan/default/src/ckan/requirements.txt

### Crear una configuracion para CKAN
*Inicialmente, la llamaremos <code>development.ini</code>, es recomendable, luego, remplazarlo por uno similar llamado <code>produccion.ini</code>*

    sudo mkdir -p /etc/ckan/default
    sudo chown -R `whoami` /etc/ckan/
    paster make-config ckan /etc/ckan/default/development.ini


### Customizar development.ini
*Vamos a realizar varias configuraciones, es importante aclarar que estas configuraciones son solo validas para el modo **desarrollo***

```python
ckan.site_id = default
sqlalchemy.url = postgresql://ckan_postgres_user:ckan_postgres_user_pass@tu_db_ip/ckan_default #REMPLAZAR ckan_postgres_user, ckan_postgres_user_pass y tu_db_ip, por lo que corresponda.
ckan.site_url = http://XXX.XXX.XXX.XXX:5000 #IP de la maquina donde se esta instalando CKAN
solr_url=http://XXX.XXX.XXX.XXX:PPPP/solr #IP y puerto del servidor donde este instalado Solr
```


### Inicializar Base de Datos de CKAN
*Si todo esta configurado correctamente, luego de unos momentos leera **"Initialising DB: SUCCESS"***

    cd /usr/lib/ckan/default/src/ckan
    paster db init -c /etc/ckan/default/development.ini

### Crear link a who.ini

    ln -s /usr/lib/ckan/default/src/ckan/who.ini /etc/ckan/default/who.ini

# Correr por primera vez CKAN

    cd /usr/lib/ckan/default/src/ckan
    paster serve /etc/ckan/default/[tu_configuracion_actual].ini

*Nota: para corroborar que efectivamente ckan esta funcionando, ir a la url que declaramos dentro de development.ini, en el campo: **ckan.site_url***

### Crear usuario Administrador para CKAN

    . /usr/lib/ckan/default/bin/activate
    cd /usr/lib/ckan/default/src/ckan
    paster sysadmin add ckan_admin -c /etc/ckan/default/development.ini

---

### Tareas a realizar dentro del servidor de la base de datos.
#### Instalacion y configuracion de servidor Postgres:

    sudo yum -y install postgresql-server postgresql-devel postgresql

#### Activar el inicio de postgres en el arranque del OS.

      sudo chkconfig postgresql on

#### Inicializar base de datos PostgreSQL

    sudo service postgresql initdb

#### Modificar el archivo <code>pg_hba.conf</code>, deberia quedar de la siguiente manera:

    sudo nano /etc/postgresql/[tu_version_de_postgres]/main/pg_hba.conf

```bash
local   all         postgres                          ident
local   all         all                               md5
# IPv4 local connections:
host    all         ckan_default_user  192.168.1.2/32 ident
# IPv6 local connections:
host    all         all         ::1/128               md5
```

#### Iniciar el postgres como servicio

     sudo service postgresql start

#### Crear base de datos <code>default</code> y un usuario para CKAN

*Para nuestro caso particular vamos a llamar al usuario:  <code>ckan_default_user</code> y <code>ckan_default_db</code> a la base de datos.*

    su - postgres
    createdb -O ckan_default_user ckan_default_db
    createuser -S -D -R -P ckan_default_user
    exit



*es posible que se requiera crear una regla en <code>/etc/sysconfig/iptables</code>
para esto otorgarle permisos a cruzar el firewall a postgreas.*

    sudo vim /etc/sysconfig/iptables

*Agregar la siguiente linea al final del archivo iptables:*

<code>-A INPUT -m state --state NEW -m tcp -p tcp --dport 5432 -j ACCEPT</code>

*Reiniciar el servicio iptables:*

    /etc/init.d/iptables restart

*Asi mismo, es posible que requiera configurar las direcciones que "escucha" PostgreSQL, para ello vamos a hacer una pequeña modificacion a el archivo de configuracion general de PG*

    sudo nano /etc/postgresql/[tu_version_de_postgres]/main/postgresql.conf

*Debemos cambiar el parametro de configuracion <code>listen_addresses</code> y deberia quedarnos de la siguiente manera:*

```bash
#------------------------------------------------------------------------------
# CONNECTIONS AND AUTHENTICATION
#------------------------------------------------------------------------------

# - Connection Settings -
listen_addresses = '*'                  # what IP address(es) to listen on;
                                        # comma-separated list of addresses;
                                        # defaults to 'localhost'; use '*' for all
```

*Nota: por omision, el parametro **listen_addresses** se encuentra cometado y apuntando solo a **localhost***.

*Para chequear que efectivamente este funcionando la regla de iptables, podemos usar:*

    netstat -tulpn | less


---

#### Instalación y configuración de Apache Tomcat 6 + SOLR 1.4.1.
 *En arquitectura multicore con esquemas para CKAN 1.4 y 2.3 (OS:RHEL 6)*

#### Instalar tomcat6 y java6
    sudo yum -y install tomcat6 tomcat6-webapps tomcat6-admin-webapps
    sudo yum -y install java-1.6.0-openjdk ava-1.6.0-openjdk-devel

#### Chequear que la versión de java por default sea la 1.6:
    alternatives --config java # Seleccionar el OpenJDK 6
    java -version # Deberia mostrar la opcion configurada en el paso anterior

#### Bajar y descomprimir solr en /opt:
    cd /opt
    wget http://archive.apache.org/dist/lucene/solr/1.4.1/apache-solr-1.4.1.tgz
    tar xzvf apache-solr-1.4.1.tgz

#### Crear los directorios:
    mkdir -p /usr/share/solr/
    mkdir -p /var/lib/solr/data/

* *Opcional pero prolijo: <code>ln -s /usr/share/solr /etc/solr</code>*

#### Copiar la estructura multicore y los archivos de conf en cada core:
    cp -r /opt/apache-solr-1.4.1/example/multicore/* /usr/share/solr/
    cp -nr /opt/apache-solr-1.4.1/example/solr/* /usr/share/solr/core0
    cp -nr /opt/apache-solr-1.4.1/example/solr/* /usr/share/solr/core1

#### Modificar solrconfig.xml de los cores:
    vim /usr/share/solr/core0/conf/solrconfig.xml
    vim /usr/share/solr/core1/conf/solrconfig.xml


* *Se agrega entre los tags "config" lo siguiente:*
```xml
<config>
  ...
    <dataDir>${dataDir}</dataDir>
  ...
</config>
```

#### Borrar archivos innecesarios:
    rm -rf /usr/share/solr/exampledocs/

#### Modificar /usr/share/solr/solr.xml:
    vim /usr/share/solr/solr.xml

** Dejar solo la siguiente sentencia **

```xml
<solr persistent="true" sharedLib="lib">
  <cores adminPath="/admin/cores">
    <core name="ckan-schema-1.4" instanceDir="core0">
    <property name="dataDir" value="/var/lib/solr/data/core0" />
    </core>
    <core name="ckan-schema-2.3" instanceDir="core1">
    <property name="dataDir" value="/var/lib/solr/data/core1" />
    </core>
  </cores>
</solr>
```

### Setear permisos:
    chown -R tomcat:tomcat /usr/share/solr/
    chown -R tomcat:tomcat /var/lib/solr/


### Copiar solr.war para tomcat:
    cp /opt/apache-solr-1.4.1/dist/apache-solr-1.4.1.war /usr/share/solr/apache-solr-1.4.1.war


### Crear xml de solr para tomcat:
    vim /usr/share/tomcat6/conf/Catalina/localhost/solr.xml


#### Pegar al final del archivo:
```xml
    <Context docBase="/usr/share/solr/apache-solr-1.4.1.war" debug="0" privileged="true" allowLinking="true" crossContext="true">
       <Environment name="solr/home" type="java.lang.String" value="/usr/share/solr" override="true" />
    </Context>
```

### Reemplazar los archivos de esquema
 *<code>/usr/share/solr/core0/conf/schema.xml</code> y <code>/usr/share/solr/core1/conf/schema.xml</code> por los de CKAN 1.4 y 2.0 respectivamente*


    cp schema-1.4.xml /usr/share/solr/core0/conf/schema.xml
    cp schema-2.0.xml /usr/share/solr/core1/conf/schema.xml


### Levantar el servicio de Tomcat:
    service tomcat6 start


### Autostart tomcat6
    chkconfig tomcat6 on
---


#### Permisos para datastore:
    sudo ckan datastore set-permissions | ssh dbserver sudo -u postgres psql --set ON_ERROR_STOP=1
*o si no se puede usar psql, simplemente, ejecutar:*

<code>sudo ckan datastore set-permissions</code>



*A esta altura ya solo nos quedaria instalar algunos plugins y modulos de ckan, para lo cual, es EXTREMADAMENTE recomendable, consultar la documentacion Oficial de CKAN*
