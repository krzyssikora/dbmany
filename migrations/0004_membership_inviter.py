# Generated by Django 4.0.7 on 2022-12-06 23:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dbmany', '0003_person_groups'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='inviter',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='membership_invites', to='dbmany.person'),
            preserve_default=False,
        ),
    ]
