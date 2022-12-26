# Generated by Django 3.2.9 on 2022-11-30 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_intervieweraccount_linkedin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intervieweeaccount',
            name='Year_of_study',
            field=models.PositiveIntegerField(default=2023),
        ),
        migrations.AlterField(
            model_name='intervieweraccount',
            name='Age',
            field=models.PositiveIntegerField(default=50),
        ),
        migrations.AlterField(
            model_name='intervieweraccount',
            name='Experience',
            field=models.PositiveIntegerField(default=15),
        ),
        migrations.AlterField(
            model_name='intervieweraccount',
            name='Price',
            field=models.PositiveIntegerField(default=1500),
        ),
    ]