# Generated by Django 2.0.1 on 2018-01-13 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Jpider_response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=300)),
                ('headers', models.CharField(max_length=1000)),
                ('data', models.CharField(max_length=100)),
                ('cookies', models.CharField(max_length=1000)),
            ],
        ),
    ]
