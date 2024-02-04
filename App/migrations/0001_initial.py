# Generated by Django 4.2.6 on 2023-12-09 07:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='about',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('About_us', models.CharField(max_length=500)),
                ('mission', models.CharField(max_length=500)),
                ('plan', models.CharField(max_length=500)),
                ('vesion', models.CharField(max_length=500)),
                ('mission_img', models.ImageField(default='some_value3', max_length=1000, upload_to='about')),
            ],
        ),
        migrations.CreateModel(
            name='detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fichier', models.FileField(upload_to='details')),
            ],
        ),
        migrations.CreateModel(
            name='equipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
                ('Email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='personnel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('position', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('fichier_CV', models.TextField(max_length=250)),
                ('photo', models.ImageField(max_length=1000, upload_to='personnel')),
                ('lien_linkedln', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='projet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='some_value', max_length=1000, upload_to='projects')),
                ('libellai', models.TextField(max_length=100)),
                ('categorie', models.TextField(max_length=100)),
                ('description', models.TextField(max_length=500)),
                ('date_debut', models.DateTimeField(auto_now_add=True)),
                ('date_fin', models.DateTimeField(auto_now_add=True)),
                ('acheve', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.TextField()),
                ('username', models.TextField(default='', max_length=25, null=True, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=26)),
                ('phone', models.TextField(blank=True, null=True)),
                ('photo', models.ImageField(null=True, upload_to='clients')),
                ('confirmation_code', models.CharField(blank=True, max_length=6, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('user', models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ServiceDemand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object', models.TextField(max_length=200, null=True)),
                ('details', models.TextField(max_length=2000)),
                ('submission_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_accepted', models.BooleanField(default=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('service_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.service')),
            ],
        ),
        migrations.CreateModel(
            name='CompletedCommand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completion_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('command', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='App.servicedemand')),
            ],
        ),
        migrations.CreateModel(
            name='AcceptedCommand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acceptance_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('command', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='App.servicedemand')),
            ],
        ),
    ]
