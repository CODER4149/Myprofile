# Generated by Django 4.1.4 on 2023-08-10 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('introduction', '0009_rename_resume_pdf_resume_resume_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='front_images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='item_images')),
            ],
        ),
    ]