# Generated by Django 3.0.6 on 2020-06-04 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='picture',
            field=models.ImageField(upload_to='profile_pic'),
        ),
    ]