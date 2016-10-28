import ckan.lib.base as base
from ckan.common import request, g
import ckanext.gobar_theme.helpers as gobar_helpers
import ckan.logic as logic

parse_params = logic.parse_params


class GobArConfigController(base.BaseController):
    def edit_title(self):
        if request.method == 'POST':
            params = parse_params(request.params)
            new_title_config = {
                'site-title': params['site-title'].strip(),
                'site-description': params['site-description'].strip()
            }
            if params['image-logic'] == 'new-image':
                new_title_config['background-image'] = gobar_helpers.save_img(params['background-image'])
            elif params['image-logic'] == 'delete-image':
                new_title_config['background-image'] = None
            else:
                new_title_config['background-image'] = gobar_helpers.get_theme_config('title.background-image')
            g.gobar['title'] = new_title_config
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
        if request.method == 'POST':
            params = parse_params(request.params)
            if params['image-logic'] == 'new-image':
                g.gobar['header'] = {'image': gobar_helpers.save_img(params['background-image'])}
            elif params['image-logic'] == 'delete-image':
                g.gobar['header'] = {'image': None}
            else:
                g.gobar['header'] = {'image': gobar_helpers.get_theme_config('header.image')}
            gobar_helpers.save_theme_config()
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
        if request.method == 'POST':
            params = parse_params(request.params)
            new_footer_params = {'url': params['url'].strip()}
            if params['image-logic'] == 'new-image':
                new_footer_params['image'] = gobar_helpers.save_img(params['background-image'])
            elif params['image-logic'] == 'delete-image':
                new_footer_params['image'] = None
            else:
                new_footer_params['image'] = gobar_helpers.get_theme_config('footer.image')
            g.gobar['footer'] = new_footer_params
            gobar_helpers.save_theme_config()
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
        if request.method == 'POST':
            params = parse_params(request.POST)
            g.gobar['about'] = {
                'title': params['about-title'].strip(),
                'description': params['about-description'].strip(),
                'show-about': 'show-about' in params
            }
            gobar_helpers.save_theme_config()
        return base.render('config/config_09_about.html')

    def edit_metadata_google_fb(self):
        if request.method == 'POST':
            params = parse_params(request.POST)
            new_metadata_config = {
                'title': params['metadata-title'].strip(),
                'description': params['metadata-description'].strip()
            }
            if params['image-logic'] == 'new-image':
                new_metadata_config['image'] = gobar_helpers.save_img(params['image'])
            elif params['image-logic'] == 'delete-image':
                new_metadata_config['image'] = None
            else:
                new_metadata_config['image'] = gobar_helpers.get_theme_config('fb-metadata.image')
            g.gobar['fb-metadata'] = new_metadata_config
            gobar_helpers.save_theme_config()
        return base.render('config/config_10_metadata_google_fb.html')

    def edit_metadata_tw(self):
        if request.method == 'POST':
            params = parse_params(request.POST)
            new_metadata_config = {
                'title': params['metadata-title'].strip(),
                'description': params['metadata-description'].strip(),
                'user': params['metadata-user'].strip()
            }
            if params['image-logic'] == 'new-image':
                new_metadata_config['image'] = gobar_helpers.save_img(params['image'])
            elif params['image-logic'] == 'delete-image':
                new_metadata_config['image'] = None
            else:
                new_metadata_config['image'] = gobar_helpers.get_theme_config('tw-metadata.image')
            g.gobar['tw-metadata'] = new_metadata_config
            gobar_helpers.save_theme_config()
        return base.render('config/config_11_metadata_twitter.html')
