# Generated by Django 4.2 on 2023-05-23 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0011_alter_lessonwithteacher_teacher'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProPractice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.IntegerField(verbose_name='Amaliyot muddati')),
                ('semestr', models.IntegerField(verbose_name='Semestr')),
                ('direction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='curriculum.direction', verbose_name="Yo'nalish")),
            ],
            options={
                'verbose_name': 'Malakaviy amaliyot reja',
                'verbose_name_plural': '9. Malakaviy amaliyot rejalar',
            },
        ),
        migrations.CreateModel(
            name='ProPracticeWithGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='curriculum.smallgroup', verbose_name='Guruh')),
                ('pro_practice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='curriculum.propractice')),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='curriculum.teacher', verbose_name="O'qituvchi")),
            ],
            options={
                'verbose_name': 'Malakaviy amaliyot dars',
                'verbose_name_plural': '10. Malakaviy amaliyot darslar',
            },
        ),
    ]
