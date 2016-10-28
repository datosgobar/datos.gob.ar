from routes.mapper import SubMapper


class GobArRouter:

    def __init__(self, route_map):
        self.route_map = route_map

        self.home_controller = 'ckanext.gobar_theme.controller:GobArHomeController'
        self.home_routes = SubMapper(self.route_map, controller=self.home_controller)
        self.api_controller = 'ckanext.gobar_theme.controller:GobArApiController'
        self.package_controller = 'ckanext.gobar_theme.package_controller:GobArPackageController'
        self.config_controller = 'ckanext.gobar_theme.config_controller:GobArConfigController'

    def redirect(self, *routes):
        for url_from, url_to in routes:
            self.route_map.redirect(url_from, url_to)

    def set_routes(self):
        self.connect_home()
        self.connect_static()
        self.connect_datasets()
        self.connect_organizations()
        self.connect_groups()
        self.connect_users()
        self.remove_dashboard()
        self.remove_tags()
        self.remove_revision()
        self.connect_api()
        self.connect_template_config()

    def connect_home(self):
        self.home_routes.connect('/', action='index')

    def connect_static(self):
        self.home_routes.connect('gobar_about', '/acerca', action='about')
        self.redirect(
            ('/about', '/acerca')
        )

    def connect_datasets(self):
        with SubMapper(self.route_map, controller=self.package_controller) as m:
            m.connect('search', '/dataset', action='search', highlight_actions='index search')
        self.route_map.connect('/dataset/{id}/archivo/{resource_id}', action='resource_read', controller='package')
        self.redirect(
            ('/dataset/history/{id:.*?}', '/dataset/{id}'),
            ('/dataset/activity/{id:.*?}', '/dataset/{id}'),
            ('/dataset/groups/{id:.*?}', '/dataset/{id}'),
            ('/dataset/followers/{id:.*?}', '/dataset/{id}'),
            ('/dataset/{id}/resource/{resource_id}', '/dataset/{id}/archivo/{resource_id}')
        )

    def remove_dashboard(self):
        self.redirect(
            ('/dashboard', '/'),
            ('/dashboard/datasets', '/'),
            ('/dashboard/groups', '/'),
            ('/dashboard/organizations', '/'),
            ('/dashboard/{url:.*?}', '/dashboard')
        )

    def connect_organizations(self):
        self.route_map.connect('/organizaciones', action='index', controller='organization')
        self.route_map.connect('/organization/new', action='new', controller='organization')
        self.redirect(
            ('/organization', '/organizaciones'),
            ('/organization/list', '/organization'),
            ('/organization/{id}', '/organization/list'),
            ('/organization/activity/{id}/{offset}', '/organization/list'),
            ('/organization/about/{id}', '/organization/list'),
            ('/organization/admins/{id}', '/organization/list'),
            ('/organization/members/{id}', '/organization/list'),
            ('/organization/member_new/{id}', '/organization/list'),
            ('/organization/member_delete/{id}', '/organization/list'),
            ('/organization/history/{id}', '/organization/list'),
            ('/organization/bulk_process/{id}', '/organization/list')
        )

    def connect_groups(self):
        self.route_map.connect('group_new', '/group/new', action='new', controller='group')
        self.redirect(
            ('/group', '/'),
            ('/group/list', '/'),
            ('/group/{id}', '/group/list'),
            ('/group/about/{id}', '/group/list'),
            ('/group/members/{id}', '/group/list'),
            ('/group/member_new/{id}', '/group/list'),
            ('/group/member_delete/{id}', '/group/list'),
            ('/group/history/{id}', '/group/list'),
            ('/group/followers/{id}', '/group/list'),
            ('/group/follow/{id}', '/group/list'),
            ('/group/unfollow/{id}', '/group/list'),
            ('/group/admins/{id}', '/group/list'),
            ('/group/activity/{id}/{offset}', '/group/list')
        )

    def connect_users(self):
        self.route_map.connect('login', '/ingresar', action='login', controller='user')
        self.route_map.connect('/logout', action='logout', controller='user')
        self.redirect(
            ('/user/login', '/'),
            ('/user/generate_key/{id}', '/'),
            ('/user/activity/{id}/{offset}', '/'),
            ('/user/activity/{id}', '/'),
            ('/user/follow/{id}', '/'),
            ('/user/unfollow/{id}', '/'),
            ('/user/followers/{id:.*}', '/'),
            ('/user/delete/{id}', '/'),
            ('/user/reset/{id:.*}', '/'),
            ('/user/register', '/'),
            ('/user/reset', '/'),
            ('/user/set_lang/{lang}', '/'),
            ('/user', '/'),
            ('/user/_logout', '/logout'),
            ('/user/logged_out_redirect', '/'),
            ('/salir', '/logout')
        )

    def remove_tags(self):
        self.redirect(
            ('/tag', '/'),
            ('/tag/{url}', '/')
        )

    def remove_revision(self):
        self.redirect(
            ('/revision', '/'),
            ('/revision/list', '/'),
            ('/revision/edit/{id}', '/revision'),
            ('/revision/diff/{id}', '/revision'),
            ('/revision/{id}', '/revision')
        )

    def connect_api(self):
        with SubMapper(self.route_map, controller=self.api_controller, path_prefix='/api{ver:/3|}', ver='/3') as m:
            m.connect('/action/{logic_function}', action='action', conditions=dict(method=['GET', 'POST']))

    def connect_template_config(self):
        with SubMapper(self.route_map, controller=self.config_controller) as m:
            m.connect('/configurar/titulo', action='edit_title')
            m.connect('/configurar/portada', action='edit_home')
            m.connect('/configurar/encabezado', action='edit_header')
            m.connect('/configurar/temas', action='edit_groups')
            m.connect('/configurar/redes', action='edit_social')
            m.connect('/configurar/pie-de-pagina', action='edit_footer')
            m.connect('/configurar/datasets', action='edit_datasets')
            m.connect('/configurar/organizaciones', action='edit_organizations')
            m.connect('/configurar/acerca', action='edit_about')
            m.connect('/configurar/metadata/google_fb', action='edit_metadata_google_fb')
            m.connect('/configurar/metadata/tw', action='edit_metadata_tw')

        self.redirect(
            ('/configurar', '/configurar/titulo'),
            ('/configurar', '/configurar/metadata')
        )
