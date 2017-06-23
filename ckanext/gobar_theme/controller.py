from ckanext.gobar_theme_base.controller import GobArHomeController as HomeController
import ckan.logic as logic
import ckan.lib.base as base
import json


class GobArHomeController(HomeController):
    def about_our_site(self):
        return base.render('static/about_our_site.html')

    def about_legal(self):
        return base.render('static/about_legal.html')

    def about_developers(self):
        return base.render('static/about_developers.html')

    def about_glossary(self):
        return base.render('static/about_glossary.html')

    def theme_taxonomy(self):
        print "HOLA"
        data_dict_page_results = {
            'all_fields': True,
            'type': 'group',
            'limit': None,
            'offset': 0,
        }
        groups = logic.get_action('group_list')({}, data_dict_page_results)
        taxonomy = [{
            'id': group['name'],
            'label': group['display_name'],
            'description': group['description']
        } for group in groups]

        return json.dumps(taxonomy)

    def technical_problems(self):
        return base.render('static/technical_problems.html')

    def server_overload(self):
        return base.render('static/server_overload.html')

    def upgrading_server(self):
        return base.render('static/upgrading_server.html')

