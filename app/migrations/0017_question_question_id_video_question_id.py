# Generated by Django 4.1.7 on 2023-03-08 06:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20230306_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_id',
            field=models.IntegerField(auto_created=True, null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='question_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.question'),
        ),
    ]
