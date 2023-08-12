

from django.http import FileResponse
from .models import Resume
from .forms import ResumeForm
from django.shortcuts import render, redirect
from email import message
from django.shortcuts import render, HttpResponse
from .models import Member, Contact, Description, front_images,about
from django.http import JsonResponse
from datetime import datetime


def index(request):
    resume_ = Resume.objects.all()
    front_images_ = front_images.objects.filter(type='1').all()
    front_images_profile = front_images.objects.filter(type='2').all()
    about_ = about.objects.all()
    keys = []
    data =[]
    print(about_)
    given_date = datetime(2021, 6, 26)
    current_date = datetime.now()
    time_difference = current_date - given_date
    
    years = time_difference.days // 365
    months = (time_difference.days % 365) // 30
    
    context = {
        'years': years,
        'months': months
    }

    for i in about_:
        print(i.name)
        
        data.extend([
    {
        "name": "Name",
        "value": i.name
    },
    {
        "name": "Email",
        "value": i.email,
    },
    {
        "name": "email",
        "value": i.address,
    },
    {
        "name": "Natinality",
        "value": i.natinality,
    }
])






    print(front_images_[0].logo)
    return render(request, 'introduction/templlate.html',
                  {"id": resume_[len(resume_)-1].id,
                   "logo": front_images_[0].logo,
                   "profile_image": front_images_profile[0].logo,
                    "profile" : about_[0] if len(about_)!=0 else "AMOL YADAV",
                    'time_difference': f" {years} and {months}",
                    "about": data,

                   }
                  )


def skills(request):
    front_images_ = front_images.objects.filter(type='1').all()
    front_images_profile = front_images.objects.filter(type='2').all()
    about_ = about.objects.all()
    keys = []
    data =[]
    print(about_)
    given_date = datetime(2021, 6, 26)
    current_date = datetime.now()
    time_difference = current_date - given_date
    
    years = time_difference.days // 365
    months = (time_difference.days % 365) // 30
    
    context = {
        'years': years,
        'months': months
    }

    for i in about_:
        print(i.name)
        
        data.extend([
    {
        "name": "Name",
        "value": i.name
    },
    {
        "name": "Email",
        "value": i.email,
    },
    {
        "name": "email",
        "value": i.address,
    },
    {
        "name": "Natinality",
        "value": i.natinality,
    }
])



    return render(request, 'introduction/skills.html', {
        "about": data,

        "logo": front_images_[0].logo,
        "profile_image": front_images_profile[0].logo,
         'time_difference': f" {years} and {months}"
    })


def experience(request):
    front_images_ = front_images.objects.filter(type='1').all()
    front_images_profile = front_images.objects.filter(type='2').all()
    return render(request, 'introduction/experience.html', {
        "logo": front_images_[0].logo,
        "profile_image": front_images_profile[0].logo
    })


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('subject')
        newcontact = Contact(name=name, email=email, message=message)
        newcontact.save()
        data = {'name': name, 'email': email, 'subject': message}
        print(data)
        front_images_ = front_images.objects.filter(type='1').all()
        front_images_profile = front_images.objects.filter(type='2').all()
        return render(request, 'introduction/contact.html', {"message": "Your Response successfully send",
                                                             "status_code": 200,
                                                             "logo": front_images_[0].logo,
                                                             "profile_image": front_images_profile[0].logo
                                                             })

        # return render(request, 'success.html', {})

    else:
        front_images_ = front_images.objects.filter(type='1').all()
        front_images_profile = front_images.objects.filter(type='2').all()
        # return render(request, 'workingcontat.html', {})
        return render(request, 'introduction/contact.html', {"data": "Failed",
                                                             "logo": front_images_[0].logo,
                                                             "profile_image": front_images_profile[0].logo
                                                             })
    # return render(request, 'introduction/contact.html')


def description(request):
    related_items = Description.objects.all()
    front_images_ = front_images.objects.filter(type='1').all()
    front_images_profile = front_images.objects.filter(type='2').all()
    return render(request, 'introduction/contact.html', {

        "related_items": related_items,
        "logo": front_images_[0].logo,
        "profile_image": front_images_profile[0].logo


    })


def upload_resume(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = ResumeForm()
    return render(request, 'upload_resume.html', {'form': form})


def download_resume(request, resume_id):
    resume = Resume.objects.get(pk=resume_id)
    resume_file = resume.resume_file
    response = FileResponse(resume_file, as_attachment=True)
    return response


def get_resume_data(request):
    related_items = Resume.objects.all()
    front_images_ = front_images.objects.filter(type='1').all()
    front_images_profile = front_images.objects.filter(type='2').all()

    # print(front_images_profile[0].logo)

    return render(request, 'introduction/', {

        "id": related_items[-1].id,
        "logo": front_images_[0].logo,
        "profile_image": front_images_profile[0].logo})



def about__(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        nationality = request.POST.get('nationality')

        newcontact = about(name=name, email=email, address=address,nationality=nationality)
        newcontact.save()
        front_images_ = front_images.objects.filter(type='1').all()
        front_images_profile = front_images.objects.filter(type='2').all()
        return render(request, 'introduction/contact.html', {"message": "Your Response successfully send",
                                                             "status_code": 200,
                                                             "logo": front_images_[0].logo,
                                                             "profile_image": front_images_profile[0].logo
                                                             })


    else:
        front_images_ = front_images.objects.filter(type='1').all()
        front_images_profile = front_images.objects.filter(type='2').all()
        # return render(request, 'workingcontat.html', {})
        return render(request, 'introduction/contact.html', {"data": "Failed",
                                                             "logo": front_images_[0].logo,
                                                             "profile_image": front_images_profile[0].logo
                                                             })


