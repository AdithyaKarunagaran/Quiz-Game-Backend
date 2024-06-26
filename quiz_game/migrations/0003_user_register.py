# Generated by Django 5.0 on 2024-04-13 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_game', '0002_rename_text_jsquestion_question'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Register',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('quiz_marks', models.JSONField(default=list)),
                ('quiz_attempts', models.IntegerField(default=0)),
            ],
        ),
    ]
