# ckanext-gobar_theme
Plugin para ckan con los seteos de la instancia del portal de datos de Argentina

## Instalacion
Suponiendo que la instancia de ckan está instalada en /usr/lib/ckan/default/src
```
$ . /usr/lib/ckan/default/bin/activate
(virtualenv) $ cd /usr/lib/ckan/default
(virtualenv) $ pip install -e "git+https://github.com/transparencia-argentina/ckanext-gobar_theme.git#egg=ckanext-gobar_theme"
```
Y agregar al archivo de configuracion de ckan (development.ini o production.ini) el plugin
```
ckan.plugins = (otros plugins) gobar_theme
```

## Configuracion
Dentro del archivo de configuracion de ckan (development.ini o production.ini)
```
ckan.auth.create_user_via_api = false
ckan.auth.create_user_via_web = false
```