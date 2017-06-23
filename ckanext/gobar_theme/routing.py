from routes.mapper import SubMapper


class GobArRouter:

    def __init__(self, route_map, base_theme):
        self.route_map = route_map
        self.base_theme = base_theme.GobArRouter(route_map)

        self.home_controller = 'ckanext.gobar_theme.controller:GobArHomeController'
        self.home_routes = SubMapper(self.route_map, controller=self.home_controller)

    def set_routes(self):
        self.connect_static()
        self.connect_users()
        self.connect_theme_taxonomy()
        self.connect_error_pages()
        self.base_theme.set_routes()

    def connect_static(self):
        with SubMapper(self.route_map, controller='ckanext.gobar_theme.controller:GobArHomeController') as m:
            m.connect('gobar_our_site', '/acerca/nuestro-portal', action='about_our_site')
            m.connect('gobar_legal', '/acerca/marco-legal', action='about_legal')
            m.connect('gobar_devs', '/acerca/desarrolladores', action='about_developers')
            m.connect('gobar_glossary', '/acerca/glosario', action='about_glossary')
            self.base_theme.redirect(
                ('/acerca', '/acerca/nuestro-portal'),
                ('/about', '/acerca/nuestro-portal')
            )

    def connect_users(self):
        self.route_map.connect('login', '/635511788', action='login', controller='user')

    def connect_theme_taxonomy(self):
        self.home_routes.connect('/superThemeTaxonomy.json', action='theme_taxonomy')

    def connect_error_pages(self):
        self.home_routes.connect('technical_problems', '/problemas-tecnicos', action='technical_problems')
        self.home_routes.connect('server_overload', '/muchas-visitas', action='server_overload')
        self.home_routes.connect('upgrading_server', '/mejorando-el-sitio', action='upgrading_server')
