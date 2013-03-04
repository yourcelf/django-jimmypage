from django.core.management.base import BaseCommand
from jimmypage.cache import clear_cache

class Command(BaseCommand):
    help = "Increments the cache generation"
    def handle(self, *args, **options):
        clear_cache()