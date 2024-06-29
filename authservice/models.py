from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User
from django.contrib.auth.password_validation import validate_password
# Create your models here.


class CustomManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, and password.
        """
        if not email:
            raise ValueError("Users must have a valid email address ")
        user = self.model(
            email=self.normalize_email(email),
           
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, and password.
        """
        if not email:
            raise ValueError("Users must have a valid email address ")
        
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
        raise ValueError("Users must have a valid email address ")


class CustomUser(AbstractBaseUser, PermissionsMixin): 
    full_name = models.CharField(max_length= 255, default= 'Anyname')
    email = models.EmailField(
        verbose_name="email address",
        max_length= 255,
        unique=True,
        )
    verified = models.BooleanField(default=False)
    phone_number = models.IntegerField(default= '12345')
    password = models.CharField(max_length=255,default='defaultpassword')
    address = models.TextField(null= True)
    is_active = models.BooleanField(default= True)
    is_admin = models.BooleanField(default=False)


    objects = CustomManager()

    USERNAME_FIELD = "email"
    #REQUIRED_FIELDS = ["phone_number"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class UserProfile(models.Model):
    user = models.OneToOneField("CustomUser", on_delete=models.CASCADE) # every profile must belong one to user
    bio = models.TextField(null=True)

    #pass1 = ebubaJohn