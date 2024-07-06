# Generated by Django 5.0.6 on 2024-07-04 13:33

import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
import multiselectfield.db.fields
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(blank=True, max_length=150, null=True, unique=True)),
                ('is_client', models.BooleanField(default=False)),
                ('is_agency', models.BooleanField(default=False)),
                ('is_guide', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Guide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guide_email', models.EmailField(max_length=254, null=True, unique=True)),
                ('guide_phone_number', models.CharField(max_length=15, null=True)),
                ('password', models.CharField(max_length=100, null=True)),
                ('guide_first_name', models.CharField(max_length=30, null=True)),
                ('guide_last_name', models.CharField(max_length=30, null=True)),
                ('guide_gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('guide_languages', multiselectfield.db.fields.MultiSelectField(choices=[('en', 'English'), ('es', 'Spanish'), ('fr', 'French'), ('de', 'German'), ('zh', 'Chinese'), ('ja', 'Japanese'), ('ar', 'Arabic'), ('ru', 'Russian'), ('pt', 'Portuguese'), ('it', 'Italian'), ('ko', 'Korean'), ('nl', 'Dutch'), ('sv', 'Swedish'), ('tr', 'Turkish'), ('pl', 'Polish'), ('vi', 'Vietnamese'), ('el', 'Greek'), ('th', 'Thai')], max_length=50)),
                ('guide_dateofbirth', models.DateField(verbose_name='mm/dd/yyyy')),
                ('guide_description', models.CharField(max_length=200)),
                ('guide_website', models.CharField(max_length=100, null=True)),
                ('guide_location', models.CharField(max_length=100, null=True)),
                ('guide_licenses', models.FileField(null=True, upload_to='licenses/')),
                ('guide_profile_picture', models.ImageField(default='projectone/Users/defaults/default-avatar-icon-of-social-media-user-vector.jpg', upload_to='profile_pictures/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='guide', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30, null=True)),
                ('last_name', models.CharField(max_length=30, null=True)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('email_user', models.EmailField(max_length=254, null=True, unique=True)),
                ('password', models.CharField(max_length=100, null=True)),
                ('profile_picture', models.ImageField(default='projectone/Users/defaults/default-avatar-icon-of-social-media-user-vector.jpg', upload_to='profile_pictures/')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agency_name', models.CharField(max_length=255, null=True)),
                ('agency_email', models.EmailField(max_length=254, null=True, unique=True)),
                ('password', models.CharField(max_length=100, null=True)),
                ('agency_phone_number', models.CharField(max_length=15, null=True)),
                ('agency_website', models.CharField(max_length=255, null=True)),
                ('number_of_employees', models.CharField(max_length=15, null=True)),
                ('agency_location', models.CharField(max_length=15, null=True)),
                ('agency_licenses', models.FileField(blank=True, null=True, upload_to='licenses/')),
                ('agency_profile_picture', models.FileField(default='projectone/Users/defaults/default-avatar-icon-of-social-media-user-vector.jpg', upload_to='profile_pictures/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='agency', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]