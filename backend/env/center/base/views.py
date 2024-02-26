from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from .models import Teacher, Lesson, Appendix, ContactMessage
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta


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
    appendices = Appendix.objects.filter(lesson=lesson_)
    return render(request, 'base/lesson.html', context={"lesson": lesson_,
                                                        "appendices": appendices})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        remember = request.POST.get("remember")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if remember:
                request.session.set_expiry(2592000)
            next_url = request.GET.get("next", "home")
            return redirect(next_url)
        else:
            return render(request, 'base/sign-in.html', context={"error": "Incorrect username or password"})

    else:
        return render(request, 'base/sign-in.html')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            print(username)
            print(password)
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return redirect('home')
        else:
            return render(request, 'base/sign-up.html',
                          context={"error": f"User {request.POST.get('username')} is not available",
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
        last_minute = timezone.now() - timedelta(minutes=1)
        print(last_minute.minute)
        objects = ContactMessage.objects.filter(ip_address=ip_address, created_at__gte=last_minute)
        messages_sent = objects.count()
        print(objects)

        if messages_sent >= 1:
            # Return error response if message has been sent within the last minute
            return JsonResponse({'status': 'error',
                                 'message': 'لقد قمت بالفعل بإرسال رسالة خلال آخر 15 دقيقة. الرجاء معاودة المحاولة في وقت لاحق.'})
        else:
            name = request.POST.get('name')
            phone_number = request.POST.get('phone-number')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            print("here")

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
