from ckan.controllers.home import HomeController
from ckan.common import c
import ckan.logic as logic
import ckan.model as model
import ckan.lib.base as base


class GobArHomeController(HomeController):

    def index(self):
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
        c.groups = logic.get_action('group_list')(context, data_dict_page_results)
        return super(GobArHomeController, self).index()

    def open_data(self):
        return base.render('static/open_data.html')

    def legal(self):
        return base.render('static/legal.html')

    def platform(self):
        return base.render('static/platform.html')
