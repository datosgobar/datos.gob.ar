# coding=utf-8
import ckan.logic as logic
import ckan.lib.activity_streams as activity_streams
import ckan.lib.base as base
import re
import sys
from webhelpers.html import literal


def package_activity_list_html(context, data_dict):
    activity_stream = logic.action.get.package_activity_list(context, data_dict)
    offset = int(data_dict.get('offset', 0))
    extra_vars = {
        'controller': 'package',
        'action': 'activity',
        'id': data_dict['id'],
        'offset': offset,
    }
    return activity_list_to_html(
        context, activity_stream, extra_vars)


def activity_list_to_html(context, activity_stream, extra_vars):
    activity_list = [] # These are the activity stream messages.
    for activity in activity_stream:
        detail = None
        activity_type = activity['activity_type']
        # Some activity types may have details.
        if activity_type in activity_streams.activity_stream_actions_with_detail:
            details = logic.get_action('activity_detail_list')(context=context,
                                                               data_dict={'id': activity['id']})
            # If an activity has just one activity detail then render the
            # detail instead of the activity.
            if len(details) == 1:
                detail = details[0]
                object_type = detail['object_type']

                if object_type == 'PackageExtra':
                    object_type = 'package_extra'

                new_activity_type = '%s %s' % (detail['activity_type'],
                                               object_type.lower())
                if new_activity_type in activity_streams.activity_stream_string_functions:
                    activity_type = new_activity_type

        if not activity_type in activity_streams.activity_stream_string_functions:
            raise NotImplementedError("No activity renderer for activity "
                                      "type '%s'" % activity_type)

        if activity_type in activity_streams.activity_stream_string_icons:
            activity_icon = activity_streams.activity_stream_string_icons[activity_type]
        else:
            activity_icon = activity_streams.activity_stream_string_icons['undefined']

        activity_msg = activity_streams.activity_stream_string_functions[activity_type](context,
                                                                                        activity)

        include_msg = True

        # Get the data needed to render the message.
        matches = re.findall('\{([^}]*)\}', activity_msg)
        data = {}
        for match in matches:
            snippet = activity_streams.activity_snippet_functions[match](activity, detail)
            if match == 'extra':
                if 'updateFrequency' in snippet:
                    data[str(match)] = 'Frecuencia de actualización'
                    activity_msg = u'{actor} actualizó {extra} del conjunto de datos {dataset}'
                else:
                    include_msg = False
            else:
                data[str(match)] = snippet

        reload(sys)
        sys.setdefaultencoding('utf-8')

        if include_msg:
            activity_list.append({'msg': activity_msg,
                                  'type': activity_type.replace(' ', '-').lower(),
                                  'icon': activity_icon,
                                  'data': data,
                                  'timestamp': activity['timestamp'],
                                  'is_new': activity.get('is_new', False)})

    extra_vars['activities'] = activity_list
    return literal(base.render('activity_streams/activity_stream_items.html',
extra_vars=extra_vars))