import ckan.logic as logic
import ckan.lib.helpers as ckan_helpers
import ckan.plugins as p
import ckan.plugins.toolkit as toolkit
from urlparse import urlparse



def get_page_try(page):
    """wrapper to ckan_helpers get_page_html, if the page is not found
    this function scapes the error silently."""

    _page = p.toolkit.get_action('ckanext_pages_show')(
            data_dict={'org_id': None,
                'page': page})
    try:
        return _page['content']
    except KeyError as k:
        raise k

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


def cut_img_path(url):
    return urlparse(url).path


def organizations_with_packages():
    organizations = logic.get_action('organization_list')({}, {'all_fields': True})
    organizations_with_at_least_one_package = [
        organization for organization in organizations if organization['package_count'] > 0
    ]
    return len(organizations_with_at_least_one_package)

def _last_resources():
        """
        Obtiene los ultimos datasets modificados/creados, con su respectivos
        recursos.
        Sin embargo lo que se obtendra es el ultimo recurso de cada dataset
        que traiga.
        """
        data_dict = {
            'limit': 6
        }
        packages = logic.get_action('current_package_list_with_resources')\
            ({}, data_dict)

        response  = []
        for package in packages:
            if 'resources' in package:
                try:
                    modified = package['resources'][-1]['last_modified']\
                        .split('T')[0]
                    title = package['title']
                    pack_id = package['id']
                    response.append({ 'id': pack_id,
                                     'modified': modified,
                                     'title': title })
                except IndexError:
                    pass
                except KeyError:
                    pass
                except AttributeError:
                    pass

        return response


def get_blog_articles(number=8, exclude=None):
    """
    Obtiene las ultimas notas publicadas. es necesario el plugin de pages.
    Taked from https://github.com/ckan/ckanext-pages/blob/master/ckanext/pages/plugin.py
    """
    #import pdb; pdb.set_trace()
    blog_list = toolkit.get_action('ckanext_pages_list')(
        None, {'order_publish_date': True, 'private': False,
               'page_type': 'blog'}
    )
    new_list = []
    for blog in blog_list:
        if exclude and blog['name'] == exclude:
            continue
        new_list.append(blog)
        if len(new_list) == number:
            break

    return new_list

def prueba_helper():
    return "esto es un helper de prueba"


