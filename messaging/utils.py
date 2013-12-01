import json
import urllib2


def send_notification(session_key, message, users):
    user_pks = [unicode(user.pk) for user in users]
    data = {'sessionid': session_key,
            'message_id': message.pk,
            'message': message.body,
            'users': user_pks}
    urllib2.urlopen("http://localhost:8080/post_message",
                    data=json.dumps(data))
