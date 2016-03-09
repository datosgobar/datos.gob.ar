Customizacion de CKAN mediante plugins
======================================

## Creacion de un plugin nuevo

1\. Usar las el comando "paster create" para crear una extension vacia
```bash
. /usr/lib/ckan/default/bin/activate
cd /usr/lib/ckan/default/src
paster --plugin=ckan create -t ckanext ckanext-gobar_testtheme
```

2\. Crear el archivo "ckanext-gobar_testtheme/ckanext/gobar_testtheme/plugin.py" con el siguiente contenido si no existe:
```python
import ckan.plugins as plugins

class Gobar_TestthemePlugin(plugins.SingletonPlugin):
    pass
```
e
3\. Editar la veriablec entry_points en ckanext-gobar_testtheme/setup.py para que quede de esta manera:
```python
entry_points='''
    [ckan.plugins]
    gobar_testtheme=ckanext.gobar_testtheme.plugin:Gobar_TestthemePlugin
```

4\. Run python setup.py develop:
```bash
cd ckanext-gobar_testtheme
python setup.py develop
```

5\. Agregar el plugin al setting ckan.plugins en /etc/ckan/default/development.ini:
```
ckan.plugins = stats text_view recline_view gobar_testtheme [...]
```

6\. Arrancar el servidor de desarrollo de CKAN:
```bash
paster serve --reload /etc/ckan/default/development.ini
```

## Customizando templates
Para este ejemplo vamos a modificar el texto de la seccion about.
Lo primero que uno consideraria para hacer esto basarse ./ckan/ckan/templates/home/index.html
Pero revisando dicho archivo entrontramos esta linea:
```python
[...]
          {% snippet 'home/snippets/about_text.html' %}
[...]
```

Revisando este archivo vemos que es alli donde esta el texto que quemos alterar.

1\. Crear el directorio donde va esta el template que sequiere pisar:
```bash
mkdir -p ./ckanext-gobar_testtheme/ckanext/gobar_testtheme/templates/home/snippets
```

2\. Crear el archivo ./ckanext-gobar_testtheme/ckanext/gobar_testtheme/templates/home/snippets/about_text.html y agregarle este contenido:
```jinja2
{% trans %}
<p>Esta es una prueba de customizacion de CKAN</p>
{% endtrans %}
```

En este punto se pude acceder a http://127.0.0.1:5000/about para revisar si el cambio se produjo exitosamente.


## Customizacion de estilos CSS
En este eje

1\. Crear el directorio donde va a estar guardado el CSS que queremos agregar
```bash
mkdir -p ./ckanext-gobar_testtheme/ckanext/gobar_testtheme/public/
```

2\. Crear el archivo ./ckanext-gobar_testtheme/ckanext/gobar_testtheme/public/gobar_testtheme.css

Contenido de ejemplo:
```css
.account-masthead {
    background-color: #ffffff;
}

.masthead {
    min-height: 55px;
    color: #ffffff;
    background: #75AADB url("../../../base/images/bg.png");
}

.account-masthead .account ul li a {
    display: block;
    color: #2A3D42;
    font-size: 13px;
    font-weight: bold;
    padding: 0 10px;
    line-height: 31px;
}
```

3\. Asegurarse de que se use el css recien creado.
Para esto hay que crear el archivo ./ckanext-gobar_testtheme/ckanext/gobar_testtheme/templates/base.html con el siguiente contenido:

```jinja2
{% ckan_extends %}
{% block styles %}
  {{ super() }}
  <link rel="stylesheet" href="/gobar_testtheme.css" />
{% endblock %}
```

