from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save


# Create your models here.
class Categories(models.Model):
    icon = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.name

    def get_all_category(self):
        return Categories.objects.all().order_by('id')


class Author(models.Model):
    author_profile = models.ImageField(upload_to='Media/author')
    name = models.CharField(max_length=100, null=True)
    about_author = models.TextField()

    def __str__(self):
        return self.name


class level(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Course(models.Model):
    STATUS = (
        ('PUBLISH', 'PUBLISH'),
        ('PUBLISH', 'PUBLISH'),
    )

    featured_image = models.ImageField(upload_to='Media/featured_img', null=True)
    featured_video = models.CharField(max_length=300, null=True)
    title = models.CharField(max_length=500)
    created_at = models.DateField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    level = models.ForeignKey(level, max_length=100, on_delete=models.CASCADE, null=True)
    description = models.TextField()
    price = models.IntegerField(null=True, default=0)
    discount = models.IntegerField(null=True)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)
    status = models.CharField(choices=STATUS, max_length=100, null=True)
    certificate = models.CharField(null=True, max_length=100)
    question_number = models.PositiveIntegerField(null=True)
    total_marks = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("course_details", kwargs={'slug': self.slug})


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Course.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, Course)


class what_will_you_learn(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    points = models.CharField(max_length=500)

    def __str__(self):
        return self.points


class Requirement(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    points = models.CharField(max_length=500)

    def __str__(self):
        return self.points


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name + " - " + self.course.title
class Question(models.Model):
    question_id = models.IntegerField(auto_created=True,null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    question = models.CharField(max_length=600)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    cat = (('Option1', 'Option1'), ('Option2', 'Option2'), ('Option3', 'Option3'), ('Option4', 'Option4'))
    answer = models.CharField(max_length=200, choices=cat)

    def __str__(self):
        return self.course.title + "--------------------------------------------------------------------------------------------" + self.question


class Video(models.Model):
    serial_number = models.IntegerField(null=True)
    thumbnail = models.ImageField(upload_to="Media/Ty_Thumbnail", null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    youtube_id = models.CharField(max_length=200)
    time_duration = models.FloatField(null=True)
    preview = models.BooleanField(default=False)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.title


class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    paid = models.BooleanField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name + " - " + self.course.title


class Payment(models.Model):
    order_id = models.CharField(max_length=100, null=True, blank=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    user_course = models.ForeignKey(UserCourse, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name + "--" + self.course.title


# EXAM MODELS




class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/Student/', null=True, blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=False)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_instance(self):
        return self

    def __str__(self):
        return self.user.first_name


class Result(models.Model):

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)
    points = models.FloatField(null=True)

    @property
    def get_name(self):
        return self.student.user.username

    @property
    def get_instance(self):
        return self

    def __str__(self):
        return self.student.user.username


class Subscribe(models.Model):
    email = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.email
