# Generated by Django 2.2.16 on 2022-07-03 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reg_org', '0005_auto_20220702_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loginhistory',
            name='login_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='registerhistory',
            name='register_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]