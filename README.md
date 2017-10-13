# [datos.gob.ar](http://datos.gob.ar/)

Repositorio de la extensión del Portal [datos.gob.ar](http://datos.gob.ar/) de la República Argentina para [CKAN](http://ckan.org/). Este proyecto se encarga de modificaciones al ruteo de la aplicación web, cambios visuales a la interfaz, y customización del portal, entre otros. Este repositorio *no* constituye el proyecto entero. El repositorio central del proyecto del Portal datos.gob.ar es [portal_datos.gob.ar](https://github.com/datosgobar/portal_datos.gob.ar)

- [Instalación](#instalaci%C3%B3n)
- [Desarrollo](#desarrollo)
- [Uso del theme](#uso-del-theme)
- [Créditos](#cr%C3%A9ditos)
- [Consultas sobre Andino](#consultas-sobre-andino)
- [Contacto](#contacto)

## Instalación

La instalación del paquete completo está disponible como un contenedor de Docker. Seguir las instrucciones del repositorio del [Portal datos.gob.ar](https://github.com/datosgobar/portal_datos.gob.ar) para levantar la instancia con Docker.

## Desarrollo

Como alternativa a la instalación dockerizada existe la posibilidad de tener una instalación contenida en un `virtualenv` del sistema. Esto se puede obtener siguiendo las instrucciones de [esta guia](http://docs.ckan.org/en/ckan-2.5.2/maintaining/installing/install-from-source.html). Una vez instalado el paquete a nivel sistema, es posible linkear el proceso principal a un debbuger de python (por ej pycharm). Este metodo no es recomendado para hacer modificaciones que impacten en el manejo del servidor por parte del wsgi de apache o nginx. Para dicho caso, es necesario tener una instalación de la aplicación dockerizada y acceder al contenedor del theme para realizar el desarrollo necesario.

Esta extensión de ckan fue desarrollada siguiendo la [guia de creación de extensiones](http://docs.ckan.org/en/ckan-2.5.2/extensions/tutorial.html).

### Estructura de archivos

```
- ckanext
    - gobar_theme
        - js
            - archivos de js a ser importados por los distintos templates html
        - public
            - assets estáticos y públicos como imagenes y fuentes
        - styles
            - archivos css generados desde sus versiones de scss
        - templates
            - archivos de jinja renderizados por los controladores
        - actions.py # lógica de modelos de ckan, sobreescribe y/o extiende la lógica de ckan
        - controller.py # controladores para la home y la api, sobreescriben y/o extienden la lógica de ckan
        - helpers.py # metodos auxiliares para renderizado de templates
        - package_controller.py # controlador de lógica de datasets y recursos, sobreescribe y/o extiende la lógica de ckan
        - plugin.py # archivo que registra el repositorio como extensión de ckan y declara acciones, helpers y ruteo
        - routing.py # asociación de rutas a controladores y redireccionamientos, sobreescribe y/o extiende las de ckan
```

## Créditos

Este proyecto está basado en [CKAN](https://github.com/ckan/ckan) y en la [guia para crear extensiones](http://docs.ckan.org/en/latest/extensions/tutorial.html).

## Contacto

Te invitamos a [creanos un issue](https://github.com/datosgobar/datos.gob.ar/issues/new?title=Encontre%20un%20bug%20en%20datos.gob.ar) en caso de que encuentres algún bug o tengas feedback de alguna parte de `datos.gob.ar`.

Para todo lo demás, podés mandarnos tu comentario o consulta a [datos@modernizacion.gob.ar](mailto:datos@modernizacion.gob.ar).
