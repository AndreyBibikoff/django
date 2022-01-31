from authapp.models import ShopUser, ShopUserProfile
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = ShopUser.objects.all()
        for i in users:
            user_profile = ShopUserProfile.objects.create(user=i)
            user_profile.save()