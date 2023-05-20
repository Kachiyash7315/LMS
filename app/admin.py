from django.contrib import admin

from app.models import Categories, Lesson, Video, UserCourse, Payment, Question, Result, Student, Subscribe

from app.models import Author, Course, level, what_will_you_learn, Requirement


class what_will_you_learn_TabularInline(admin.TabularInline):
    model = what_will_you_learn


class Requirements_TabularInline(admin.TabularInline):
    model = Requirement


class Video_TabularInline(admin.TabularInline):
    model = Video


class course_admin(admin.ModelAdmin):
    inlines = (what_will_you_learn_TabularInline, Requirements_TabularInline, Video_TabularInline)


# Register your models here.
admin.site.register(Categories)
admin.site.register(Author)
admin.site.register(Course, course_admin)
admin.site.register(level)
admin.site.register(what_will_you_learn)
admin.site.register(Requirement)
admin.site.register(Lesson)
admin.site.register(UserCourse)
admin.site.register(Video)
admin.site.register(Payment)
admin.site.register(Question)
admin.site.register(Student)
admin.site.register(Result)
admin.site.register(Subscribe)