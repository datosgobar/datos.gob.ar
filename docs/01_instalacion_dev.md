

# Tutorial de instalacion de CKAN

## Requerimientos de Sistema
Sistema Operativo: Ubuntu Server 14 o 15

GB: [TODO]

Disco: [TODO]

## Instalacion de CKAN
Basado en este tutorial:
http://docs.ckan.org/en/latest/maintaining/installing/install-from-source.html

1\. Instalar paquetes necesarios
```
sudo apt-get update
sudo apt-get install python-dev postgresql libpq-dev python-pip python-virtualenv git-core solr-jetty openjdk-6-jdk
```

2\. Instalar CKAN en un entorno virtual de python

2.a. Create a Python virtual environment (virtualenv) to install CKAN into, and activate it:
```
sudo mkdir -p /usr/lib/ckan/default
sudo chown `whoami` /usr/lib/ckan/default
virtualenv --no-site-packages /usr/lib/ckan/default
. /usr/lib/ckan/default/bin/activate
```

2.b Instalar codigo de CKAN en el virtualenv. Para instalar la ultima version estable de CKAN (CKAN 2.5.1), correr:
```
pip install -e 'git+https://github.com/ckan/ckan.git@ckan-2.5.1#egg=ckan'
```
(Esto tarda un rato)

2.c Instalar modulos de python que requiere CKAN en el virtualenv:
```
pip install -r /usr/lib/ckan/default/src/ckan/requirements.txt
```

2.d Desactivar y reactivar el virtualenv, para asergurarse de que se estan usando las versiones del virtualenv de comandos como paster en lugar de los nativos del sistema.
```
deactivate
. /usr/lib/ckan/default/bin/activate
```

3\. Setupear la base de datos PostgreSQL. Para este ejemplo se creo un usuario con estas credenciales: ckan_default:pass
```
sudo -u postgres psql -l
sudo -u postgres createuser -S -D -R -P ckan_default
sudo -u postgres createdb -O ckan_default ckan_default -E utf-8
```

4\. Crear archivo de configuracion de CKAN
```
sudo mkdir -p /etc/ckan/default
sudo chown -R `whoami` /etc/ckan/
paster make-config ckan /etc/ckan/default/development.ini
```

Editar /etc/ckan/default/development.ini:
Asumo que el user y pass es ckan_default:ckan y la db es ckan_default
```
sqlalchemy.url = postgresql://ckan_default:ckan@localhost/ckan_default
```

Cada CKAN site should have a unique site_id, for example (esto no es necesario):
```
ckan.site_id = default
```

Configurar la URL del sitio (esto se usa para poner los links al FileStore, notificaciones, emails etc). Por ejemplo:
```
ckan.site_url = http://127.0.0.1:5000
```

5\. Setup de Solr
Actualmente el paquete de solr-jetty esta roto asi que conviene usar solr-tomcat

5.1.A. Setup del servicio HTTP jetty
5.1.A.1 Instalar paquete
```
sudo apt-get install solr-jetty
```

5.1.A.2 Editar el archivo de configuracion de Jetty (/etc/default/jetty) y cambiar las siguientes variables:
```
[..]
NO_START=0            # (linea 4)
JETTY_HOST=127.0.0.1  # (linea 16)
JETTY_PORT=8983       # (linea 19)
[..]
```

5.1.B. Setup con tomcat
5.1.B.1 Instalar paquetes
```
sudo apt-get install solr-tomcat
```

5.1.B.2 Configurar de puerto de tomcat
/etc/tomcat6/server.xml
```
[..]
    -->
    <Connector port="8983" protocol="HTTP/1.1" 
               connectionTimeout="20000" 
               URIEncoding="UTF-8"
               redirectPort="8443" />
[..]
```


5.2.1 Reemplazar archivo schema.xml default por un symlink al archivo de schema CKAN incluido en las fuentes.
```
sudo mv /etc/solr/conf/schema.xml /etc/solr/conf/schema.xml.bak
sudo ln -s /usr/lib/ckan/default/src/ckan/ckan/config/solr/schema.xml /etc/solr/conf/schema.xml
```

5.2.2 Reiniciar el servicio
```
#sudo service jetty restart
sudo service tomcat6 restart
```

5.3. Finalmente cambiar la opcion solr_url en el archivo de configuracion de CKAN para que apunte al server Solr, por ejemplo:
```
solr_url=http://127.0.0.1:8983/solr
```

