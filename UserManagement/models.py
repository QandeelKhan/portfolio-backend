from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils.text import slugify
from django.core.files.storage import default_storage
from decouple import config
from django.core.files.storage import FileSystemStorage
from django.core.validators import EmailValidator, validate_email
from PIL import Image
# Create user manager.


USE_SPACES = config('USE_SPACES', cast=bool, default=False)
if USE_SPACES:
    fs = default_storage
else:
    fs = FileSystemStorage(location='space-resume/media')


def validate_image(image):
    try:
        img = Image.open(image)
        img.verify()
    except (IOError, SyntaxError) as e:
        raise ValidationError("Invalid image: %s" % e)

# class ProfileImagePosition(models.Model):
#     user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='profile')
#     cropped_x = models.IntegerField(default=0)
#     cropped_y = models.IntegerField(default=0)
#     cropped_width = models.IntegerField(default=0)
#     cropped_height = models.IntegerField(default=0)
#     # Add more fields as needed for image positioning

#     # ... other fields related to image adjustments


class UserManager(BaseUserManager):
    def create_user(self, email, tc, first_name, last_name, password=None, password2=None):
        """
        Creates and saves a User with the given email, name, tc and password.
        """
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            tc=tc,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, tc, password=None):
        """
        Creates and saves a superuser with the given email, name, tc
        and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            tc=tc,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


# Create a custom validator object with a custom message
custom_validator = EmailValidator(
    message="Please enter a correct email address.")


class User(AbstractBaseUser):
    # Define roles
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('regular', 'Regular'),
        # Add more roles as needed
    ]

    role = models.CharField(max_length=20,
                            choices=ROLE_CHOICES, default='regular', blank=True)
    username = None
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
        # default error msg for unique field is "user with this Email already exist."
        # default error msg for max length is i.e "Ensure this field has no more than 255 characters.",
        error_messages={
            'unique': 'This Email is already registered. Please choose a different one.',
            'max_length': 'This Email is %(show_value)s characters long. The maximum allowed length is %(limit_value)s.',
            "required": "This Field is required!"
        },
        # Add the custom validator to the validators list
        # validators=[custom_validator]
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user_slug = models.SlugField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
        help_text="A URL-friendly version of the blog post's title.",
    )
    profile_image = models.ImageField(upload_to='profile-images/',
                                      storage=fs, validators=[validate_image], null=True, blank=True)
    tc = models.BooleanField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['tc', 'first_name', 'last_name']

    def __str__(self):
        return self.email

    def clean(self):
        # Call the validate_email function with a custom message
        validate_email(
            self.email, message="%(value)s is not a valid email address.")

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_absolute_url(self):
        """
        Returns the absolute URL of the blog post.
        """
        return reverse("user:profile", kwargs={"user_slug": self.user_slug})

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def save(self, *args, **kwargs):
        if not self.user_slug:
            base_slug = slugify(self.first_name)
            self.user_slug = self.generate_unique_slug(base_slug)
        super().save(*args, **kwargs)

    def generate_unique_slug(self, base_slug):
        slug = base_slug
        suffix = 1
        while User.objects.filter(user_slug=slug).exists():
            slug = f'{base_slug}-{suffix}'
            suffix += 1
        return slug
