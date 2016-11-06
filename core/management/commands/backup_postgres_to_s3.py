# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import os
from datetime import datetime

from boto3.session import Session
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Backs up PostgreSQL database to AWS S3'

    def handle(self, *args, **options):
        AWS_ACCESS_KEY_ID = os.environ.get('AWS_S3_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_S3_SECRET_ACCESS_KEY')
        AWS_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
        AWS_BUCKET_NAME = os.environ.get('AWS_S3_BUCKET_NAME')

        session = Session(aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                          region_name=AWS_REGION_NAME)

        s3 = session.resource('s3')

        bucket = s3.Bucket(AWS_BUCKET_NAME)

        timestamp = datetime.utcnow().strftime('%Y_%m_%d_%H%M_UTC')
        db_file = "pgbackup_{}.dump".format(timestamp)
        db_host = settings.DATABASES['default']['HOST']
        db_port = settings.DATABASES['default']['PORT']
        db_name = settings.DATABASES['default']['NAME']
        db_user = settings.DATABASES['default']['USER']

        # See command definitions at http://www.postgresql.org/docs/9.4/static/app-pgdump.html
        pg_dump_command = "pg_dump --host={host} --port={port} --user={user} --format=c -O -x --file={file_name} {name}".format(
            host=db_host,
            port=db_port,
            user=db_user,
            file_name=db_file,
            name=db_name)
        self.stdout.write("Enter {}'s psql password".format(db_user))
        os.system(pg_dump_command)

        bucket.upload_file(db_file, db_file)
        os.system("rm {}".format(db_file))
        self.stdout.write("{} successfully uploaded to AWS S3".format(db_file))
