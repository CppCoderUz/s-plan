# Generated by Django 4.2 on 2023-05-22 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0004_delete_smallgroup'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmallGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Guruh nomi')),
                ('code', models.CharField(max_length=50, verbose_name='Guruh kodi')),
                ('sum_students', models.IntegerField(default=0)),
                ('direction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='curriculum.direction', verbose_name="Yo'nalishi")),
            ],
            options={
                'verbose_name': 'Guruh',
                'verbose_name_plural': '5. Guruhlar',
            },
        ),
    ]