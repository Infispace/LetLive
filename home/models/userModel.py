from django.contrib.auth.models import User, Group
from django.db import models

class AppUserManager(models.Manager):
    def create_user(self, username, email, password, user_level):
        new_user = User.objects.create_user(username, email, password)
        app_user = self.create(user=new_user, user_level=user_level)

        user_group = None
        if(user_level == 'AUT'):
            user_group = Group.objects.get(name='Authors')
        elif(user_level == 'PUB'):
            user_group = Group.objects.get(name='Publishers')
        elif(user_level == 'ADM'):
            new_user.is_staff = True
            user_group = Group.objects.get(name='Administrators')

        new_user.groups.set([user_group])
        new_user.save()
        return new_user

class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    telephone = models.IntegerField(null = True, blank=True)
    address = models.CharField(max_length=100, null = True)

    AUTHOR = 'AUT'
    PUBLISHER = 'PUB'
    ADMIN = 'ADM'
    USER_LEVEL = (
        (AUTHOR, 'Author'),
        (PUBLISHER, 'Publisher'),
        (ADMIN, 'Admin'),
    )
    user_level = models.CharField(
        max_length=3,
        choices=USER_LEVEL,
        default=AUTHOR,
    )

    objects = AppUserManager()
    class Meta:
        abstract = True

    def __str__(self):
        return self.user.username

def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)


class Author(AppUser):
    avatar = models.ImageField(upload_to = upload_location, null = True, blank=True)

class Publisher(AppUser):
    avatar = models.ImageField(upload_to = upload_location, null = True, blank=True)

class Admin(AppUser):

    class Meta:
        verbose_name = "Administrator"
