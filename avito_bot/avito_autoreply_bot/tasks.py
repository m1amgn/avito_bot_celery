import logging

from celery_app import app
from .models import Profiles
from .service import AvitoAutoreplyBot


logger = logging.getLogger('django')


@app.task
def get_access_token():
    try:
        profiles = Profiles.objects.filter(paid=True)
    except Exception as e:
        logger.error(
            "Error in tasks.get_access_token to get parameters of profiles from db: %s", str(e))
    try:
        for profile in profiles:
            client_id = profile.client_id
            client_secret = profile.client_secret
            user_id = profile.user_id
            text_message = profile.text_message
            avito_bot = AvitoAutoreplyBot(client_id=client_id,
                                          client_secret=client_secret,
                                          user_id=user_id,
                                          text_message=text_message)
            avito_bot.get_access_token()
        return True
    except Exception as e:
        logger.error(
            "Error in tasks.get_access_token: %s", str(e))


@app.task
def auto_reply():
    try:
        profiles_data = Profiles.objects.filter(paid=True)
    except Exception as e:
        logger.error(
            "Error in tasks.auto_reply to get parameters of profiles from db: %s", str(e))
    try:
        for profile in profiles_data:
            client_id = profile.client_id
            client_secret = profile.client_secret
            user_id = profile.user_id
            text_message = profile.text_message
            avito_bot = AvitoAutoreplyBot(client_id=client_id,
                                          client_secret=client_secret,
                                          user_id=user_id,
                                          text_message=text_message)
            avito_bot.send_auto_reply()
        return True
    except Exception as e:
        logger.error(
            "Error in tasks.auto_reply: %s", str(e))
