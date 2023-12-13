# Generated by Django 4.2.8 on 2023-12-13 20:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', django_resized.forms.ResizedImageField(crop=None, force_format='WEBP', keep_meta=True, quality=75, scale=None, size=[500, None], upload_to='categories/')),
                ('image_alt', models.CharField(max_length=100)),
                ('order', models.IntegerField(blank=True, null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='stock.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_categories', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
