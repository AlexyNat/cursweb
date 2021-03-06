# Generated by Django 3.2.6 on 2021-08-10 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0002_alter_typesubscription_duration'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gym',
            options={'ordering': ['name'], 'verbose_name': 'Зал', 'verbose_name_plural': 'Помещения'},
        ),
        migrations.AlterModelOptions(
            name='schedule',
            options={'ordering': ['recordStart'], 'verbose_name': 'Запись', 'verbose_name_plural': 'Расписание'},
        ),
        migrations.AlterModelOptions(
            name='subscription',
            options={'ordering': ['type'], 'verbose_name': 'Абонемент', 'verbose_name_plural': 'Абонементы'},
        ),
        migrations.AlterModelOptions(
            name='typesubscription',
            options={'ordering': ['name'], 'verbose_name': 'Вид абонемента', 'verbose_name_plural': 'Виды абонементов'},
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('М', 'Мужчина'), ('Ж', 'Женщина')], default=1, max_length=1, verbose_name='Пол'),
            preserve_default=False,
        ),
    ]
