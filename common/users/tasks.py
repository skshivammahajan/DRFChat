import datetime

from celery.decorators import periodic_task
from django.conf import settings
from django.core.files.storage import default_storage
from django.utils import timezone

from experchat.models.users import UserMedia


@periodic_task(run_every=(settings.TMP_MEDIA_CLEANUP_TASK_SCHEDULE))
def delete_unused_media_files():
    """
    Celery Task to delete unused media files .
    """
    unused_media_timestamp = timezone.now() - datetime.timedelta(minutes=settings.CLEAN_TMP_MEDIA_OLDER_THAN)
    usermedias = UserMedia.objects.filter(profile__isnull=True, modified_timestamp__lt=unused_media_timestamp)

    if UserMedia.MEDIA_IMAGE == 'image':
        THUMBNAIL_SIZES = getattr(settings, 'PROFILE_PHOTO_THUMBNAIL_SIZES', [])
    else:
        THUMBNAIL_SIZES = getattr(settings, 'VIDEO_THUMBNAIL_SIZES', [(600, 400)])

    for usermedia in usermedias:
        filename, file_extension = usermedia.media.name.rsplit('.', 1)
        for width, height in THUMBNAIL_SIZES:
            default_storage.delete(
                '{filename}_{width}x{height}.jpg'.format(
                    filename=filename,
                    width=width,
                    height=height,
                )
            )
        default_storage.delete(usermedia.media.name)
    usermedias.delete()
