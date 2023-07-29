import json
from django.core.management.base import BaseCommand
from universities.models import University


class Command(BaseCommand):
    help = 'Load universities data from JSON file'

    def handle(self, *args, **kwargs):
        with open('universities.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            for entry in data:
                name = entry.get('name')
                country = entry.get('country')
                domains = entry.get('domains', [])
                web_pages = entry.get('web_pages', [])
                state = entry.get('state-province')

                if not name or not country:
                    self.stdout.write(self.style.WARNING(f"Skipping entry: {entry}. Missing required fields."))
                    continue

                domain = None
                if domains:
                    domain = domains[0]

                university = University.objects.create(
                    name=name,
                    country=country,
                    domain=domain,
                    state=state if state else None
                )
                self.stdout.write(self.style.SUCCESS(f"Successfully created University: {university}"))
