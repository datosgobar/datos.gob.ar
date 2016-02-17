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

    def about(self):
        return base.render('static/about.html')

    def terms(self):
        return base.render('static/terms.html')

    def specs(self):
        return base.render('static/specs.html')


class GobArOrganizationController(OrganizationController):

    def index(self):
        return base.render('organization/index.html')


class GobArUserController(UserController):

    def read(self, id=None):
        if not c.user:
            h.redirect_to('/')
        else:
            return super(GobArUserController, self).read(id)
