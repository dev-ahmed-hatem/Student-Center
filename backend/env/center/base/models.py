from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    name = models.CharField(max_length=50, default="")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username


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
