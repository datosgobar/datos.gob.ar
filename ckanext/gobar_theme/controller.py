from ckan.controllers.home import HomeController
from ckan.common import c
import ckan.logic as logic
import ckan.model as model
import ckan.lib.base as base


class GobArHomeController(HomeController):
    def _list_groups(self):
        context = {
            'model': model,
            'session': model.Session,
            'user': c.user or c.author
        }
        data_dict_page_results = {
            'all_fields': True,
            'type': 'group',
            'limit': None,
            'offset': 0,
        }
        return logic.get_action('group_list')(context, data_dict_page_results)

    def _featured_packages(self):
        context = {
            'model': model,
            'session': model.Session,
            'user': c.user or c.author,
            'for_view': True
        }
        data_dict = {
            'q': ''
        }
        search = logic.get_action('package_search')(context, data_dict)
        if 'results' in search:
            results = search['results']
            featured_packages = []
            for result in results:
                for extra_pair in result['extras']:
                    if extra_pair['key'] == 'home_featured':
                        featured_packages.append(result)

            segmented_packages = [featured_packages[n:n + 2] for n in range(len(featured_packages))[::2]]
            return segmented_packages
        return []

    def index(self):
        c.groups = self._list_groups()
        c.featured_packages = self._featured_packages()
        return super(GobArHomeController, self).index()

    def open_data(self):
        return base.render('static/open_data.html')

    def legal(self):
        return base.render('static/legal.html')

    def platform(self):
        return base.render('static/platform.html')
