# Generated by Django 3.2 on 2023-05-25 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20230524_1610'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('pub_date',), 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ('pub_date',), 'verbose_name_plural': 'Отзывы'},
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=256, verbose_name='имя категории'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(max_length=256, verbose_name='имя жанра'),
        ),
        migrations.AlterField(
            model_name='title',
            name='name',
            field=models.CharField(db_index=True, max_length=256, verbose_name='название'),
        ),
    ]