# Generated by Django 2.2.16 on 2022-07-02 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reg_org', '0002_auto_20220702_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='loginhistory',
            name='message',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='loginhistory',
            name='status',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
