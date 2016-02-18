import ckan.logic as logic
import ckan.lib.helpers as ckan_helpers


def _get_organizations_objs(organizations_branch, depth=0):
    organizations = []
    for tree_obj in organizations_branch:
        organization = ckan_helpers.get_organization(org=tree_obj['name'])
        organization['depth'] = depth
        if 'children' in tree_obj and len(tree_obj['children']) > 0:
            organization['children'] = _get_organizations_objs(tree_obj['children'], depth=depth+1)
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


def join_groups(selected_groups, remaining_groups):
    groups = []
    for group in selected_groups:
        group['selected'] = True
        groups.append(group)
    for group in remaining_groups:
        group['selected'] = False
        groups.append(group)
    return sorted(groups, key=lambda k: k['display_name'].lower())


def cut_text(text, limit):
    if len(text) > limit:
        text, remaining = text[:limit], text[limit:]
        if ' ' in remaining:
            text += remaining.split(' ')[0]
        text += '...'
    return text
