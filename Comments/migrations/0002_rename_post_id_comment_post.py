# Generated by Django 4.1.1 on 2022-10-20 08:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Comments', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='post_id',
            new_name='post',
        ),
    ]