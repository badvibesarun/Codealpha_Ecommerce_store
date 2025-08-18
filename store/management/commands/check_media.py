from django.core.management.base import BaseCommand
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Check media files configuration and availability'

    def handle(self, *args, **options):
        self.stdout.write("🔍 Media Configuration Check")
        self.stdout.write("-" * 40)
        
        # Check Django settings
        self.stdout.write(f"MEDIA_URL: {settings.MEDIA_URL}")
        self.stdout.write(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
        
        # Check if media directory exists
        if os.path.exists(settings.MEDIA_ROOT):
            self.stdout.write(f"✓ MEDIA_ROOT directory exists: {settings.MEDIA_ROOT}")
            
            # Check products subdirectory
            products_dir = os.path.join(settings.MEDIA_ROOT, 'products')
            if os.path.exists(products_dir):
                self.stdout.write(f"✓ Products directory exists: {products_dir}")
                
                # List some files
                files = os.listdir(products_dir)
                self.stdout.write(f"📁 Found {len(files)} files in products directory:")
                for i, file in enumerate(files[:5]):  # Show first 5 files
                    file_path = os.path.join(products_dir, file)
                    file_size = os.path.getsize(file_path)
                    self.stdout.write(f"   {i+1}. {file} ({file_size} bytes)")
                
                if len(files) > 5:
                    self.stdout.write(f"   ... and {len(files) - 5} more files")
                    
                # Check specific file that's failing
                test_file = os.path.join(products_dir, 'smartphone-pro_ultra_precise.jpg')
                if os.path.exists(test_file):
                    size = os.path.getsize(test_file)
                    self.stdout.write(f"✓ Test file exists: smartphone-pro_ultra_precise.jpg ({size} bytes)")
                else:
                    self.stdout.write("✗ Test file missing: smartphone-pro_ultra_precise.jpg")
            else:
                self.stdout.write(f"✗ Products directory missing: {products_dir}")
        else:
            self.stdout.write(f"✗ MEDIA_ROOT directory missing: {settings.MEDIA_ROOT}")
            
        # Check current working directory
        cwd = os.getcwd()
        self.stdout.write(f"📍 Current working directory: {cwd}")
        
        # Check if media files exist relative to CWD
        local_media = os.path.join(cwd, 'media', 'products')
        if os.path.exists(local_media):
            files = os.listdir(local_media)
            self.stdout.write(f"📁 Local media/products has {len(files)} files")
        else:
            self.stdout.write("✗ Local media/products directory not found")
