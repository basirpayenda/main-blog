# Generated by Django 2.2.1 on 2019-05-13 06:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_blogpost_updated_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogpost',
            options={'ordering': ['-updated_at', '-created_at']},
        ),
    ]
