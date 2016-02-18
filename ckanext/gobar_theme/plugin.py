import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.plugins import implements, IRoutes
import ckanext.gobar_theme.helpers as gobar_helpers


class Gobar_ThemePlugin(plugins.SingletonPlugin):
    implements(plugins.IConfigurer)
    implements(IRoutes, inherit=True)
    implements(plugins.ITemplateHelpers)

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
        routing_map.connect('/organization', controller=organizations_controller, action='index')
        routing_map.redirect('/organization/list', '/organization')
        routing_map.connect('/organization/new', action='new', controller='organization')
        routing_map.redirect('/organization/{id}', '/organization/list')
        routing_map.redirect('/organization/activity/{id}/{offset}', '/organization/list')
        routing_map.redirect('/organization/about/{id}', '/organization/list')
        routing_map.redirect('/organization/members/{id}', '/organization/list')
        routing_map.redirect('/organization/bulk_process/{id}', '/organization/list')

        # Grupos
        routing_map.redirect('/group', '/')
        routing_map.redirect('/group/list', '/')
        routing_map.connect('group_new', '/group/new', action='new', controller='group')
        routing_map.redirect('/group/{id}', '/group/list')
        routing_map.redirect('/group/about/{id}', '/group/list')
        routing_map.redirect('/group/members/{id}', '/group/list')
        routing_map.redirect('/group/activity/{id}/{offset}', '/group/list')

        # Usuarios
        user_controller = 'ckanext.gobar_theme.controller:GobArUserController'
        routing_map.connect('/user/edit', action='edit', controller='user')
        routing_map.redirect('/user/generate_key/{id}', '/')
        routing_map.redirect('/user/activity/{id}/{offset}', '/')
        routing_map.redirect('/user/activity/{id}', '/')
        routing_map.redirect('/user/follow/{id}', '/')
        routing_map.redirect('/user/unfollow/{id}', '/')
        routing_map.redirect('/user/followers/{id:.*}', '/')
        routing_map.connect('user_edit', '/user/edit/{id:.*}', action='edit', ckan_icon='cog', controller='user')
        routing_map.redirect('/user/delete/{id}', '/')
        routing_map.redirect('/user/reset/{id:.*}', '/')
        routing_map.redirect('/user/register', '/')
        routing_map.connect('login', '/user/login', action='login', controller='user')
        routing_map.connect('/user/_logout', action='logout', controller='user')
        routing_map.connect('/user/logged_in', action='logged_in', controller='user')
        routing_map.connect('/user/logged_out', action='logged_out', controller='user')
        routing_map.connect('/user/logged_out_redirect', action='logged_out_page', controller='user')
        routing_map.redirect('/user/reset', '/')
        routing_map.redirect('/user/me', '/')
        routing_map.redirect('/user/set_lang/{lang}', '/')
        routing_map.connect('user_datasets', '/user/{id:.*}', action='read', ckan_icon='sitemap', controller=user_controller)
        routing_map.redirect('/user', '/')

        return routing_map

    def get_helpers(self):
        return {
            'organization_tree': gobar_helpers.organization_tree,
            'get_faceted_groups': gobar_helpers.get_faceted_groups,
            'join_groups': gobar_helpers.join_groups
        }
