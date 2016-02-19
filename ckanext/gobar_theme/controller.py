from ckan.controllers.home import HomeController
from ckan.controllers.organization import OrganizationController
from ckan.controllers.user import UserController
from ckan.common import c
import ckan.lib.helpers as h
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

    def legal_planning(self):
        return base.render('static/legal_planning.html')

    def legal_system(self):
        return base.render('static/legal_system.html')

    def legal_access(self):
        return base.render('static/legal_access.html')

    def platform_users(self):
        return base.render('static/platform_users.html')

    def platform_terms(self):
        return base.render('static/platform_terms.html')

    def platform_license(self):
        return base.render('static/platform_license.html')

class GobArOrganizationController(OrganizationController):

    def index(self):
        return base.render('organization/index.html')


class GobArUserController(UserController):

    def read(self, id=None):
        if not c.user:
            h.redirect_to('/')
        else:
            return super(GobArUserController, self).read(id)