6\. Crear tablas de la base de datos
```
cd /usr/lib/ckan/default/src/ckan
paster db init -c /etc/ckan/default/development.ini
# Despues de un rato deberia aparecer este mensajes: "Initialising DB: SUCCESS"
```

8\. Crear link a who.ini
```
ln -s /usr/lib/ckan/default/src/ckan/who.ini /etc/ckan/default/who.ini
```

9\. Listo!
```
cd /usr/lib/ckan/default/src/ckan
paster serve /etc/ckan/default/development.ini
```

En este punto ya se puede acceder al CKAN a traves de http://127.0.0.1:5000/


# Otras tareas

1\. Crear usuario sysadmin. ckan_admin:pass
```
. /usr/lib/ckan/default/bin/activate
cd /usr/lib/ckan/default/src/ckan
paster sysadmin add ckan_admin -c /etc/ckan/default/development.ini
```

2\. Create data de prueba
```
paster create-test-data -c /etc/ckan/default/development.ini
paster create-test-data search -c /etc/ckan/default/development.ini
paster create-test-data gov -c /etc/ckan/default/development.ini
paster create-test-data family -c /etc/ckan/default/development.ini
paster create-test-data translations -c /etc/ckan/default/development.ini
paster create-test-data vocab -c /etc/ckan/default/development.ini
paster create-test-data hierarchy -c /etc/ckan/default/development.ini
# paster create-test-data -c /etc/ckan/default/production.ini
# paster create-test-data --help
```

###############################################################################

# Setup de plugins
## Set up the DataStore
Ver: http://docs.ckan.org/en/latest/maintaining/datastore.html

1\. Habiltiar plugin de datastore. En /etc/ckan/default/development.ini
```
ckan.plugins = stats text_view image_view recline_view
ckan.plugins = stats text_view image_view recline_view datastore
```

2\. Setup de la base de datos. En este ejemplo se creo este usuario: datastore_default:pass
```
sudo -u postgres createuser -S -D -R -P -l datastore_default
sudo -u postgres createdb -O ckan_default datastore_default -E utf-8
```

3\. Configurar URLs. En /etc/ckan/default/development.ini
```
ckan.datastore.write_url = postgresql://ckan_default:pass@localhost/datastore_default
ckan.datastore.read_url = postgresql://datastore_default:pass@localhost/datastore_default
```
 
4\. Configurar permisos
```
paster --plugin=ckan datastore set-permissions -c /etc/ckan/default/development.ini | sudo -u postgres psql --set ON_ERROR_STOP=1
```

5\. Reiniciar CKAN

6\. Testeando que todo funciona
Este comando deberia retornar un json como el que sigue :
```
curl -X GET "http://127.0.0.1:5000/api/3/action/datastore_search?resource_id=_table_metadata"
```

```
{"help": "http://localhost/api/3/action/help_show?name=datastore_search", "success": true, "result": {"resource_id": "_table_metadata", "fields": [{"type": "text", "id": "_id"}, {"type": "name", "id": "name"}, {"type": "oid", "id": "oid"}, {"type": "name", "id": "alias_of"}], "records": [{"_id": "1fab8662e5772995", "alias_of": "pg_views", "name": "_table_metadata", "oid": 70605}, {"_id": "21b5fe766665b205", "alias_of": "pg_tables", "name": "_table_metadata", "oid": 70605}], "_links": {"start": "/api/3/action/datastore_search?resource_id=_table_metadata", "next": "/api/3/action/datastore_search?offset=100&resource_id=_table_metadata"}, "total": 2}}
```

### Habilitar vista de datos del datastore
```
ckan.plugins = recline_grid_view [...] # Puede haber otros plugins
ckan.views.default_views = recline_grid_view [...] # Puede haber otros plugins
```

## Setup de FileStore (Esto se usa para cargar CSVs)
Ver http://docs.ckan.org/en/latest/maintaining/filestore.html

1\. Crear el directorio donde el CKAN va a subir los archivos:
```
sudo mkdir -p /var/lib/ckan/default
```

2\. Agregar la siguiente linea al archivo de documentacion de CKAN en la seccion [app:main]:
```
ckan.storage_path = /var/lib/ckan/default
```

3\. Configurar los permisos para el directorio indicado en ckan.storage_path. (Poner el usuario que corresponde en lugar de www-data)
```
sudo chown www-data /var/lib/ckan/default
sudo chmod u+rwx /var/lib/ckan/default
```

