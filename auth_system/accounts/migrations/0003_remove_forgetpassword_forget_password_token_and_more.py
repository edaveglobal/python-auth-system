# Generated by Django 4.0 on 2022-11-25 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_forgetpassword_forget_password_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forgetpassword',
            name='forget_password_token',
        ),
        migrations.AddField(
            model_name='forgetpassword',
            name='forget_password_otp',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
