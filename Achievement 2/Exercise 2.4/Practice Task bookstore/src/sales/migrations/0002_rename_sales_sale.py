# Generated by Django 4.2.15 on 2024-08-19 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_rename_books_book'),
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Sales',
            new_name='Sale',
        ),
    ]