4\. Reiniciar el web server
```
paster serve /etc/ckan/default/development.ini
```

## Setup del DataPusher
Ver:
- http://docs.ckan.org/projects/datapusher/en/latest/
- http://docs.ckan.org/projects/datapusher/en/latest/development.html

1\. Instalar los paquetes necesarios:
```
sudo apt-get install python-dev python-virtualenv build-essential libxslt1-dev libxml2-dev git
```

2\. Configurar el entorno:
```
sudo mkdir -p /usr/lib/ckan/datapusher
sudo chown `whoami` /usr/lib/ckan/datapusher
virtualenv --no-site-packages /usr/lib/ckan/datapusher
. /usr/lib/ckan/datapusher/bin/activate
cd /usr/lib/ckan/datapusher
```

3\. Get the code:
```
git clone https://github.com/ckan/datapusher
cd datapusher
```

4\. Instalar las dependencias:
```
pip install -r requirements.txt
pip install -e .
```

5\. Correr el DataPusher:
```
python datapusher/main.py deployment/datapusher_settings.py
```

7\. Por default el DataPusher should be running at the following port:
http://localhost:8800/

8\. Configurar CKAN. /etc/ckan/default/development.ini
```
ckan.plugins = datapusher [...] # Agregar a los plugins ya existentes
ckan.datapusher.formats = csv xls xlsx tsv application/csv application/vnd.ms-excel application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
ckan.datapusher.url = http://127.0.0.1:8800/
```

9\. Reiniciar CKAN

###############################################################################
# Testeando que todo funciona
Ver http://docs.ckan.org/en/latest/contributing/test.html

1\. Instalar dependencias
```
. /usr/lib/ckan/default/bin/activate
pip install -r /usr/lib/ckan/default/src/ckan/dev-requirements.txt
```

2\. Setup db de pruebas
```
cd /usr/lib/ckan/default/src/ckan/
sudo -u postgres createdb -O ckan_default ckan_test -E utf-8
sudo -u postgres createdb -O ckan_default datastore_test -E utf-8
#paster datastore set-permissions -c test-core.ini | sudo -u postgres psql
paster --plugin=ckan datastore set-permissions -c test-core.ini | sudo -u postgres psql
```

3\. Correr tests
```
nosetests --ckan --reset-db --with-pylons=test-core.ini ckan
```

Despues de media hora mas o menos deberia verse un output como el siguiente:
```
Ran 1922 tests in 1747.069s
OK (SKIP=12)
```

###############################################################################
# Cargar un CSV estatico
Para que esto funcione tambien es necesario que los plugins datastore y datapusher esten operativos.

Antes de empezar con esto conviene habilitar la vista de datos del datastore ademas de tener instalado dicho plugin.
Caso contrario CKAN intenta usar un servicio externo para convertir la data en crudo del CSV en algo qyue puede mostrar.
Esto puede fallar si el sitio no tiene un IP visible desde afuera. (Quien diseño esto???)

Ahora si, para cargar un CSV a traves de la UI hay que seguir estos pasos:

1\. Una vez logueado ir a la pagina de datasets
http://127.0.0.1:5000/dataset
Hacer click en "Add new"

2\. Completar la informacion pertinente y hacer click en el boton "Next: Add Data" situado abajo.

3\. Alli cargar el csv objetivo.
Aca se puede usar un dataset como este:
http://data.buenosaires.gob.ar/dataset/areas-de-proteccion-historica/resource/46fa522d-7696-4903-ba69-175dde668501

4\. Ir al tab "DataStore". Confirmar que la fila "Status" tiene valor "Complete" en lugar de pending.
En este punto va a haber bastante ouput por el las shells donde se estan corriendo el CKAN y data pusher.
Puede que aparezcan excepciones de python pero al parecer los datos se cargan de todas formas.

5\. Ir al tab "Views". Alli hacer click en "New view" > "Grid"

6\. En este punto ya deberia ser posible acceder al recurso a traves de la UI y ver una tabla con los datos.

###############################################################################
## Customizando UX de CKAN
Ver:
- http://docs.ckan.org/en/latest/theming/index.html
- http://docs.ckan.org/en/latest/theming/templates.html
- http://docs.ckan.org/en/847-new-theming-docs/theming/fanstatic.html
