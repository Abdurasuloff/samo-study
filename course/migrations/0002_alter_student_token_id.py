# Generated by Django 4.1.1 on 2022-11-16 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("course", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="token_id",
            field=models.CharField(default="81843354", max_length=150),
        ),
    ]