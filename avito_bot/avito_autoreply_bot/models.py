from django.db import models


class Users(models.Model):
    user_id = models.CharField(
        max_length=50, verbose_name='user_id', unique=True, blank=True, null=True, default='')

    def __str__(self):
        return self.user_id

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Profiles(models.Model):
    profiles_id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=50, verbose_name='name', blank=True, null=True)
    client_id = models.CharField(
        max_length=50, verbose_name='client_id', blank=True, null=True)
    client_secret = models.CharField(
        max_length=50, verbose_name='client_secret', blank=True, null=True)
    user_id = models.ForeignKey(
        Users, on_delete=models.CASCADE, verbose_name='user_id', null=True)
    text_message = models.TextField(
        verbose_name='text_message', blank=True, null=True)
    paid = models.BooleanField(
        verbose_name='paid', blank=True, null=True, default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.paid and self.pk:
            from .service import AvitoAutoreplyBot
            avito_bot = AvitoAutoreplyBot(
                client_id=self.client_id,
                client_secret=self.client_secret,
                user_id=self.user_id,
                text_message=self.text_message
            )
            avito_bot.get_access_token()


class Chats(models.Model):
    user_id = models.ForeignKey(
        Users, on_delete=models.CASCADE, verbose_name='user_id', null=True)
    chat_id = models.CharField(
        max_length=50, verbose_name='chat_id', blank=True, null=True)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.created_timestamp)

    class Meta:
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'


class AccessTokens(models.Model):
    user_id = models.CharField(
        max_length=50, verbose_name='user_id', blank=True, null=True)
    access_token = models.CharField(
        max_length=50, verbose_name='access_token', blank=True, null=True)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_id

    class Meta:
        verbose_name = 'Token'
        verbose_name_plural = 'Tokens'
