# Generated by Django 4.0.5 on 2022-09-13 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_faculty_administrator'),
    ]

    operations = [
        migrations.CreateModel(
            name='course',
            fields=[
                ('course_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('course_name', models.CharField(max_length=64)),
                ('lecture_hours', models.IntegerField()),
                ('tutorial_hours', models.IntegerField()),
                ('practical_hours', models.IntegerField()),
                ('j_project_hours', models.IntegerField()),
                ('credits', models.IntegerField()),
            ],
        ),
    ]