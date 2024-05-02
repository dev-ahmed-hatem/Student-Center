from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Group, Permission, BaseUserManager, User, PermissionsMixin
from django.utils import timezone


# Create your models here.


class Teacher(models.Model):
    img = models.ImageField(upload_to='teachers/')
    title = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=125)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    GRADE_CHOICES = [
        (10, 'Grade 10'),
        (11, 'Grade 11'),
        (12, 'Grade 12'),
    ]

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    video_embed_url = models.CharField(max_length=50)
    video_title = models.CharField(max_length=200)
    grade = models.IntegerField(choices=GRADE_CHOICES)

    def __str__(self):
        return self.name


class UserProfileManager(BaseUserManager):
    def create_user(self, phone, password=None):
        if not phone:
            raise ValueError('The phone number must be set')
        user = self.model(phone=phone)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None):
        user = self.create_user(phone, password)
        user.is_staff = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    lessons_registered = models.ManyToManyField(Lesson, verbose_name="Lessons Registered", blank=True)

    USERNAME_FIELD = 'phone'

    objects = UserProfileManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.phone

class Appendix(models.Model):
    name = models.CharField(max_length=100, default="")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    linkname = models.CharField(max_length=200, default="")
    linkURL = models.URLField(blank=True)
    text = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.TimeField(auto_now_add=True, verbose_name="created at")
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return f"{self.subject} from {self.name}"


class AccessCode(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    code = models.CharField(max_length=50, unique=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"Code for lesson {self.lesson}: {self.code}"
