# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0009_auto_20150407_2021'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='form',
            name='emails_send_from',
        ),
        migrations.AddField(
            model_name='form',
            name='confirmation_mail',
            field=models.TextField(default=b'Hi there!This is a confirmation of your application to <a href="http://djangogirls.org/{city}">Django Girls {CITY}</a>. Yay! That\'s a huge step already, we\'re proud of you!\n\nMind that this is not a confirmation of participation in the event, but a confirmation that we received your application.\n\nYou\'ll receive an email from the team that organizes Django Girls {CITY} soon. You can always reach them by answering to this email or by writing to {your event mail}.\nFor your reference, we\'re attaching your answers below.\n\nHugs, cupcakes and high-fives!\nDjango Girls', help_text=b'Mail will be sent from your event mail.\nAlso the answers will be attached.'),
        ),
        migrations.AlterField(
            model_name='application',
            name='email',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='sent_from',
            field=models.EmailField(max_length=254),
        ),
    ]
