import csv
import os

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from users.models import User


class Command(BaseCommand):
    help = 'populates users_user table'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_name = User

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

    def insert_users_to_db(self, data):
        try:
            self.model_name.objects.create(
                id=data['id'],
                username=data['username'],
                email=data['email'],
                role=data['role'],
                bio=data['bio'],
                first_name=data['first_name'],
                last_name=data['last_name']
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
                        data['username'] = row[1]
                        data['email'] = row[2]
                        data['role'] = row[3]
                        data['bio'] = row[4]
                        data['first_name'] = row[5]
                        data['last_name'] = row[6]
                        self.insert_users_to_db(data)
                    line_count += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f'{line_count} entries added to Users'
                )
            )
        except FileNotFoundError:
            raise CommandError(f'File {file_path} does not exist')
