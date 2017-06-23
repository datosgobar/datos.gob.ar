import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.plugins import implements, IRoutes
import ckanext.gobar_theme_base as gobar_theme_base
import ckanext.gobar_theme_base.routing as gobar_routes_base
import ckanext.gobar_theme.routing as gobar_routes
import ckanext.gobar_theme.helpers as gobar_helpers
import os

class Gobar_ThemePlugin(plugins.SingletonPlugin):
    implements(plugins.IConfigurer)
    implements(IRoutes, inherit=True)
    implements(plugins.ITemplateHelpers)

    def before_map(self, routing_map):
        gobar_router = gobar_routes.GobArRouter(routing_map, gobar_routes_base)
        gobar_router.set_routes()
        return routing_map

    def add_base_templates(self, config):
        base_theme_dir = os.path.dirname(gobar_theme_base.__file__)
        rootdir = os.path.dirname(os.path.dirname(base_theme_dir))
        template_dir = os.path.join(rootdir, 'ckanext', 'gobar_theme_base', 'templates')
        config['extra_template_paths'] = ','.join([
            template_dir, config.get('extra_template_paths', '')
        ])

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        self.add_base_templates(config_)
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('styles/css', 'gobar_css')
        toolkit.add_resource('js', 'gobar_js')
        toolkit.add_resource('recline', 'gobar_data_preview')

    def get_helpers(self):
        return {
            'update_frequencies': gobar_helpers.update_frequencies
        }