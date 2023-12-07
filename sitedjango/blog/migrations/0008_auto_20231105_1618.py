# Generated by Django 3.2.22 on 2023-11-05 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_rename_cometary_comentary'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentary',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='comentary',
            name='name',
            field=models.CharField(default='User', max_length=100, verbose_name='Имя'),
        ),
    ]