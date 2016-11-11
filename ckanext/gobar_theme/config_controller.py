import ckan.lib.base as base
from ckan.common import request, g, c, _
import ckan.lib.helpers as h
import ckanext.gobar_theme.helpers as gobar_helpers
import ckan.logic as logic
import ckan.model as model
import urlparse

parse_params = logic.parse_params
abort = base.abort
check_access = logic.check_access
NotAuthorized = logic.NotAuthorized


class GobArConfigController(base.BaseController):
    def edit_title(self):
        self.authorize()
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
        self.authorize()
        if request.method == 'POST':
            params = parse_params(request.POST)
            g.gobar['home'] = {
                'title-template': params['title-template']
            }
            gobar_helpers.save_theme_config()
        return base.render('config/config_02_home.html')

    def edit_groups(self):
        self.authorize()
        if request.method == 'POST':
            params = parse_params(request.POST)
            g.gobar['groups'] = {
                'imgs': params['group-imgs']
            }
            gobar_helpers.save_theme_config()
            if 'json' in params:
                return h.json.dumps({'success': True}, for_json=True)
        return base.render('config/config_03_groups.html')

    def edit_header(self):
        self.authorize()
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
        self.authorize()
        if request.method == 'POST':
            params = parse_params(request.POST)
            g.gobar['social'] = {
                'fb': self._url_with_protocol(params['fb'].strip()),
                'tw': self._url_with_protocol(params['tw'].strip()),
                'github': self._url_with_protocol(params['github'].strip()),
                'inst': self._url_with_protocol(params['inst'].strip()),
                'yt': self._url_with_protocol(params['yt'].strip()),
                'mail': params['mail'].strip()
            }
            gobar_helpers.save_theme_config()
        return base.render('config/config_05_social.html')

    def edit_footer(self):
        self.authorize()
        if request.method == 'POST':
            params = parse_params(request.params)
            new_footer_params = {'url': self._url_with_protocol(params['url'].strip())}
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
        self.authorize()
        if request.method == 'POST':
            params = parse_params(request.POST)
            g.gobar['dataset'] = {
                'description': params['dataset-description'].strip()
            }
            gobar_helpers.save_theme_config()
        return base.render('config/config_07_dataset.html')

    def edit_organizations(self):
        self.authorize()
        if request.method == 'POST':
            params = parse_params(request.POST)
            g.gobar['organization'] = {
                'description': params['organization-description'].strip(),
                'show-organizations': 'show-organizations' in params
            }
            gobar_helpers.save_theme_config()
        return base.render('config/config_08_organizations.html')

    def edit_about(self):
        self.authorize()
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
        self.authorize()
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
        self.authorize()
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

    def edit_greetings(self):
        if request.method == 'POST':
            g.gobar['show-greetings'] = False
            gobar_helpers.save_theme_config()
        return h.json.dumps({'success': True}, for_json=True)

    @staticmethod
    def _url_with_protocol(url):
        if not urlparse.urlparse(url).scheme:
            url = "http://" + url
        return url

    @staticmethod
    def authorize():
        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'auth_user_obj': c.userobj,
                   'save': 'save' in request.params}
        try:
            check_access('package_create', context)
            return True
        except NotAuthorized:
            abort(401, _('Unauthorized to change config'))
