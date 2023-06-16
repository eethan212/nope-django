from django.core.management.base import BaseCommand

from nope.accounts.models import User


data = [
    {"username": "tjm32019601", "name": "南京高新区（江北新区）"},
    {"username": "tjm32019603", "name": "南京高新区（江宁国家高新园）"},
    {"username": "tjm32019604", "name": "南京高新区（江宁园）"},
    {"username": "tjm32019605", "name": "南京高新区（玄武园）"},
    {"username": "tjm32019606", "name": "南京高新区（秦淮园）"},
    {"username": "tjm32019607", "name": "南京高新区（高淳园）"},
    {"username": "tjm32019608", "name": "南京高新区（麒麟园）"},
    {"username": "tjm32019609", "name": "南京高新区（建邺园）"},
    {"username": "tjm32019610", "name": "南京高新区（鼓楼园）"},
    {"username": "tjm32019612", "name": "南京高新区（雨花台园）"},
    {"username": "tjm32019614", "name": "南京高新区（六合园）"},
    {"username": "tjm32019615", "name": "南京高新区（溧水园）"},
    {"username": "tjm32019611", "name": "南京高新区（栖霞园）"},
    {"username": "tjm32019602", "name": "南京高新区（新港高新园）"},
    {"username": "tjm32019613", "name": "南京高新区（浦口园）"}
]


class Command(BaseCommand):
    help = 'add admin command'

    def handle(self, *args, **options):
        for item in data:
            print(f'adding {item["username"]}')
            user = User.objects.create(username=item['username'], role='admin')
            user.set_password(item['username'])
            user.save()
