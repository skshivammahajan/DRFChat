import uuid

from django.core.files.storage import default_storage
from django.test import TestCase
from PIL import Image

from experchat.utils import create_image_thumbnail


class TestThumbnailUtil(TestCase):

    def setUp(self):
        # Generate unique file name to avoid
        self.filename = uuid.uuid4().hex
        self.width = 256
        self.height = 256

    def test_thumbnail_creation(self):
        image = Image.open('media/sample.png')

        create_image_thumbnail(image, self.width, self.height, self.filename)

        assert default_storage.exists(
            '{filename}_{width}x{height}.jpg'.format(
                filename=self.filename,
                width=self.width,
                height=self.height,
            )
        )

    def tearDown(self):
        default_storage.delete(
            '{filename}_{width}x{height}.jpg'.format(
                filename=self.filename,
                width=self.width,
                height=self.height,
            )
        )
