# Generated by Django 4.2.1 on 2023-06-08 02:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.RenameField(
            model_name='category',
            old_name='catagory_name',
            new_name='category_name',
        ),
        migrations.RenameField(
            model_name='fooditem',
            old_name='Category',
            new_name='category',
        ),
    ]
