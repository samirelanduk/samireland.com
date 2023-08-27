# Generated by Django 4.2.2 on 2023-08-27 13:02

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
        ('about', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('name', models.CharField(max_length=100)),
                ('start', models.CharField(max_length=7)),
                ('end', models.CharField(blank=True, max_length=7)),
                ('description', wagtail.fields.RichTextField(blank=True, max_length=1000)),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='about.aboutpage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
