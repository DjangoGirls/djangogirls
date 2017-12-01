# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='has_option_other',
            field=models.BooleanField(default=False, help_text=b"Used only with 'Choices' question type", verbose_name=b"Allow for 'Other' answer?"),
        ),
        migrations.AlterField(
            model_name='question',
            name='is_multiple_choice',
            field=models.BooleanField(default=False, help_text=b"Used only with 'Choices' question type", verbose_name=b'Are there multiple choices allowed?'),
        ),
        migrations.AlterField(
            model_name='question',
            name='is_required',
            field=models.BooleanField(default=True, verbose_name=b'Is the answer to the question required?'),
        ),
    ]
