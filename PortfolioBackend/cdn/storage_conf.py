import os
from decouple import config
# from StrefrontBackend2.settings import BASE_DIR
from ..settings.common import BASE_DIR

# USE_SPACES = config('USE_SPACES', cast=bool, default=False)
USE_SPACES = True

if USE_SPACES:
    # settings
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = "qandeelkhan.com-bucket"
    # AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    # AWS_DEFAULT_ACL = 'public-read'
    # default acl to none for the aws but public-read for the digitalocean aws bucket
    AWS_DEFAULT_ACL = None
    # AWS_S3_ENDPOINT_URL = config('AWS_S3_ENDPOINT_URL')
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME')
    # static settings
    AWS_LOCATION = 'space-resume/static'
    # STATIC_URL = f'https://shopingly-space.fra1.digitaloceanspaces.com/{AWS_LOCATION}/'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    # public media settings
    PUBLIC_MEDIA_LOCATION = 'space-resume/media'
    # MEDIA_URL = f'https://shopingly-space.fra1.digitaloceanspaces.com/{PUBLIC_MEDIA_LOCATION}/'

    # DEFAULT_FILE_STORAGE = '<space-name>.cdn.backends.MediaRootS3Boto3Storage'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
if not USE_SPACES:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'space-resume/static')
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'space-resume/media')
