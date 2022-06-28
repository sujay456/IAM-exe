# Generated by Django 4.0.5 on 2022-06-28 06:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org_name', models.CharField(max_length=100, unique=True)),
                ('num_of_users', models.IntegerField(default=0)),
                ('client_secret', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('head_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Permissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission_name', models.CharField(max_length=100)),
                ('org', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reg_org.organization')),
            ],
        ),
        migrations.CreateModel(
            name='UserPermissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('perm_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reg_org.permissions')),
            ],
        ),
        migrations.CreateModel(
            name='PartOf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('org', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reg_org.organization')),
            ],
        ),
        migrations.CreateModel(
            name='IsRoot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_root', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
