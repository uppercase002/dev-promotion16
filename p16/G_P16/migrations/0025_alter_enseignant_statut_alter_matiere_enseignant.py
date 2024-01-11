# Generated by Django 4.2.5 on 2024-01-07 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('G_P16', '0024_alter_enseignant_statut'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enseignant',
            name='Statut',
            field=models.CharField(choices=[('vacataire', 'Vacataire'), ('titulaire', 'Titulaire'), ('missionnaire', 'Missionnaire')], max_length=15, verbose_name='Statut'),
        ),
        migrations.AlterField(
            model_name='matiere',
            name='Enseignant',
            field=models.CharField(max_length=10, verbose_name='Enseignant'),
        ),
    ]
