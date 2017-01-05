import json

from celery.utils.log import get_task_logger

from channels import Group

from django.conf import settings

from twilio import TwilioRestException
from twilio.rest import TwilioRestClient

from growthstreet.celery import app as celery_app

from customers.models import Customer


logger = get_task_logger(__name__)


@celery_app.task
def send_phone_code(user_id, verify_token, phone_number):
    customer = Customer.objects.get(id=user_id)

    from time import sleep
    from random import randint
    # simulating a short delay
    sleep(randint(3, 9))

    client = TwilioRestClient(  # noqa
        settings.TWILLO_API_KEY,
        settings.TWILLO_AUTH_TOKEN,
    )

    try:
        client.messages.create(
            to=phone_number,
            from_=settings.TWILLO_FROM_NUMBER,
            body="Your Verify Code is {}".format(
                verify_token
            )
        )
        # Notify the FE task has completed
        Group('phone_verify-%s' % customer.username).send({
            'text': json.dumps({
                'success': True,
                'msg': 'new message sent'
            })
        })
    except TwilioRestException as e:
        Group('phone_verify-%s' % customer.username).send({
            'text': json.dumps({
                'success': False,
                'msg': e.msg
            })
        })
