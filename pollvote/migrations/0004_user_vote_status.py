# Generated by Django 4.2.3 on 2023-07-27 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pollvote', '0003_alter_pollvote_candidate'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='vote_status',
            field=models.CharField(blank=True, choices=[{'polled': 'polled', 'unpolled': 'unpolled'}], default='unpolled', max_length=100, null=True),
        ),
    ]