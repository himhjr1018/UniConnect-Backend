# Generated by Django 4.2.2 on 2023-07-30 06:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0004_alter_interestedprogram_stage'),
        ('universities', '0002_university_domain_alter_university_city_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('tags', models.TextField()),
                ('ctime', models.DateTimeField(auto_now_add=True)),
                ('liked_by', models.ManyToManyField(to='users.userprofile')),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='users.userprofile')),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='universities.university')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('ctime', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='community.post')),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='users.userprofile')),
            ],
        ),
    ]