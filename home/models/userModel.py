from django.contrib.auth.models import User, Group, Permission
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, Error

class AppUserManager(models.Manager):
    def create_user(self, username, email, password, user_level):
        new_user = User.objects.create_user(username, email, password)
        app_user = self.create(user=new_user, user_level=user_level)

        user_group = None
        if(user_level == 'SUB'):
            user_group = Group.objects.get(name='Subscribers')
        elif(user_level == 'AUT'):
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
    SUBSCRIBER = 'SUB'
    USER_LEVEL = (
        (AUTHOR, 'Author'),
        (PUBLISHER, 'Publisher'),
        (ADMIN, 'Administrator'),
        (SUBSCRIBER, 'Subscriber'),
    )
    
    user_level = models.CharField(
        max_length=3,
        choices=USER_LEVEL,
        default=SUBSCRIBER,
    )

    objects = AppUserManager()

    user_groups = {
        'Subscribers': [
            'view_article',
        ],
        'Authors': [
            'add_article',
            'change_article',
            'delete_article',
            'view_article',
        ],
        'Administrators': [
            'add_user',
            'view_user',
            'delete_user',
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
            user.save()
            return
        except ObjectDoesNotExist:
            pass

        try:
            user.publisher
            user.groups.set([Group.objects.get(name='Publishers')])
            user.save()
            return
        except ObjectDoesNotExist:
            pass

        try:
            user.admin
            user.groups.set([Group.objects.get(name='Administrators')])
            user.save()
            return
        except ObjectDoesNotExist:
            pass

    def create_user_groups(self):
        user_group = None
        for group_name, perm_list in self.user_groups.items():
            user_group = Group.objects.create(name=group_name)
            permission_list = []
            for perm_codename in perm_list:
                permision = Permission.objects.get(codename=perm_codename)
                permission_list.append(permision)
            user_group.permissions.set(permission_list)
            user_group.save()
        for user in User.objects.all():
            self.set_user_permmisions(user)

    def test_user_groups(self):
        user_group = None
        try:
            for group_name, perm_list in self.user_groups.items():
                user_group = Group.objects.get(name=group_name)
                for perm_codename in perm_list:
                    user_group.permissions.get(codename=perm_codename)
        except ObjectDoesNotExist as e:
            if(len(Group.objects.all()) > 0):
                Group.objects.all().delete()
            self.create_user_groups()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.test_user_groups()
        except Error as e:
            print('>Database Error: ', e)

    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        User.objects.get(username=self.user.username).delete()

    class Meta:
        abstract = True

def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)

class Subscriber(AppUser):
    avatar = models.ImageField(upload_to = upload_location, null = True, blank=True)
    
    FREE = 'FREE'
    PAID = 'PAID'
    SUBCRIPTIONS = (
        (FREE, FREE),
        (PAID,PAID),
    )
    
    subscription_type = models.CharField(
        max_length=4, 
        choices=SUBCRIPTIONS,
        default=FREE,
    )

class Author(AppUser):
    avatar = models.ImageField(upload_to = upload_location, null = True, blank=True)

class Publisher(AppUser):
    avatar = models.ImageField(upload_to = upload_location, null = True, blank=True)

class Admin(AppUser):
    class Meta:
        verbose_name = "administrator"
