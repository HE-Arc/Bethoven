# Generated by Django 3.1.7 on 2021-03-25 09:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bet',
            old_name='choice2',
            new_name='choice0',
        ),
        migrations.AlterField(
            model_name='bethovenuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='bethovenUser', to=settings.AUTH_USER_MODEL),
        ),
    ]
