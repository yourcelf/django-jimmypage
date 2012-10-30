from jimmypage.cache import clear_cache

class Command(BaseCommand):
    help = "Increments the cache generation"
    def handle(self, *args, **options):
        clear_cache()