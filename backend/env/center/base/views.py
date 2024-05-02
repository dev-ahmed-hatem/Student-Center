from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import UserRegistrationForm
from .models import Teacher, Lesson, Appendix, ContactMessage, AccessCode, UserProfile
from django.http import JsonResponse, HttpResponse
from django.utils.timezone import localtime, timedelta
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User


# Create your views here.
def home(request):
    teachers = Teacher.objects.all()
    return render(request, 'base/home.html', context={"teachers": teachers})


def about(request):
    return render(request, 'base/about.html')


def contact(request):
    return render(request, 'base/contact.html')


@login_required
def teacher(request, pk):
    teacher_ = Teacher.objects.get(id=pk)
    grade10 = Lesson.objects.filter(teacher=teacher_, grade=10)
    grade11 = Lesson.objects.filter(teacher=teacher_, grade=11)
    grade12 = Lesson.objects.filter(teacher=teacher_, grade=12)
    return render(request, 'base/teacher.html', context={"teacher": teacher_,
                                                         "grade10": grade10,
                                                         "grade11": grade11,
                                                         "grade12": grade12, })


@login_required
def lesson(request, pk):
    lesson_ = Lesson.objects.get(id=pk)
    try:
        request.user.lessons_registered.get(id=pk)
        appendices = Appendix.objects.filter(lesson=lesson_)
        return render(request, 'base/lesson.html', context={"registered": True, "lesson": lesson_,
                                                            "appendices": appendices})
    except:
        return render(request, 'base/lesson.html', context={"registered": False, "lesson": lesson_})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == 'POST':
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        remember = request.POST.get("remember")
        user = authenticate(request=request, phone=phone, password=password)
        if user is not None:
            login(request, user)
            if remember:
                request.session.set_expiry(2592000)
            next_url = request.GET.get("next", "home")
            return redirect(next_url)
        else:
            return render(request, 'base/sign-in.html', context={"error": "اسم المستخدم أو كلمة المرور غير صحيحة"})

    else:
        return render(request, 'base/sign-in.html')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            phone = form.cleaned_data.get("phone")
            password = form.cleaned_data.get("password1")
            user = authenticate(phone=phone, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        else:
            return render(request, 'base/sign-up.html',
                          context={"error": f"رقم الموبايل  ( {request.POST.get('phone')} )   مسجل بالفعل",
                                   "name": request.POST.get("name"),
                                   "phone": request.POST.get("phone")})
    return render(request, 'base/sign-up.html')


def logout_view(request):
    logout(request)
    return redirect("login")


def recieve_contact_message(request):
    if request.method == 'POST':
        # Get form data from POST request
        ip_address = request.META.get('REMOTE_ADDR')

        # Check if a message has been sent by this IP address within the last minute
        last_minute = localtime() - timedelta(minutes=15)
        objects = ContactMessage.objects.filter(ip_address=ip_address, created_at__gte=last_minute)
        messages_sent = objects.count()

        if messages_sent >= 1:
            # Return error response if message has been sent within the last minute
            return JsonResponse({'status': 'error',
                                 'message': 'لقد قمت بالفعل بإرسال رسالة خلال آخر 15 دقيقة. الرجاء معاودة المحاولة في وقت لاحق.'})
        else:
            name = request.POST.get('name')
            phone_number = request.POST.get('phone-number')
            subject = request.POST.get('subject')
            message = request.POST.get('message')

            # Create ContactMessage object and save it to the database
            contact_message = ContactMessage(name=name, phone_number=phone_number, subject=subject, message=message,
                                             ip_address=ip_address)
            contact_message.save()

            # Return success response
            return JsonResponse({'status': 'success', 'message': 'تم إرسال رسالتك!'})
    else:
        # Return error response if request method is not POST
        return JsonResponse(
            {'status': 'error', 'message': 'حدث خطأ أثناء إرسال الرسالة. الرجاء معاودة المحاولة في وقت لاحق.'})


@staff_member_required
def access_codes(request):
    lessons = Lesson.objects.all()
    codes = AccessCode.objects.filter(lesson=lessons[0])
    return render(request, "base/access-codes.html", context={"lessons": lessons, "codes": codes})


def get_lesson_coodes(request, lessonID):
    lesson = Lesson.objects.get(id=lessonID)
    codes = AccessCode.objects.filter(lesson=lesson)
    if codes:
        htmlResponse = """
                    <table id="access-codes-list">
                        <thead class="header">
                        <th>الكود</th>
                        <th>الحالة</th>
                        """
        for code in codes:
            htmlResponse += f"""
                <tr>
                <td>{code.code}</td>
                <td class="{"used" if code.is_used else "available"}">{"مستخدم" if code.is_used else "متاح"}</td>
                </tr>
            """
        htmlResponse += "</head>"
    else:
        htmlResponse = "<div>لا توجد أكواد خاصة بهذا الدرس</div>"
    return HttpResponse(htmlResponse)


def generate_access_codes(request, lessonID, number):
    lesson = Lesson.objects.get(id=lessonID)
    for _ in range(number):
        while True:
            access_code = get_random_string(length=10)
            if not AccessCode.objects.filter(code=access_code):
                AccessCode.objects.create(lesson=lesson, code=access_code)
                break

    return get_lesson_coodes(request, lessonID)


def register_lesson(request, lessonID, code):
    lesson = Lesson.objects.get(id=lessonID)
    print(lesson)
    print(code)
    try:
        access_code = AccessCode.objects.get(lesson=lesson, code=code)
        if access_code.is_used:
            raise Exception("access code isn't available")
        request.user.lessons_registered.add(lesson)
        access_code.is_used = True
        access_code.save()
        return JsonResponse({"status": "success"})
    except:
        return JsonResponse({"status": "invalid"})
