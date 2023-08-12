from django.contrib import admin
from .models import Member, Contact, Description, Resume, front_images, about



# Register your models here.


class MemberAdmin(admin.ModelAdmin):
    list_display = ("Name", "email", "message")


class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "message")


class DescriptionAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "message",
                    "logo", "address", "description")


class ResumeForm(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'resume_file')


class Frontimages(admin.ModelAdmin):
    list_display = ['logo']

class About(admin.ModelAdmin):
    list_display = ('name', 'email', 'address', 'natinality')

admin.site.register(Member, MemberAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Description, DescriptionAdmin)
admin.site.register(Resume, ResumeForm)
admin.site.register(front_images, Frontimages)
admin.site.register(about, About)

