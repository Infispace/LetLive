"""
:synopsis: Used to define the `home.models.userModel` models
"""
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.core.exceptions import ObjectDoesNotExist
from django.db import Error
from django.db import models
from django.db import transaction

def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)
    
class AppUserManager(models.Manager):
    """
    AppUser objects manager.
    """
    @transaction.atomic
    def create_user(self, username, email, password, user_level):
        """
        Creates an app user using the given user level.
        
        :param str username: the user's user name
        :param str email: the user's email
        :param str password: the user's password
        :param str user_level: one of user's user name
        :return: the new user object
        :rtype: home.models.userModel.AppUser
        """
        new_user = None
        new_user = User.objects.create_user(username, email, password)
        app_user = self.create(user=new_user, user_level=user_level)

        user_group = None
        if(user_level == AppUser.SUBSCRIBER):
            user_group = Group.objects.get(name='Subscribers')
        elif(user_level == AppUser.AUTHOR):
            user_group = Group.objects.get(name='Authors')
        elif(user_level == AppUser.PUBLISHER):
            user_group = Group.objects.get(name='Publishers')
        elif(user_level == AppUser.ADMIN):
            new_user.is_staff = True
            user_group = Group.objects.get(name='Administrators')
        elif(user_level == AppUser.SUPER_USER):
            new_user.is_superuser = True
            user_group = Group.objects.get(name='Super_users')

        new_user.groups.set([user_group])
        new_user.save()

        return app_user

class AppUser(models.Model):
    """
    Virtual object for the app user. 
    Has one to one relationship with django auth user.
    
    It is inherited by the models:
    
    * home.models.userModel.Admin
    * home.models.userModel.Author
    * home.models.userModel.Subscriber
    * home.models.userModel.Publisher
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, blank=False)
    telephone = models.CharField(max_length=100, null = True, blank=True)
    address = models.CharField(max_length=100, null = True, blank=True)

    ADMIN = 'ADM'       #: Admin user level.
    AUTHOR = 'AUT'      #: Author user level.
    PUBLISHER = 'PUB'   #: publisher user level.
    SUBSCRIBER = 'SUB'  #: subscriber user level.
    SUPER_USER = 'SU'   #: `'super user'` user level.
    
    #: AppUser user levels
    USER_LEVEL = (
        (AUTHOR, 'Author'),
        (PUBLISHER, 'Publisher'),
        (ADMIN, 'Administrator'),
        (SUBSCRIBER, 'Subscriber'),
        (SUPER_USER, 'Super_user'),
    )
    
    user_level = models.CharField(
        max_length=3,
        choices=USER_LEVEL,
        default=SUBSCRIBER,
    )

    #: AppUser objects manager.
    objects = AppUserManager()

    #: The available user groups and their permissions.
    user_groups = {
        'Super_users': [],
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
            'view_article',
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
        """
        Set the user group permissions.
        
        :param user: Django user object to be set permission
        :type user: django.contrib.auth.models.User
        """
        try:
            user.admin
            user.groups.set([Group.objects.get(name='Subscribers')])
            user.save()
            return
        except ObjectDoesNotExist:
            pass
            
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
        """
        Create and store the available user groups.
        """
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
        """
        Verify if the user groups are available in the database.
        """
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
        """
        Delete the app user as well as django user model instances.
        
        calls ``super().delete(*args, **kwargs)``
        """
        super().delete(*args, **kwargs)
        User.objects.get(username=self.user.username).delete()

    class Meta:
        abstract = True

class Subscriber(AppUser):
    """
    Inherits the app user.
    Should have a user level 'SUB'
    """
    avatar = models.ImageField(upload_to = upload_location, null = True, blank=True)
    
    FREE = 'FREE'     #: Free subscription type
    PAID = 'PAID'     #: Paid subscription type
    
    #: Subscriber subscription types
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
    """
    Inherits the app user.
    Should have a user level 'AUT'
    """
    avatar = models.ImageField(upload_to = upload_location, null = True, blank=True)

class Publisher(AppUser):
    """
    Inherits the app user.
    Should have a user level 'PUB'
    """
    avatar = models.ImageField(upload_to = upload_location, null = True, blank=True)

class Admin(AppUser):
    """
    Inherits the app user.
    Should have a user level 'ADM'
    """
    class Meta:
        verbose_name = "administrator"

