from django.shortcuts import redirect, render
from .models import *
from .forms import *
import random
from django.core.mail import send_mail
from django.conf import settings

default_dict = {
    "acc_pages": ["login_page", "register_page", "recover_pwd_page"],
    "courses": [course for course in Course.objects.all()]
}

# otp
def otp(request, otp_for=None):
    otp_num = random.randint(1000, 9999)

    print("OTP is: ", otp_num)
    request.session['otp'] = otp_num

    email_to_list = [request.session['email'],]

    subject = f'OTP for {otp_for} Registration'

    email_from = settings.EMAIL_HOST_USER

    message = f"Your One Time Password for verification is: {otp_num}."

    send_mail(subject, message, email_from, email_to_list)

def index(request):
    default_dict["current_page"] = "index"
    return render(request, "index.html", default_dict)

def login_page(request):
    default_dict["current_page"] = "login_page"
    return render(request, "login_page.html", default_dict)

# otp page
def otp_page(request):
    default_dict["current_page"] = "otp_page"
    return render(request, "otp_page.html", default_dict)

def register_page(request):
    default_dict["current_page"] = "register_page"
    default_dict["roles"] = [role for role in Role.objects.all()]
    return render(request, "register_page.html", default_dict)

def recover_pwd_page(request):
    default_dict["current_page"] = "recover_pwd_page"
    
    if request.POST:
        print('recover pwd requested.')
        master = Master.objects.get(Email=request.POST['email'])

        request.session['email'] = master.Email
        otp(request, master.Role.Name) # otp create method calling
        
        default_dict["current_page"] = 'varify_otp'
        default_dict['varify_for'] = 'rec'
    
    return render(request, "recover_pwd_page.html", default_dict)

def profile_page(request):
    profile_data(request)
    default_dict["current_page"] = "profile_page"
    return render(request, "profile_page.html", default_dict)

def register(request):
    # print(request.POST)
    role = Role.objects.get(id=int(request.POST['role']))
    request.session['email'] = request.POST['email']
    
    master = Master.objects.create(
        Role = role,
        Email = request.POST['email'],
        Password = request.POST['password']
    )
    if role.Name == 'student':
        course = Course.objects.get(id=int(request.POST['course']))
        Student.objects.create(
            Master = master,
            Course = course,
        )
    else:
        Faculty.objects.create(
            Master = master,
        )
    otp(request, role.Name) # otp create method calling
    
    return redirect(otp_page)

def varify_otp(request, varify_for='reg'):
    email = request.session['email']

    if request.session['otp'] == int(request.POST['otp']):
        master = Master.objects.get(Email=email)

        if varify_for == 'rec':
            if request.POST['new_password'] == request.POST['conf_password']:
                master.Password = request.POST['new_password']
        else:
            master.IsActive = True

        master.save()

        del request.session['email']
        del request.session['otp']
    else:
        print('invalid otp.')
        return redirect(register_page)

    return redirect(login_page)

def profile_data(request):
    master = Master.objects.get(Email=request.session['email'])
    gender = []
    for k,v in gender_choice:
        gender.append(
            {'short_tag': k, 'text': v}
        )
    print(gender)
    if master.Role.Name == 'student':
        user = Student.objects.get(Master=master)
    else:
        user = Faculty.objects.get(Master=master)
    default_dict['gender_choice'] = gender
    default_dict['user_profile'] = user

def login(request):
    master = Master.objects.get(Email=request.POST['email'])
    
    if master.Password == request.POST['password']:
        request.session['email'] = master.Email
        if master.IsActive:
            profile_data(request) # to load profile data after login
            
            return redirect(profile_page)
        else:
            otp(request, master.Role.Name)
            return redirect(otp_page)
    else:
        return redirect(index)

def profile_update(request):
    # print("update data: ", request.FILES)
    user = default_dict['user_profile']
    user_role = user.Master.Role.Name

    full_name = request.POST['full_name']
    mobile = request.POST['mobile']
    dob = request.POST['dob']
    gender = request.POST['gender']

    if user_role == 'student':
        user = Student.objects.get(id=user.id)
    elif user_role == 'faculty':
        user = Faculty.objects.get(id=user.id)
    
    user.FullName = full_name
    user.Mobile = mobile
    user.DoB = dob
    user.Gender = gender

    # upload an image
    import os
    if 'profile_image' in request.FILES:
        profile_image = request.FILES['profile_image']

        file_type = profile_image.name.split('.')[1]
        new_file_name = f"{'_'.join(user.FullName.lower().split())}_{user.Mobile}.{file_type}"
        profile_image.name = new_file_name

        for file in os.listdir(settings.MEDIA_ROOT + '/' + user_role + 's/profile/'):
            print('file: ', file)

        if new_file_name in os.listdir(settings.MEDIA_ROOT + '/' + user_role + 's/profile/'):
            os.remove(settings.MEDIA_ROOT + '/' + user_role + 's/profile/' + new_file_name)
            
        print('image name: ', profile_image.name)
        user.ProfileImage = profile_image

    user.save()

    return redirect(profile_page)

def check(request):
    course = Course.objects.get(CourseName="IT Career")

    subjects = Subject.objects.filter(Course=course)

    print(subjects)

    return redirect(index)

def signout(request):
    if 'email' in request.session:
        del request.session['email']
    return redirect(login_page)