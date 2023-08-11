

from django.http import FileResponse
from .models import Resume
from .forms import ResumeForm
from django.shortcuts import render, redirect
from email import message
from django.shortcuts import render, HttpResponse
from .models import Member, Contact, Description, front_images
from django.http import JsonResponse


def index(request):
    resume_ = Resume.objects.all()
    front_images_ = front_images.objects.filter(type='1').all()
    front_images_profile = front_images.objects.filter(type='2').all()

    print(front_images_[0].logo)
    return render(request, 'introduction/templlate.html',
                  {"id": resume_[len(resume_)-1].id,
                   "logo": front_images_[0].logo,
                   "profile_image": front_images_profile[0].logo
                   }
                  )


def skills(request):
    front_images_ = front_images.objects.filter(type='1').all()
    front_images_profile = front_images.objects.filter(type='2').all()
    return render(request, 'introduction/skills.html', {
        "logo": front_images_[0].logo,
        "profile_image": front_images_profile[0].logo
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
        # return render(request, 'workingcontat.html', {})
        return render(request, 'introduction/contact.html', {"data": "Failed"})
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
        "profile_image": front_images_profile[1].logo})
