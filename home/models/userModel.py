"""
:synopsis: Used to define the `home.models.userModel` models
"""
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.db import Error
from django.db import models
from django.db import transaction

def upload_location(instance, filename):
    # file will be uploaded to MEDIA_ROOT/avatar/user_<id>/<filename>
    return '/avatar/user_{0}/{1}'.format(instance.user.id, filename)

def set_user_groups(user, user_level):
    """
    Set user groups using the given user level
    
    :param user: the user to set group
    :type user: django.contrib.auth.models.User
    :param str user_level: the user level string
    """
    user_group = None
    if(user_level == AppUser.SUBSCRIBER):
        user_group = Group.objects.get(name='Subscribers')
    elif(user_level == AppUser.AUTHOR):
        user_group = Group.objects.get(name='Authors')
    elif(user_level == AppUser.PUBLISHER):
        user_group = Group.objects.get(name='Publishers')
    elif(user_level == AppUser.ADMIN):
        user.is_staff = True
        user_group = Group.objects.get(name='Administrators')

    user.groups.set([user_group])
    user.save()

class AppUserManager(models.Manager):
    """
    AppUser objects manager.
    """
    @transaction.atomic
    def create(self, *args, **kwargs):
        # create object
        obj = super().create(*args, **kwargs)
        
        # set user groups
        set_user_groups(
            kwargs['user'],
            obj.user_level
        )
        
        # create and return
        return obj

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
    #: The user's telephone number.
    telephone = models.CharField(max_length=100, null=True, blank=True)
    #: The user's physical address.
    address = models.CharField(max_length=100, null=True, blank=True)
    #: The user's date of birth
    dob = models.DateField(null=True, blank=True)
    #: Timestamps
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_date_time = models.DateTimeField(auto_now=True)
    #: The user model OneToOne relationship with the AppUser.
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        unique=True, 
        blank=False, 
        editable=False
    )
    #: The user's profile picture.
    avatar = models.ImageField(
        upload_to=upload_location, 
        #height_field=250, 
        #width_field=250, 
        null=True, 
        blank=True
    )

    ADMIN = 'ADM'       #: Admin user level. Manages users.
    AUTHOR = 'AUT'      #: Author user level. Creates articles.
    PUBLISHER = 'PUB'   #: publisher user level. Publishes articles.
    SUBSCRIBER = 'SUB'  #: subscriber user level. Views articles.
    
    #: AppUser user level choices.
    USER_LEVEL = (
        (AUTHOR, 'Author'),
        (PUBLISHER, 'Publisher'),
        (ADMIN, 'Administrator'),
        (SUBSCRIBER, 'Subscriber'),
    )

    #: AppUser objects manager.
    objects = AppUserManager()

    #: The available user groups and their permissions.
    user_groups = {
        'Subscribers': [
            'view_article',
        ],
        'Authors': [
            # all permissions for articles except publish
            'add_article',
            'change_article',
            'delete_article',
            'view_article',
        ],
        'Publishers': [
            # all permissions for articles
            'add_article',
            'change_article',
            'delete_article',
            'publish_article',
            'view_article',
            # all permissions for topics
            'add_topic',
            'change_topic',
            'delete_topic',
            'view_topic',
        ],
        'Administrators': [
            # all permissions for users except edit
            'add_user',
            'view_user',
            'delete_user',
            # all permissions for publishers except edit
            'add_publisher',
            'delete_publisher',
            'view_publisher',
            #can view and delete author
            'view_author',
            'delete_author',
            # can view admin
            'view_admin',
        ],
    }

    def set_user_permmisions(self, user):
        """
        Set the user group permissions.
        
        :param user: Django user object to be set permission
        :type user: django.contrib.auth.models.User
        """
        try:
            user.subscriber
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

    @transaction.atomic
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
        # call super class method
        super().__init__(*args, **kwargs)
        
        # initial user and user_level
        self.__user = self.user
        self.__user_level = self.user_level
        
        # test user groups saved in db
        try:
            self.test_user_groups()
        except Error as e:
            print('>Database Error: ', e)

    def __str__(self):
        return self.user.username

    @transaction.atomic
    def delete(self, *args, **kwargs):
        """
        Delete the app user as well as django user model instances.
        
        calls ``super().delete(*args, **kwargs)``
        """
        self.user.delete()
        return super().delete(*args, **kwargs)

    @transaction.atomic
    def save(self, *args, **kwargs):
        """
        Prevents changing the user relationship and user levels.
        Also sets new user group.
        
        calls ``super().save(*args, **kwargs)``
        """
        # reset user to original
        if self.id and self.user != self.__user:
            self.user = self.__user
        
        # reset user_level to original
        if self.id and self.user_level != self.__user_level:
            self.user_level = self.__user_level
        
        # set user group for new AppUser
        if self.id == None:
            set_user_groups(self.user, self.user_level)
            self.__user_level = self.user_level
            self.__user = self.user

        # save and return
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = ['-created_date_time', 'updated_date_time']


class Subscriber(AppUser):
    """
    Inherits the app user.
    Should have a user level 'SUB'.
    """    
    FREE = 'FREE'           #: Free subscription type.
    PAID = 'PAID'           #: Paid subscription type.
    SPONSOR = 'SPONSOR'     #: Sponsored subscription type.
    
    #: Subscriber subscription types.
    SUBCRIPTIONS = (  
        (FREE, FREE),
        (PAID,PAID),
        (SPONSOR,SPONSOR)
    )
    
    #: The subscription types, default free.
    subscription_type = models.CharField(
        max_length=10, 
        choices=SUBCRIPTIONS,
        default=FREE,
    )
    
    #: The user's user level, read only.
    user_level = models.CharField(
        max_length=3,
        default=AppUser.SUBSCRIBER, 
        editable=False
    )


class Author(AppUser):
    """
    Inherits the app user.
    Should have a user level 'AUT'
    """
    #: The user's user level, read only.
    user_level = models.CharField(
        max_length=3,
        default=AppUser.AUTHOR, 
        editable=False
    )
    
    
class Publisher(AppUser):
    """
    Inherits the app user.
    Should have a user level 'PUB'
    """
    #: The user's user level, read only.
    user_level = models.CharField(
        max_length=3,
        default=AppUser.PUBLISHER, 
        editable=False
    )

class Admin(AppUser):
    """
    Inherits the app user.
    Should have a user level 'ADM'
    """
#: The user's user level, read only.
    user_level = models.CharField(
        max_length=3,
        default=AppUser.ADMIN, 
        editable=False
    )

    class Meta:
        verbose_name = "administrator"

