# Generated by Django 4.0.7 on 2022-12-15 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbmany', '0007_alter_membership_invite_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='invite_reason',
            field=models.CharField(max_length=64),
        ),
    ]