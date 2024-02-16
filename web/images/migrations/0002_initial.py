# Generated by Django 5.0 on 2024-02-14 11:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('images', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='customimage',
            name='uploaded_by_user',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='uploaded by user'),
        ),
        migrations.AddField(
            model_name='customrendition',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='renditions', to='images.customimage'),
        ),
        migrations.AlterUniqueTogether(
            name='customrendition',
            unique_together={('image', 'filter_spec', 'focal_point_key')},
        ),
    ]