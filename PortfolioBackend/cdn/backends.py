from storages.backends.s3boto3 import S3Boto3Storage
# making settings for our static assets to after that set in conf.py
# this will make upload our static folder into digitalocean,


class StaticStorage(S3Boto3Storage):
    bucket_name = 'qandeelkhan.com-bucket'
    location = "space-resume/static"
    default_acl = 'public-read'


# this will make anything uploading through our models will go there in media folder on digitalocean.


class MediaStorage(S3Boto3Storage):
    bucket_name = 'qandeelkhan.com-bucket'
    location = "space-resume/media"
    default_acl = 'public-read'


# above provided locations we set similar to our local settings so the directories
# name and locations on the our hosted app on cloud look similar to our local file
# structure. we can type any name i.e "static-abc", "root-abcd".
