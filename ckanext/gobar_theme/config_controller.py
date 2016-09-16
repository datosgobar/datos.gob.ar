import ckan.lib.base as base
from ckan.common import request, g
import ckan.lib.helpers as h
import ckan.logic as logic
import json
parse_params = logic.parse_params


class GobArConfigController(base.BaseController):

    def edit_config(self):
        if request.method == 'POST':
            params = parse_params(request.POST)
            self._update_config(params)
            h.redirect_to(controller='ckanext.gobar_theme.controller:GobArHomeController', action='index')
        else:
            return base.render('config/edit_templates.html')

    def _update_config(self, new_params):
        new_params_dict = {
            "home_title_template": int(new_params['title-variant']),
            "home_title": new_params['home_title'],
            "home_description": new_params['home_description'],
            "organization_description": new_params['organization_description'],
            "dataset_description": new_params['dataset_description'],
            "facebook_link": new_params['facebook_link'],
            "twitter_link": new_params['twitter_link'],
            "github_link": new_params['github_link'],
            "instagram_link": new_params['instagram_link'],
            "youtube_link": new_params['youtube_link']
        }
        g.gobar = new_params_dict
        with open('/var/lib/ckan/default/gobar/settings.json', 'w') as json_data:
            json_data.write(json.dumps(new_params_dict))
