# Generated by Django 2.0.6 on 2018-06-29 06:02

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('profile_app', '0006_clientclass_weight'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='birth_date',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='client_class',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='employer_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='employment_type',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='income_yearly',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='last_loan_paid',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='last_loan_taken',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='profile_updated',
        ),
        migrations.AddField(
            model_name='profile',
            name='about',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True),
        ),
        migrations.DeleteModel(
            name='ClientClass',
        ),
        migrations.DeleteModel(
            name='Contact',
        ),
        migrations.DeleteModel(
            name='EmploymentType',
        ),
    ]
