from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

#Generate unique token for activation of account
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user,timestamp) -> str:
        return six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)

account_activation_token = AccountActivationTokenGenerator()