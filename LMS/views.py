from time import time
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
import razorpay
from django.views.decorators.csrf import csrf_exempt

from .settings import *

client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))

from django.db.models import Sum
from app.models import Categories, Video, UserCourse, Payment, Question, Student, Result, Subscribe

from app.models import Course, level
from django.template.loader import render_to_string


def BASE(request):
    return render(request, 'base.html')


def HOME(request):
    category = Categories.objects.all().order_by('id')[0:12]
    course = Course.objects.filter(status='PUBLISH').order_by('id')
    return render(request, 'Main/home.html', context={
        'category': category,
        'course': course,
    })


def SINGLE_COURSE(request):
    category = Categories.get_all_category(Categories)
    level2 = level.objects.all()
    course = Course.objects.all()
    freeCourseCount = Course.objects.filter(price=0).count()
    paidCourseCount = Course.objects.filter(price__gte=1).count()
    context = {
        'category': category,
        'level': level2,
        'course': course,
        'freeCourseCount': freeCourseCount,
        'paidCourseCount': paidCourseCount
    }
    return render(request, 'Main/single_course.html', context)


def filter_data(request):
    category = request.GET.getlist('category[]')
    level = request.GET.getlist('level[]')
    price = request.GET.getlist('price[]')
    if price == ['priceFree']:
        course = Course.objects.filter(price=0)
    elif price == ['pricePaid']:
        course = Course.objects.filter(price__gte=1)
    elif price == ['priceAll']:
        course = Course.objects.all()
    elif category:
        course = Course.objects.filter(category__id__in=category).order_by('-id')
    elif level:
        course = Course.objects.filter(level__id__in=level).order_by('-id')
    else:
        course = Course.objects.all().order_by('-id')
    # print(course)
    context = {
        'course': course
    }
    t = render_to_string('ajax/course.html', {'course': course})
    return JsonResponse({'data': t})


def SEARCH_COURSE(request):
    category = Categories.get_all_category(Categories)
    # context = {
    #     'category': category
    # }
    # if request.method == 'get':
    query = request.GET['query']
    course = Course.objects.filter(title__icontains=query)
    context = {
        'course': course,
        'category': category
    }
    return render(request, 'search/search.html', context)


def COURSE_DETAILS(request, slug):
    category = Categories.get_all_category(Categories)
    time_duration = Video.objects.filter(course__slug=slug).aggregate(sum=Sum('time_duration'))
    course_id = Course.objects.get(slug=slug)
    try:
        checkenroll = UserCourse.objects.get(user=request.user.id, course=course_id)
    except UserCourse.DoesNotExist:
        checkenroll = None
    course = Course.objects.filter(slug=slug)
    if course.exists():
        course = course.first()
    else:
        return redirect('404')
    context = {
        'course': course,
        'category': category,
        'time_duration': time_duration,
        'checkenroll': checkenroll
    }
    return render(request, 'course/course_details.html', context)


def CONTACT_US(request):
    category = Categories.get_all_category(Categories)
    context = {
        'category': category
    }
    return render(request, 'Main/contact_us.html', context)


def ABOUT_US(request):
    category = Categories.get_all_category(Categories)
    context = {
        'category': category
    }
    return render(request, 'Main/about_us.html', context)


def PAGE_NOT_FOUND(request):
    category = Categories.get_all_category(Categories)
    context = {
        'category': category
    }
    return render(request, 'error/404.html', context)

@login_required()
def CHECKOUT(request, slug):
    order = None
    action = request.GET.get('action')
    course = Course.objects.get(slug=slug)
    context = {
        'course': course
    }
    if course.price == 0:
        course = UserCourse(user=request.user, course=course)
        course.save()
        messages.success(request, "Course is successfully enrolled")
        # return redirect('my_course')
        return render(request, 'my_course.html', context)

    elif action == 'create_payment':
        if request.method == "POST":
            first_name = request.POST.get('billing_first_name')
            last_name = request.POST.get('billing_last_name')
            country = request.POST.get('billing_country')
            address_1 = request.POST.get('billing_address_1')
            address_2 = request.POST.get('billing_address_2')
            city = request.POST.get('billing_city')
            state = request.POST.get('billing_state')
            postcode = request.POST.get('billing_postcode')
            phone = request.POST.get('billing_phone')
            email = request.POST.get('billing_email')
            order_comments = request.POST.get('billing_order_comments')
            amount_cal = course.price - (course.price * course.discount / 100)
            amount = int(amount_cal) * 100
            currency = "INR"
            notes = {
                'name': f'{first_name} {last_name}',
                'country': country,
                'address': f'{address_1} {address_2}',
                'city': city,
                'state': state,
                'postcode': postcode,
                'phone': phone,
                'email': email,
                'order_comments': order_comments
            }
            receipt = f"SKola-{int(time())}"
            order = client.order.create({
                'receipt': receipt,
                'notes': notes,
                'amount': amount,
                'currency': currency
            })
            payment = Payment(
                course=course,
                user=request.user,
                order_id=order.get('id')
            )
            payment.save()

    context = {
        'course': course,
        'order': order,
    }
    return render(request, 'checkout/checkout.html', context)

    # return render(request, 'Main/home.html', context)


