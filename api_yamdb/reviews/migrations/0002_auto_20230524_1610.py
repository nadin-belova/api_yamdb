# Generated by Django 3.2 on 2023-05-24 13:10

from django.db import migrations, models
import reviews.validators


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('name',), 'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ('name',), 'verbose_name': 'Жанр', 'verbose_name_plural': 'Жанры'},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ('name',), 'verbose_name': 'Произведение', 'verbose_name_plural': 'Произведения'},
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=200, verbose_name='имя категории'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(max_length=200, verbose_name='имя жанра'),
        ),
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.TextField(verbose_name='Текст'),
        ),
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.TextField(blank=True, verbose_name='описание'),
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.SmallIntegerField(validators=[reviews.validators.validate_year], verbose_name='год'),
        ),
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, verbose_name='Биография'),
        ),
    ]
