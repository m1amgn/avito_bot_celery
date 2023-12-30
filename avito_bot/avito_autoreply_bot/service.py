import requests
import time
import random
import logging

from .models import Chats, AccessTokens


logger = logging.getLogger('django')


class AvitoAutoreplyBot:
    def __init__(self, client_id: str, client_secret: str, user_id: str, text_message: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_id = user_id
        self.text_message = text_message

    def get_access_token(self):
        try:
            response = requests.post(
                "https://api.avito.ru/token/",
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
            )
            if response.status_code == 200:
                token_data = response.json()
                access_token = token_data["access_token"]
                AccessTokens.objects.create(
                    user_id=self.user_id, access_token=access_token)
            else:
                logger.error(f"Error in get_access_token: response status code not 200 - {response.text}, user_id - {self.user_id}")
        except Exception as e:
            logger.error("Error in service.get_access_token: %s", str(e))

    def _get_user_chats(self, access_token) -> list:
        access_token = access_token
        headers = {"Authorization": f"Bearer {access_token}"}
        try:
            response = requests.get(
                f"https://api.avito.ru/messenger/v2/accounts/{self.user_id}/chats?unread_only=true&chat_types=u2i,u2u", headers=headers)

            if response.status_code == 200:
                chats = response.json()
                chats_id_list = []
                for chat in chats["chats"]:
                    if chat["last_message"]["author_id"] != 0:
                        chats_id_list.append(chat["id"])
                return chats_id_list
            else:
                logger.error(f"Error in service._get_user_chats: response status code not 200 - {response.text}, user_id - {self.user_id}")
                return []
        except Exception as e:
            logger.error("Error in service._get_users_chats: %s", str(e))

    def send_auto_reply(self):
        try:
            access_token_query = AccessTokens.objects.filter(user_id=self.user_id).order_by('-created_timestamp')[:1]
            if access_token_query.exists():
                access_token = access_token_query[0].access_token
            else:
                logger.error(f'Error in service.send_auto_reply: no access_token found for the user, user_id - {self.user_id}')
                # Handle the case when there is no access token
                return
        except Exception as e:
            logger.error("Error in service.send_auto_reply to get access token from BD: %s", str(e))

        chats_data = self._get_user_chats(access_token)

        if chats_data:
            replied_chats = Chats.objects.filter(
                user_id=self.user_id).values_list('chat_id', flat=True)
            replied_chats = list(replied_chats)
            headers = {"Authorization": f"Bearer {access_token}"}
            json = {"message": {
                "text": self.text_message
            },
                "type": "text"
            }

            for chat in chats_data:
                if chat not in replied_chats:
                    try:
                        response = requests.post(
                            f"https://api.avito.ru/messenger/v1/accounts/{self.user_id}/chats/{chat}/messages", headers=headers, json=json)
                        if response.status_code == 200:
                            Chats.objects.create(
                                user_id=self.user_id, chat_id=chat)
                            try:
                                read_response = requests.post(
                                    f"https://api.avito.ru/messenger/v1/accounts/{self.user_id}/chats/{chat}/read", headers=headers)
                                if read_response.status_code != 200:
                                    logger.error(
                                        "Failed to send auto-read. %s", read_response.status_code)
                            except Exception as e:
                                logger.error("Error in service.auto-read: %s", str(e))
                            time.sleep(random.randint(5, 10))
                        else:
                            logger.error(
                                "Failed to send auto-reply. %s", response.status_code)
                    except Exception as e:
                        logger.error("Error in service.auto-reply: %s", str(e))
