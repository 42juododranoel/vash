from filer.models import Image
from django.dispatch import receiver
from django.db.models.signals import post_save

from vash.utils import ImageProcessor


@receiver(post_save, sender=Image)
def post_process_image(sender, instance, created, raw, using, update_fields, **kwargs):
    processor = ImageProcessor(instance)
    processor.create_thumbnails()
