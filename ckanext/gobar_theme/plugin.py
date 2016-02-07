import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.plugins import implements, IRoutes


class Gobar_ThemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)

    # IConfigurer

    implements(IRoutes, inherit=True)

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('styles/css', 'gobar_css')
        toolkit.add_resource('js', 'gobar_js')

    def before_map(self, routing_map):

        gobar_home_controller = 'ckanext.gobar_theme.controller:GobArHomeController'
        routing_map.connect('/', controller=gobar_home_controller, action='index')

        routing_map.redirect('/about', '/acerca_del_sitio')
        routing_map.connect('gobar_acerca_de', '/acerca_del_sitio', controller=gobar_home_controller, action='about')
        routing_map.connect('gobar_terminos', '/terminos_y_condiciones', controller=gobar_home_controller, action='terms')
        routing_map.connect('gobar_especificaciones', '/especificaciones', controller=gobar_home_controller, action='specs')
        routing_map.connect('gobar_contacto', '/contacto', controller=gobar_home_controller, action='contact')

        return routing_map
