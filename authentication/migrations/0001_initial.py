# Generated by Django 3.2.5 on 2024-06-29 09:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(max_length=120)),
                ('last_name', models.CharField(max_length=120)),
                ('company_name', models.CharField(max_length=120)),
                ('personal_telephone', models.CharField(max_length=16)),
                ('office_telephone', models.CharField(max_length=16)),
                ('address', models.TextField(max_length=250)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(blank=True, choices=[('Know my carbon footprints', 'Know my carbon footprints'), ('Generate a sustainability report', 'Generate a sustainability report'), ('Go through the application', 'Go through the application'), ('Request a Demo', 'Request a Demo')], max_length=55, null=True)),
                ('type', models.CharField(blank=True, choices=[('Energy (Renewable & Non-renewable)', 'Energy (Renewable & Non-renewable)'), ('Manufacturing', 'Manufacturing'), ('Transportation', 'Transportation'), ('Agriculture & Food Production', 'Agriculture & Food Production'), ('Construction & Real Estate', 'Construction & Real Estate'), ('Financial Services', 'Financial Services'), ('Technology & Telecommunications', 'Technology & Telecommunications'), ('Healthcare & Pharmaceuticals', 'Healthcare & Pharmaceuticals'), ('Hospitality & Tourism', 'Hospitality & Tourism'), ('Retail & Consumer Goods', 'Retail & Consumer Goods'), ('Utilities', 'Utilities'), ('Government & Public Sector', 'Government & Public Sector'), ('Education', 'Education'), ('Entertainment & Media', 'Entertainment & Media'), ('Non-profit & NGO', 'Non-profit & NGO'), ('Other', 'Other')], max_length=55, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