def MY_COURSE(request):
    course = UserCourse.objects.filter(user=request.user)
    context = {
        'course': course
    }
    return render(request, 'course/my_course.html', context)


@csrf_exempt
@login_required()
def VERIFY_PAYMENT(request):
    if request.method == 'POST':
        data = request.POST
        print("payment", data)
        try:
            client.utility.verify_payment_signature(data)
            razorpay_order_id = data['razorpay_order_id']
            razorpay_payment_id = data['razorpay_order_id']
            payment = Payment.objects.get(order_id=razorpay_order_id)
            payment.payment_id = razorpay_payment_id
            payment.status = True

            usercourse = UserCourse(
                user=payment.user,
                course=payment.course,
            )
            usercourse.save()
            payment.user_course = usercourse
            payment.save()

            context = {
                'data': data,
                'payment': payment
            }
            print(context)
            return render(request, 'verify_payment/success.html', context)
        except:
            return render(request, 'verify_payment/next.html')

    return None


def WATCH_COURSE(request, slug):
    lecture = request.GET.get('lecture')
    # course_id = Course.objects.get(slug=slug)
    video = Video.objects.filter(id=lecture)

    course = Course.objects.filter(slug=slug)
    # try:
    #     checkenroll = UserCourse.objects.get(user=request.user,course=course_id)
    #     video = Video.objects.get(id=lecture)
    if course.exists():
        course = course.first()
    else:
        return redirect('404')
    # except UserCourse.DoesNotExist:
    #     return redirect('404')

    context = {
        'course': course,
        'video': video,
        # 'lecture': lecture
    }
    return render(request, 'course/watch_course.html', context)


def BECOME_INSTRUCTOR(request):
    return render(request, 'instructor/instructor.html')


def INSTRUCTOR_LIST(request):
    course = Course.objects.all()
    context = {
        'course': course
    }
    print("courses are", course)
    return render(request, 'instructor/instructor-list.html', context)


# ADMIN

def VIEW_HOME(request):
    # if request.user.is_authenticated:
    #     return HttpResponseRedirect('afterlogin')
    return render(request, 'oes/index.html')


# def is_student(user):
#     return user.groups.filter(name='STUDENT').exists()


def afterlogin_view(request):
    courses = Course.objects.all()
    usercourse = UserCourse.objects.filter(user=request.user)
    student = Student.objects.filter(user=request.user)
    context = {
        'usercourse': usercourse,
        'courses': courses,
        'student': student
    }
    return render(request, 'student/student-dashboard.html', context)


def STUDENT_EXAM_VIEW(request):
    # courses = QMODEL.Course.objects.all()
    courses = Course.objects.all()
    return render(request, 'student/student_exam.html', {'courses': courses})


def TAKE_EXAM_VIEW(request, pk):
    course = Course.objects.get(id=pk)
    total_questions = Question.objects.all().filter(course=course).count()
    questions = Question.objects.all().filter(course=course)
    total_marks = 0
    for q in questions:
        total_marks = total_marks + q.marks

    return render(request, 'student/take_exam.html',
                  {'course': course, 'total_questions': total_questions, 'total_marks': total_marks})


def START_EXAM_VIEW(request, pk):
    course = Course.objects.get(id=pk)
    questions = Question.objects.all().filter(course=course)
    if request.method == 'POST':
        pass
    response = render(request, 'student/start_exam.html', {'course': course, 'questions': questions})
    response.set_cookie('course_id', course.id)
    return response


def calculate_marks_view(request):
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course = Course.objects.get(id=course_id)

        total_marks = 0
        # points = 0
        questions = Question.objects.all().filter(course=course)
        for i in range(len(questions)):

            selected_ans = request.COOKIES.get(str(i + 1))
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks
        student = Student.objects.get(user_id=request.user.id)
        result = Result()
        # result = QMODEL.Result()
        result.marks = total_marks
        result.exam = course
        result.student = student
        result.points = result.marks / 10
        result.save()
        context = {
            'result':result
        }
        print("Res are",result)
        return HttpResponseRedirect('view-result',result)


def view_result_view(request):
    courses = Course.objects.all()
    return render(request, 'student/view_result.html', {'courses': courses})


def check_marks_view(request, pk):
    course = Course.objects.get(id=pk)
    student = Student.objects.get(user_id=request.user.id)
    results = Result.objects.all().filter(exam=course).filter(student=student)

    return render(request, 'student/check_marks.html', {'results': results})


#
#
# def points(request):
#     result = calculate_marks_view(request)
#
#     points = 10
#     print("Points are guys", points)
#     context = {
#         'points': points,
#
#     }
#     return render(request, 'Main/home.html', context)

def SUBSCRIBE(request):
    if request.method == "POST":
        email = request.POST.get('email')
        subscribe = Subscribe(email=email)
        subscribe.save()

        messages.success(request, "Thank you for subscribing the newsletter")
        return render(request, 'Main/home.html')


def JAVA(request):
    return render(request, 'compiler/java.html')


def CPP(request):
    return render(request, 'compiler/cpp.html')


def PYTHON(request):
    return render(request, 'compiler/python.html')


def SQL(request):
    return render(request, 'compiler/sql.html')


def COMPILER_DASHBOARD(request):
    return render(request, 'compiler/compiler_dashboard.html')
