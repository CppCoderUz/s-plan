# Generated by Django 4.2 on 2023-05-23 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0009_lessonwithteacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonwithteacher',
            name='teacher',
            field=models.ManyToManyField(null=True, to='curriculum.teacher', verbose_name="Dars beruvchi o'qituvchilar"),
        ),
    ]
