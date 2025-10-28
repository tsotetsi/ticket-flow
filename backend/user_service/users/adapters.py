from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings

class CustomAccountAdapter(DefaultAccountAdapter):
    def send_password_reset_mail(self, user, email, context):
        # Ensure the context contains the correct uid and key.
        context['password_reset_url'] = (
            f"{settings.FRONTEND_URL}/password/reset/key/{context['uid']}/{context['key']}/"
        )
        super().send_password_reset_mail(user, email, context)