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
        toolkit.add_resource('fanstatic', 'gobar_theme')
        toolkit.add_resource('fanstatic', 'bootstrap_style')
        toolkit.add_resource('fanstatic', 'bootstrap_scripts')

    def before_map(self, routing_map):

        routing_map.connect(
            '/',
            controller='ckanext.gobar_theme.controller:GobArHomeController',
            action='index'
        )

        return routing_map