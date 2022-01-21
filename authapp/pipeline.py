from collections import OrderedDict
from urllib.parse import urlunparse, urlencode
import requests
from authapp.models import ShopUserProfile, ShopUser


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse(('https',
                          'api.vk.com',
                          '/method/users.get',
                          None,
                          urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'photo_200', 'city')),
                                                access_token=response['access_token'], v='5.131')),
                          None
                          ))

    resp = requests.get(api_url)


    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]
    if data['sex']:
        user.shopuserprofile.gender = ShopUserProfile.MALE if data['sex'] == 2 else ShopUserProfile.FEMALE

    if data['about']:
        user.shopuserprofile.about_me = data['about']

    if data['city']:
        user.shopuserprofile.city = data['city']['title']

    if data['photo_200']:
        user.social_login = True
        user.avatar = data['photo_200']

    user.save()
