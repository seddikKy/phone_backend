# Generated by Django 3.2 on 2022-03-19 22:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('user_name', models.CharField(max_length=150, unique=True, verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('about', models.CharField(blank=True, max_length=500, verbose_name='about')),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CallLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_user', models.CharField(max_length=50)),
                ('call_type', models.CharField(max_length=50)),
                ('id_call', models.CharField(max_length=50)),
                ('call_started_at', models.CharField(max_length=50)),
                ('duration', models.CharField(max_length=50)),
                ('id_log', models.CharField(max_length=200)),
                ('called_phone_number', models.CharField(max_length=20)),
                ('position_call_log', models.CharField(max_length=50)),
                ('reception_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_log', models.CharField(max_length=200)),
                ('max_position_call_log', models.IntegerField(max_length=20)),
                ('reception_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(help_text='Entrez le role de votre contact', max_length=200, verbose_name='Role du contact')),
            ],
        ),
        migrations.CreateModel(
            name='Tier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tier_name', models.CharField(help_text='Entrez le nom de votre client', max_length=200, verbose_name='Nom du client')),
                ('address', models.CharField(help_text="Entrez l'adresse de votre client", max_length=200, verbose_name='Adresse du client')),
                ('email', models.EmailField(max_length=254)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_name', models.CharField(help_text='Entrez le nom de votre contact', max_length=200, verbose_name='Nom du contact')),
                ('phone_number', models.CharField(help_text='Entrez le numéro de téléphone', max_length=20, verbose_name='Numéro de téléphone')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('id_role', models.ForeignKey(help_text='Affectez le role du contact', on_delete=django.db.models.deletion.CASCADE, to='core.role', verbose_name='Role du contact')),
                ('id_tier', models.ForeignKey(help_text='Affectez le contact à votre client', on_delete=django.db.models.deletion.CASCADE, to='core.tier', verbose_name='Nom du client')),
                ('id_user', models.ForeignKey(help_text='Affectez le contact à un opérateur', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name="Nom de l'opérateur")),
            ],
        ),
    ]
