from django.core.management import BaseCommand
from shortener.models import User

import urllib.request
import json


class Command(BaseCommand):
    help = "My test command"

    def add_arguments(self, parser):
        """Add the count argument to the command."""
        parser.add_argument('count', nargs='+', type=int)
# A command must define handle()

    def handle(self, *args, **options):
        """Get the number of fake users. default is 10."""
        default_num = 10
        option_count = options["count"][0]
        if option_count > 0:
            get_and_save(option_count)
        else:
            get_and_save(default_num)


def get_and_save(number_of_users):
    """Connect to the API and creating the users."""
    serviceurl = "https://randomuser.me/api/?"
    url = serviceurl + urllib.parse.urlencode(
        {'results': str(number_of_users)})

    with urllib.request.urlopen(url) as response:
        data = response.read()
        try:
            js = json.loads(data)
        except:
            js = None
        for i, user_dict in enumerate(js['results']):
            user = User.objects.create_user(user_dict["login"]["username"])
            user.first_name = user_dict["name"]["first"]
            user.last_name = user_dict["name"]["last"]
            user.email = user_dict["email"]
            user.password = user_dict["login"]["password"]
            user.save()
            # print("First Name= ", user_dict["name"]["first"])
            # print("Last Name= ", user_dict["name"]["last"])
            # print("Email= ", user_dict["email"])
            # print("Username= ", user_dict["login"]["username"])
            # print("Password= ", user_dict["login"]["password"])
        print(number_of_users, "Users have been created!")
        # print(json.dumps(js, indent=4))