Yendo linea por linea tenemos lo siguiente:
1) Se indica a jinja2 que se desea extender el template original en lugar de sobrescribirlo
```jinja2
{% ckan_extends %}
'''

2) Indico el bloque que quiero reemplazas
```jinja2
{% block styles %}
[...]
{% endblock %}
```

3) Con esta llamada a super funcion inserto en contenido del bloque "styles" original:
```jinja2
{{ super() }}
```

4) Agrego la referencia al archivo nuevo css.
```
<link rel="stylesheet" href="/gobar_testtheme.css" />
```

Param as informacion ver:
- http://docs.ckan.org/en/latest/theming/templates.html#extending-templates-with-ckan-extends
- http://docs.ckan.org/en/latest/theming/templates.html#extending-parent-blocks-with-jinja-s-super


## Agregar una nueva pagina

En este ejemplo vamos a agregar una nueva pagina dinamica que contara con dos urls distintas.
La primera sera http://127.0.0.1/gobar y la segunda http://127.0.0.1/gobar_page/{texto}
Donde {texto} sera una variable recibira el controlador de la pagina para luego ser mostrada al usuario.

1\. Implementar la interfaz de manejo de rutas 
Hacemos esto agregando las siguientes lineas a la clase Gobar_TestthemePlugin en plugin.py
```python
[...]
    plugins.implements(plugins.IRoutes, inherit=True)

    def before_map(self, map):
        controller = 'ckanext.gobar_testtheme.plugin:GobarController'
        map.connect('gobar_page', '/gobar_page',
            controller=controller, action='index')
        map.connect('gobar_page', '/gobar_page/{testvar}',
            controller=controller, action='index')
        return map

    def after_map(self, map):
        return map
[...]
```


2\. Implementar el objeto de la clase PackageController que se encargara de atender los requests en el archivo plugin.py
```python
[...]
class GobarController(PackageController):
    def index(self, testvar="testvar default"):
        return base.render('home/gobar.html', extra_vars={"testvar":testvar})
[...]
```

3\. Creo el template de la pagina nueva./ckanext-gobar_testtheme/ckanext/gobar_testtheme/templates/home/gobar.html

```jinja2
{% extends "page.html" %}

{% block subtitle %}Pagina Nueva{% endblock %}

{% block primary %}
  <article class="module">
    <div class="module-content">
      <h1 class="page-heading">Pagina Nueva</h1>
      Contenido. Variable recibida: <strong>{{ testvar }}</strong>
    </div>
  </article>
{% endblock %}

{% block secondary %}{% endblock %}
```

Con todo esto listo ahora se puede acceder a la nueva pagina a traves de estas urls:
http://127.0.0.1/gobar_page
http://127.0.0.1/gobar_page/otro texto cualquiera

En el primer caso vamos a ver el texto "testvar default" en negrita en tanto que en el segundo aparecera "otro texto cualquiera"


## Agregar un nuevo helper al template:

1\. Implementamos interfaz ITemplateHelpers
Para esto vamos a implementar el siguiente codigo a la clase :
```python
[...]
    plugins.implements(plugins.ITemplateHelpers)

    def get_helpers(self):
        return { 'gobar_helper_test': gobar_helper_test }
[...]
```

2\. Imeplementar el helper
```python
def gobar_helper_test():
    return { "content" : "This is gobar_helper_test_function" } 
```

3\. Modificar gobar.html agregando esta linea:
```jinja2
[...]
      Contenido de generado por gobar_helper_test: <strong>{{ h.gobar_helper_test() }}</strong><br>
[...]
```

Hecho esto cuando se acceda a http://127.0.0.1/gobar_page se deberia ver el siguiente texto:
```jinja2
[...]
Contenido de generado por gobar_helper_test: {'content': 'This is gobar_helper_test_function'}
[...]
```

## Documentacion util

Doc general sobre customizacion de CKAN:
http://docs.ckan.org/en/latest/theming/index.html

Doc sobre las interfaces que pueden implementar los plugins de CKAN para modificar o extender su funcionalidad:
http://docs.ckan.org/en/latest/extensions/plugin-interfaces.html

Otras extensiones disponibles de CKAN:
https://github.com/ckan/ckan/wiki/List-of-extensions
