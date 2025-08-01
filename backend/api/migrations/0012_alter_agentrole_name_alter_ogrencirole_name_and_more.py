# Generated by Django 4.2.7 on 2025-06-15 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_agentrole_remove_hdmhafiz_egitmen_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentrole',
            name='name',
            field=models.CharField(choices=[('HBSTemsilci', 'HBSTemsilci')], max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='ogrencirole',
            name='name',
            field=models.CharField(choices=[('AkademiOgrenci', 'AkademiOgrenci'), ('HBSOgrenci', 'HBSOgrenci'), ('HDMOgrenci', 'HDMOgrenci')], max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='teacherrole',
            name='name',
            field=models.CharField(choices=[('AkademiEgitmen', 'AkademiEgitmen'), ('ESKEPEgitmen', 'ESKEPEgitmen'), ('HBSEgitmen', 'HBSEgitmen'), ('HDMEgitmen', 'HDMEgitmen')], max_length=50, unique=True),
        ),
    ]
