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

        home_controller = 'ckanext.gobar_theme.controller:GobArHomeController'
        routing_map.connect('/', controller=home_controller, action='index')

        # Paginas estaticas en el footer
        routing_map.redirect('/about', '/acerca_del_sitio')
        routing_map.connect('gobar_acerca_de', '/acerca_del_sitio', controller=home_controller, action='about')
        routing_map.connect('gobar_terminos', '/terminos_y_condiciones', controller=home_controller, action='terms')
        routing_map.connect('gobar_especificaciones', '/especificaciones', controller=home_controller, action='specs')
        routing_map.connect('gobar_contacto', '/contacto', controller=home_controller, action='contact')

        # Dashboard de usuario registrado
        routing_map.redirect('/dashboard', '/')
        routing_map.redirect('/dashboard/datasets', '/')
        routing_map.redirect('/dashboard/groups', '/')
        routing_map.redirect('/dashboard/organizations', '/')
        routing_map.redirect('/dashboard/{url:.*?}', '/dashboard')

        # Organizaciones
        organizations_controller = 'ckanext.gobar_theme.controller:GobArOrganizationController'
        routing_map.connect('organizaciones', '/organizaciones', controller=organizations_controller, action='index')
        routing_map.redirect('/organization', '/organizaciones')
        routing_map.connect('organization_read', '/organizaciones/{id}', action='read', controller='organization')
        routing_map.redirect('/organization/activity/{id}/{offset}', '/organizaciones/{id}')
        routing_map.redirect('/organization/about/{id}', '/organizaciones/{id}')
        routing_map.redirect('/organization/members/{id}', '/organizaciones/{id}')
        routing_map.redirect('/organization/history/{id}', '/organizaciones/{id}')
        routing_map.redirect('/organization/admins/{id}', '/organizaciones/{id}')
        routing_map.redirect('/organization/member_new/{id}', '/organizaciones/{id}')
        routing_map.redirect('/organization/bulk_process/{id}', '/organizaciones/{id}')

        return routing_map
