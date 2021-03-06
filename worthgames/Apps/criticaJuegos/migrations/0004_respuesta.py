# Generated by Django 3.0.4 on 2020-03-15 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('criticaJuegos', '0003_auto_20200315_1732'),
    ]

    operations = [
        migrations.CreateModel(
            name='Respuesta',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('contenido', models.TextField(verbose_name='Contenido')),
                ('comentario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='criticaJuegos.Comentario')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='criticaJuegos.Usuario')),
            ],
        ),
    ]
