import json

from channels import Group
from channels.sessions import channel_session, http_session
from channels.auth import http_session_user

from celery.result import AsyncResult


@http_session_user
@http_session
@channel_session
def connect_waiter(message):

    task_id = message.http_session['active_phone_number_task_id']
    task = AsyncResult(task_id)

    if task.ready():
        content = json.dumps({
            'success': True,
            'msg': 'already done'
        })

        message.reply_channel.send({
            'text': content
        })

    else:
        group = Group("phone_verify-%s" % message.user.username)
        group.add(
            message.reply_channel
        )

        content = json.dumps({
            'sending': True,
        })

        group.send({
            'text': content
        })


@http_session_user
@http_session
@channel_session
def disconnect_waiter(message):
    Group("phone_verify-%s" % message.user.username).discard(
        message.reply_channel
    )
