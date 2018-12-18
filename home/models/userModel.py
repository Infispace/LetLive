from django.contrib.auth.models import User, Group, Permission
from django.core.exceptions import ObjectDoesNotExist
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
    address = models.CharField(max_length=100, null = True, blank=True)

    AUTHOR = 'AUT'
    PUBLISHER = 'PUB'
    ADMIN = 'ADM'
    USER_LEVEL = (
        (AUTHOR, 'Author'),
        (PUBLISHER, 'Publisher'),
        (ADMIN, 'Administrator'),
    )
    user_level = models.CharField(
        max_length=3,
        choices=USER_LEVEL,
        default=AUTHOR,
    )

    objects = AppUserManager()

    user_groups = {
        'Authors': [
            'add_article',
            'change_article',
            'delete_article',
            'view_article',
        ],
        'Administrators': [
            'add_publisher',
            'delete_publisher',
            'view_publisher',
            'view_admin',
            'view_author',
            'delete_author',
        ],
        'Publishers': [
            'add_article',
            'change_article',
            'delete_article',
            'publish_article',
            'view_article',
            'add_topic',
            'change_topic',
            'delete_topic',
            'view_topic',
        ],
    }

    def set_user_permmisions(self, user):
        try:
            user.author
            user.groups.set([Group.objects.get(name='Authors')])
        except ObjectDoesNotExist:
            pass

        try:
            user.publisher
            user.groups.set([Group.objects.get(name='Publishers')])
        except ObjectDoesNotExist:
            pass

        try:
            user.admin
            user.groups.set([Group.objects.get(name='Administrators')])
        except ObjectDoesNotExist:
            pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_group = None
        try:
            for group_name, perm_list in self.user_groups.items():
                user_group = Group.objects.get(name=group_name)
                for perm_codename in perm_list:
                    user_group.permissions.get(codename=perm_codename)
        except Exception as e:
            Group.objects.all().delete()
            for group_name, perm_list in self.user_groups.items():
                user_group = Group.objects.create(name=group_name)
                permission_list = []
                for perm_codename in perm_list:
                    perm = Permission.objects.get(codename=perm_codename)
                    permission_list.append(perm)

                user_group.permissions.set(permission_list)
                user_group.save()

            for user in User.objects.all():
                self.set_user_permmisions(user)

    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        User.objects.get(username=self.user.username).delete()

    class Meta:
        abstract = True

def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)

class Author(AppUser):
    avatar = models.ImageField(upload_to = upload_location, null = True, blank=True)

class Publisher(AppUser):
    avatar = models.ImageField(upload_to = upload_location, null = True, blank=True)

class Admin(AppUser):
    class Meta:
        verbose_name = "Administrator"
