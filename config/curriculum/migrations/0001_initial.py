# Generated by Django 4.2 on 2023-05-22 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0002_facultymanager_departmentemployee_cafedramanager'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cafedra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Kafedra',
                'verbose_name_plural': '2. Kafedralar',
            },
        ),
        migrations.CreateModel(
            name='Science',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('cafedra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='curriculum.cafedra')),
            ],
            options={
                'verbose_name': 'Fan',
                'verbose_name_plural': '3. Fanlar',
            },
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('manager', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.facultymanager')),
            ],
            options={
                'verbose_name': 'Fakultet',
                'verbose_name_plural': '1. Fakultetlar',
            },
        ),
        migrations.AddField(
            model_name='cafedra',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='curriculum.faculty'),
        ),
        migrations.AddField(
            model_name='cafedra',
            name='manager',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.cafedramanager'),
        ),
    ]
