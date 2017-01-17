# [datos.gob.ar](http://datos.gob.ar/)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [datos.gob.ar](#datosgobar)
  - [Instalación](#instalaci%C3%B3n)
  - [Desarrollo](#desarrollo)
  - [Créditos](#cr%C3%A9ditos)
  - [Contacto](#contacto)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Repositorio del Portal de Datos de la República Argentina

## Instalación

Para tener una instancia corriendo se necesita
* Instalar una instancia local de CKAN. Seguir [este doc](./docs/01_instalacion_dev.md) (solo para instalacion bajo debian/ubuntu)
* Instalar CKAN con Servidor WA separado del server de DB. Seguir [este doc](./docs/install_ckan_rhel_centos.md) (solo para instalacion bajo RHEL7/CentOS6.3)
* Instalar el tema visual y sus dependencias, siguiendo [este doc](./docs/03_instalacion_tema_visual.md)

## Desarrollo

El principal desarrollo de este proyecto se encuentra en la carpeta [gobar_theme](./ckanext/gobar_theme).
Si se desea modificar el css de la web, modificar los archivos de sass y seguir las instrucciones dentro del archivo [style.scss](./ckanext/gobar_theme/styles/sass/style.scss) para compilar sass a css.

## Créditos

Este proyecto está basado en [CKAN](https://github.com/ckan/ckan) y en la [guia para crear extensiones](http://docs.ckan.org/en/latest/extensions/tutorial.html).

## Contacto

Te invitamos a [creanos un issue](https://github.com/datosgobar/datos.gob.ar/issues/new?title=Encontre un bug en datos.gob.ar) en caso de que encuentres algún bug o tengas feedback de alguna parte de `datos.gob.ar`.

Para todo lo demás, podés mandarnos tu comentario o consulta a [datos@modernizacion.gob.ar](mailto:datos@modernizacion.gob.ar).
