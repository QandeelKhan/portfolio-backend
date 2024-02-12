import os
from django.conf import settings
from PortfolioBackend.cdn.storage_conf import MEDIA_ROOT, PUBLIC_MEDIA_LOCATION
from django.core.management.base import BaseCommand
from boto3 import Session
from botocore.exceptions import NoCredentialsError
from decouple import config
from pathlib import Path


class Command(BaseCommand):
    help = 'Collects media files and uploads them to the DigitalOcean Space bucket'

    def handle(self, *args, **options):
        session = Session(
            aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
            region_name='nyc3',
        )
        s3 = session.resource('s3')
        bucket = s3.Bucket(config('AWS_STORAGE_BUCKET_NAME'))

        for dirpath, dirnames, filenames in os.walk(MEDIA_ROOT):
            for filename in filenames:
                local_path = Path(dirpath) / filename
                remote_path = Path(PUBLIC_MEDIA_LOCATION) / \
                    local_path.relative_to(MEDIA_ROOT)
                obj = bucket.Object(str(remote_path))
                obj.upload_file(str(local_path), ExtraArgs={
                                'ACL': 'public-read'})

            for dirname in dirnames:
                local_path = Path(dirpath) / dirname
                remote_path = Path(PUBLIC_MEDIA_LOCATION) / \
                    local_path.relative_to(MEDIA_ROOT)
                obj = bucket.Object(str(remote_path) + '/')
                obj.put()
