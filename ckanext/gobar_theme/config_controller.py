import ckan.lib.base as base
from ckan.common import request, g
import ckan.lib.helpers as h
import ckanext.gobar_theme.helpers as gobar_helpers
import ckan.logic as logic
parse_params = logic.parse_params


class GobArConfigController(base.BaseController):

    def edit_config(self):
        # TODO: sacar este metodo
        if request.method == 'POST':
            params = parse_params(request.POST)
            self._update_config(params)
            h.redirect_to(controller='ckanext.gobar_theme.controller:GobArHomeController', action='index')
        else:
            return base.render('config/edit_templates.html')

    def edit_title(self):
        if request.method == 'POST':
            params = parse_params(request.POST)
            g.gobar['title'] = {
                'site-title': params['site-title'].strip(),
                'site-description': params['site-description'].strip()
            }
            gobar_helpers.save_theme_config()
        return base.render('config/config_01_title.html')

    def edit_home(self):
        if request.method == 'POST':
            params = parse_params(request.POST)
            g.gobar['home'] = {
                'title-template': params['title-template']
            }
            gobar_helpers.save_theme_config()
        return base.render('config/config_02_home.html')

    def edit_groups(self):
        if request.method == 'POST':
            params = parse_params(request.POST)
            g.gobar['groups'] = {
                'imgs': params['group-imgs']
            }
            gobar_helpers.save_theme_config()
        return base.render('config/config_03_groups.html')

    def edit_header(self):
        return base.render('config/config_04_header.html')

    def edit_social(self):
        if request.method == 'POST':
            params = parse_params(request.POST)
            g.gobar['social'] = {
                'fb': params['fb'].strip(),
                'tw': params['tw'].strip(),
                'github': params['github'].strip(),
                'inst': params['inst'].strip(),
                'yt': params['yt'].strip(),
                'mail': params['mail'].strip()
            }
            gobar_helpers.save_theme_config()
        return base.render('config/config_05_social.html')

    def edit_footer(self):
        return base.render('config/config_06_footer.html')

    def edit_datasets(self):
        if request.method == 'POST':
            params = parse_params(request.POST)
            g.gobar['dataset'] = {
                'description': params['dataset-description'].strip()
            }
            gobar_helpers.save_theme_config()
        return base.render('config/config_07_dataset.html')

    def edit_organizations(self):
        if request.method == 'POST':
            params = parse_params(request.POST)
            g.gobar['organization'] = {
                'description': params['organization-description'].strip(),
                'show-organizations': 'show-organizations' in params
            }
            gobar_helpers.save_theme_config()
        return base.render('config/config_08_organizations.html')

    def edit_about(self):
        return base.render('config/config_09_about.html')

    def edit_metadata_google_fb(self):
        return base.render('config/config_10_metadata_google_fb.html')

    def edit_metadata_tw(self):
        return base.render('config/config_11_metadata_twitter.html')
