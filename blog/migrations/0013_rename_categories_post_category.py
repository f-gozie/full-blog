# Generated by Django 3.2.4 on 2021-06-30 16:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_post_categories'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='categories',
            new_name='category',
        ),
    ]