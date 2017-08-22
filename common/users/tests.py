import uuid

from django.conf import settings
from django.core.files.storage import default_storage
from django.test import TestCase

from users.utils import create_video_thumbnail


class TestVideoThumbnailUtil(TestCase):

    def setUp(self):
        # Generate unique file name to avoid
        self.filename = uuid.uuid4().hex
        self.video = 'media/sample.mp4'

    def test_video_thumbnail_creation(self):
        create_video_thumbnail(self.video, self.filename)

        for width, height in getattr(settings, 'VIDEO_THUMBNAIL_SIZES', [(600, 400)]):
            assert default_storage.exists(
                '{filename}_{width}x{height}.jpg'.format(
                    filename=self.filename,
                    width=width,
                    height=height,
                )
            )

    def tearDown(self):
        for width, height in getattr(settings, 'VIDEO_THUMBNAIL_SIZES', [(600, 400)]):
            default_storage.delete(
                '{filename}_{width}x{height}.jpg'.format(
                    filename=self.filename,
                    width=width,
                    height=height,
                )
            )
