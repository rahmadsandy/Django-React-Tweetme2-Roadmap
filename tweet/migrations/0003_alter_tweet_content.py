# Generated by Django 3.2.4 on 2021-09-11 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0002_alter_tweet_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='content',
            field=models.TextField(default='tweets'),
            preserve_default=False,
        ),
    ]
