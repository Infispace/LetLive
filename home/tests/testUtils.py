from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django_seed import Seed


class TestUtils ():
    """
    Common test utilities for LetLive test cases.
    
    Includes:
    
    * seeder
    * create_password()
    * create_username()
    """
    seeder = Seed.seeder()       #: django-seed instance

    def create_password(self):
        """
        Create a valid password.
        """
        password = ''
        while (len(password) < 8):
            password += self.seeder.faker.word()

        return password

    def create_username(self):
        """
        Create a non_used username.
        """    
        # user username
        username = ''
        while (username.strip() == ''):
            try:
                username = self.seeder.faker.first_name()
                user = User.objects.get(username=username)
            except ObjectDoesNotExist:
                pass
            else:
                username = ''

        return username

