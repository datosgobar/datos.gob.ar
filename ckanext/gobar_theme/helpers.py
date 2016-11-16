# coding=utf-8
import ckan.logic as logic
import ckan.lib.helpers as ckan_helpers
from urlparse import urlparse
from ckan.common import request, c, g
import json
from urlparse import urljoin
from config_controller import GobArConfigController


def _get_organizations_objs(organizations_branch, depth=0):
    organizations = []
    for tree_obj in organizations_branch:
        organization = ckan_helpers.get_organization(org=tree_obj['name'])
        organization['depth'] = depth
        if 'children' in tree_obj and len(tree_obj['children']) > 0:
            organization['children'] = _get_organizations_objs(tree_obj['children'], depth=depth + 1)
        organizations.append(organization)
    return organizations


def _count_total(organization):
    children_count = 0
    if 'children' in organization and len(organization['children']):
        for child_organization in organization['children']:
            children_count += _count_total(child_organization)
    return organization['package_count'] + children_count


def organization_tree():
    organizations_tree = logic.get_action('group_tree')({}, {'type': 'organization'})
    organizations = _get_organizations_objs(organizations_tree)
    for organization in organizations:
        organization['display_count'] = _count_total(organization)
    return organizations


def get_faceted_groups():
    data_dict_page_results = {
        'all_fields': True,
        'type': 'group',
        'limit': None,
        'offset': 0,
    }
    groups = logic.get_action('group_list')({}, data_dict_page_results)
    facets = ckan_helpers.get_facet_items_dict('groups')
    facets_by_name = {}
    for facet in facets:
        facets_by_name[facet['name']] = facet
    for group in groups:
        group_name = group['name']
        if group_name in facets_by_name:
            group['facet_active'] = facets_by_name[group['name']]['active']
            group['facet_count'] = facets_by_name[group['name']]['count']
        else:
            group['facet_active'] = False
            group['facet_count'] = 0
    return groups


def join_groups(selected_groups):
    data_dict_page_results = {
        'all_fields': True,
        'type': 'group',
        'limit': None,
        'offset': 0,
    }
    groups = logic.get_action('group_list')({}, data_dict_page_results)
    for selected_group in selected_groups:
        for group in groups:
            if selected_group['name'] == group['name']:
                group['selected'] = True
    return sorted(groups, key=lambda k: k['display_name'].lower())


def cut_text(text, limit):
    if len(text) > limit:
        text, remaining = text[:limit], text[limit:]
        if ' ' in remaining:
            text += remaining.split(' ')[0]
        text += '...'
    return text


def cut_img_path(url):
    return urlparse(url).path


def organizations_with_packages():
    organizations = logic.get_action('organization_list')({}, {'all_fields': True})
    organizations_with_at_least_one_package = [
        organization for organization in organizations if organization['package_count'] > 0
        ]
    return len(organizations_with_at_least_one_package)


def get_pkg_extra(pkg, keyname):
    if 'extras' in pkg and pkg['extras']:
        for extra in pkg['extras']:
            if extra['key'] == keyname:
                return extra['value']
    return None


def all_descendants(organization_list):
    descendants = []
    for organization in organization_list:
        descendants.append(organization['name'])
        if 'children' in organization and len(organization['children']) > 0:
            descendants += all_descendants(organization['children'])
    return descendants


def organization_filters():
    top_organizations = {}
    ancestors_relations = {}
    tree = organization_tree()
    for top_organization in tree:
        top_organization['count'] = 0
        top_organizations[top_organization['name']] = top_organization
        ancestors_relations[top_organization['name']] = top_organization['name']
        if 'children' in top_organization and len(top_organization['children']) > 0:
            children = all_descendants(top_organization['children'])
            for child_name in children:
                ancestors_relations[child_name] = top_organization['name']

    for organization in ckan_helpers.get_facet_items_dict('organization'):
        top_parent_name = ancestors_relations[organization['name']]
        if top_parent_name in top_organizations:
            top_organizations[top_parent_name]['count'] += organization['count']
    if ckan_helpers.get_request_param('organization') in top_organizations:
        top_organizations[ckan_helpers.get_request_param('organization')]['active'] = True

    top_organizations_with_results = [organization for organization in top_organizations.values() if
                                      organization['count'] > 0]
    sorted_organizations = sorted(top_organizations_with_results, key=lambda item: item['count'], reverse=True)

    limit = int(request.params.get('_organization_limit', g.facets_default_number))
    c.search_facets_limits['organization'] = limit
    if limit is not None and limit > 0:
        return sorted_organizations[:limit]
    return sorted_organizations


def get_facet_items_dict(facet, limit=None, exclude_active=False):
    if facet == 'organization':
        return organization_filters()
    return ckan_helpers.get_facet_items_dict(facet, limit, exclude_active)


def get_theme_config(path=None, default=None):
    return GobArConfigController.get_theme_config(path, default)


def url_join(*args):
    return urljoin(*args)


def json_loads(json_string):
    return json.loads(json_string)


def update_frequencies():
    return {
        "R/P10Y": "Cada diez años",
        "R/P4Y": "Cada cuatro años",
        "R/P3Y": "Cada tres años",
        "R/P2Y": "Cada dos años",
        "R/P1Y": "Anualmente",
        "R/P6M": "Cada medio año",
        "R/P4M": "Cuatrimestralmente",
        "R/P3M": "Trimestralmente",
        "R/P2M": "Bimestralmente",
        "R/P1M": "Mensualmente",
        "R/P0.5M": "Cada 15 días",
        "R/P0.33M": "Tres veces por mes",
        "R/P1W": "Semanalmente",
        "R/P3.5D": "Cada media semana",
        "R/P0.5W": "Dos veces a la semana",
        "R/P0.33W": "Tres veces a la semana",
        "R/P1D": "Diariamente",
        "R/PT1H": "Cada hora",
        "R/PT1S": "Continuamente actualizado",
        'eventual': 'Eventual'
    }


def field_types():
    return {
        "string": "Texto (string)",
        "integer": "Número entero (integer)",
        "number": "Número decimal (number)",
        "boolean": "Verdadero/falso (boolean)",
        "time": "Tiempo ISO-8601 (time)",
        "date": "Fecha ISO-8601 (date)",
        "date-time": "Fecha y hora ISO-8601 (date-time)",
        "object": "JSON (object)",
        "geojson": "GeoJSON (geojson)",
        "geo_point": "GeoPoint (geo_point)",
        "array": "Lista de valores en formato JSON (array)",
        "binary": "Valor binario en base64 (binary)",
        "any": "Otro (any)"
    }
