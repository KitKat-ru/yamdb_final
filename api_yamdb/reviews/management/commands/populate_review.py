import csv
import os

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from reviews.models import Review, Title
from users.models import User


class Command(BaseCommand):
    help = 'populates reviews_review table'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_name = Review

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='filename for csv file')

    def get_current_app_path(self):
        return apps.get_app_config('static').path

    def get_csv_file(self, filename):
        app_path = self.get_current_app_path()
        return os.path.join(app_path, "data", filename)

    def clear_model(self):
        try:
            self.model_name.objects.all().delete()
        except Exception as e:
            raise CommandError(
                f'Error in clearing {self.model_name}: {str(e)}'
            )

    def insert_title_to_db(self, data):
        try:
            self.model_name.objects.create(
                id=data['id'],
                title=data['title'],
                text=data['text'],
                author=data['author'],
                score=data['score'],
                pub_date=['pub_date']
            )
        except Exception as e:
            raise CommandError(
                f'Error in inserting {self.model_name}: {str(e)}'
            )

    def handle(self, *args, **kwargs):
        filename = kwargs['filename']
        self.stdout.write(self.style.SUCCESS(f'filename:{filename}'))
        file_path = self.get_csv_file(filename)
        line_count = 0
        try:
            with open(file_path, encoding='utf-8') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                self.clear_model()
                for row in csv_reader:
                    if row != '' and line_count >= 1:
                        data = {}
                        data['id'] = row[0]
                        data['title'] = Title.objects.get(pk=row[1])
                        data['text'] = row[2]
                        data['author'] = User.objects.get(pk=row[3])
                        data['score'] = row[4]
                        data['pub_date'] = row[5]
                        self.insert_title_to_db(data)
                    line_count += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f'{line_count} entries added to Review'
                )
            )
        except FileNotFoundError:
            raise CommandError(f'File {file_path} does not exist')
