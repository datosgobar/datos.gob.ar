from ckan.controllers.home import HomeController
from ckan.controllers.api import ApiController
from ckan.controllers.user import UserController
import ckan.lib.helpers as h
from ckan.common import c
import ckan.logic as logic
import ckan.model as model
import ckan.lib.base as base
import json


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
                    if extra_pair['key'] == 'home_featured' and extra_pair['value'] == 'true':
                        featured_packages.append(result)

            segmented_packages = [featured_packages[n:n + 2] for n in range(len(featured_packages))[::2]]
            return segmented_packages
        return []

    def index(self):
        c.groups = self._list_groups()
        c.featured_packages = self._featured_packages()
        return super(GobArHomeController, self).index()

    def about(self):
        return base.render('about.html')


class GobArApiController(ApiController):

    def _remove_extra_id_field(self, json_string):
        json_dict = json.loads(json_string)
        has_extra_id = False
        if 'result' in json_dict and 'fields' in json_dict['result']:
            for field in json_dict['result']['fields']:
                if 'id' in field and field['id'] == '_id':
                    has_extra_id = True
                    json_dict['result']['fields'].remove(field)
            if has_extra_id and 'records' in json_dict['result']:
                for record in json_dict['result']['records']:
                    if '_id' in record:
                        del record['_id']
        return json.dumps(json_dict)

    def action(self, logic_function, ver=None):
        default_response = super(GobArApiController, self).action(logic_function, ver)
        if logic_function == 'datastore_search':
            default_response = self._remove_extra_id_field(default_response)
        return default_response


class GobArUserController(UserController):

    def read(self, id=None):
        if id and id == c.user:
            return super(GobArUserController, self).read(id)
        return h.redirect_to('home')
