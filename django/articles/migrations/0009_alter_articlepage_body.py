# Generated by Django 4.2.2 on 2023-08-27 13:02

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0008_alter_articlepage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepage',
            name='body',
            field=wagtail.fields.StreamField([('text', wagtail.blocks.RichTextBlock(features=['bold', 'link', 'italic', 'h2', 'h3', 'ol', 'ul', 'code', 'strikethrough'])), ('figure', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.blocks.RichTextBlock(features=['bold', 'link', 'italic']))], icon='image')), ('code', wagtail.blocks.StructBlock([('language', wagtail.blocks.CharBlock()), ('code', wagtail.blocks.TextBlock())], icon='code'))], use_json_field=True),
        ),
    ]