"""LMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views, user_login

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('404', views.PAGE_NOT_FOUND, name='404'),
                  path('verify_payment', views.VERIFY_PAYMENT, name='verify_payment'),
                  path('base', views.BASE, name='base'),
                  path('', views.HOME, name='home'),
                  path('courses', views.SINGLE_COURSE, name='single_course'),
                  path('courses/filter-data', views.filter_data, name="filter-data"),
                  path('course/<slug:slug>', views.COURSE_DETAILS, name='course_details'),
                  path('search', views.SEARCH_COURSE, name="search_course"),
                  path('contact/us', views.CONTACT_US, name='contact_us'),
                  path('about/us', views.ABOUT_US, name='about_us'),
                  path('accounts/', include('django.contrib.auth.urls')),  # use accounts/login
                  path('accounts/register', user_login.REGISTER, name='register'),
                  path('dologin', user_login.DO_LOGIN, name='dologin'),
                  path('accounts/profile', user_login.PROFILE, name='profile'),
                  path('checkout/<slug:slug>', views.CHECKOUT, name='checkout'),
                  path('my_course', views.MY_COURSE, name='my_course'),
                  path('become-instructor', views.BECOME_INSTRUCTOR, name='become-instructor'),
                  path('instructor-list', views.INSTRUCTOR_LIST, name='instructor-list'),
                  path('course/watch_course/<slug:slug>', views.WATCH_COURSE, name='watch_course'),
                  path('accounts/profile/update', user_login.PROFILE_UPDATE, name='profile_update'),

                  # admin
                  path('oes', views.VIEW_HOME, name='oes'),
                  path('afterlogin', views.afterlogin_view, name='afterlogin'),

                  # student
                  path('student-exam', views.STUDENT_EXAM_VIEW, name='student-exam'),
                  path('take-exam/<int:pk>', views.TAKE_EXAM_VIEW, name='take-exam'),
                  path('start-exam/<int:pk>', views.START_EXAM_VIEW, name='start-exam'),
                  path('calculate-marks', views.calculate_marks_view, name='calculate-marks'),
                  path('view-result', views.view_result_view, name='view-result'),
                  path('check-marks/<int:pk>', views.check_marks_view, name='check-marks'),
                  # path('point', views.points, name='point'),
                  path('subscribe', views.SUBSCRIBE, name='subscribe'),
                  path('compiler_dashboard',views.COMPILER_DASHBOARD,name='compiler_dashboard'),
                  path('java',views.JAVA, name='java'),
                  path('cpp', views.CPP, name='cpp'),
                  path('python', views.PYTHON, name='python'),
                  path('sql', views.SQL, name='sql'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
