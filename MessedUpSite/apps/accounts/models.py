from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser



class Committee(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Committees"

    def __str__(self):
        return self.name
    

class UserManager(BaseUserManager):
    def create_user(self, username:str, email:str, committees:list[str]|None, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        
        user.set_password(password)
        user.save(using=self._db)

        if committees is not None:
            for committee in committees:
                user.committees.add(Committee.objects.get(name=committee))
        else:
            user.committees.clear()

        return user

    def create_superuser(self, username:str, password:str=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username=username,
            email="admin@messedup.utwente.nl",
            committees=None,
            password=password
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(
        verbose_name="user name",
        max_length=255,
        unique=True,
    )
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    committees = models.ManyToManyField(Committee, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # If you are an admin, then yes
        if self.is_admin:
            return True
        else:
            return False

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # If you are an admin, then yes
        if self.is_admin:
            return True
        else:
            return False

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
