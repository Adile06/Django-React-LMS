# Generated by Django 4.2.7 on 2024-07-20 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_cart_options_alter_cartorder_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='level',
            field=models.CharField(choices=[('Başlangic', 'Başlangıç'), ('Orta', 'Orta'), ('Ileri Seviye', 'İleri Seviye')], default='Baslangic', max_length=100),
        ),
        migrations.AlterField(
            model_name='course',
            name='platform_status',
            field=models.CharField(choices=[('İncelemede', 'İncelemede'), ('Pasif', 'Pasif'), ('Reddedilmiş', 'Reddedilmiş'), ('Taslak', 'Taslak'), ('Yayinlanmis', 'Yayınlanmış')], default='Yayinlanmis', max_length=100),
        ),
        migrations.AlterField(
            model_name='course',
            name='teacher_course_status',
            field=models.CharField(choices=[('Taslak', 'Taslak'), ('Pasif', 'Pasif'), ('Yayinlanmis', 'Yayınlanmış')], default='Yayinlanmis', max_length=100),
        ),
    ]