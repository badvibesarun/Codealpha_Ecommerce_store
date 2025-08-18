from django.core.management.base import BaseCommand
from django.conf import settings
import os
import shutil

class Command(BaseCommand):
    help = 'Syncs media files to the production media directory'

    def handle(self, *args, **kwargs):
        media_root = settings.MEDIA_ROOT
        if not os.path.exists(media_root):
            os.makedirs(media_root)

        # Copy product images
        products_dir = os.path.join(media_root, 'products')
        if not os.path.exists(products_dir):
            os.makedirs(products_dir)

        self.stdout.write('Syncing media files...')
        # Copy all files from media/products to production media directory
        source_dir = os.path.join(settings.BASE_DIR, 'media', 'products')
        if os.path.exists(source_dir):
            for filename in os.listdir(source_dir):
                source = os.path.join(source_dir, filename)
                destination = os.path.join(products_dir, filename)
                if os.path.isfile(source):
                    shutil.copy2(source, destination)
                    self.stdout.write(f'Copied {filename}')

        self.stdout.write(self.style.SUCCESS('Successfully synced media files'))
