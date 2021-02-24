# Generated by Django 3.1.5 on 2021-02-24 14:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=500)),
                ('choice1', models.CharField(max_length=50)),
                ('choice2', models.CharField(max_length=50)),
                ('isClosed', models.BooleanField(default=False)),
                ('result', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BethovenUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('coins', models.IntegerField()),
                ('following', models.ManyToManyField(related_name='followers', to='main_app.BethovenUser')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserBet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('choice', models.IntegerField()),
                ('amount', models.IntegerField()),
                ('bet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.bet')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.bethovenuser')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('text', models.CharField(max_length=200)),
                ('bet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.bet')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.bethovenuser')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='bet',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='BetsOwned', to='main_app.bethovenuser'),
        ),
        migrations.AddField(
            model_name='bet',
            name='usersBetting',
            field=models.ManyToManyField(related_name='BetsDone', through='main_app.UserBet', to='main_app.BethovenUser'),
        ),
    ]
