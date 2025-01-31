# Generated by Django 5.0.2 on 2025-01-29 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0004_alter_session_date_end_alter_session_date_start'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('uid', models.CharField(max_length=1000)),
                ('room_name', models.CharField(max_length=200)),
                ('insession', models.BooleanField(default=True)),
            ],
        ),
    ]
