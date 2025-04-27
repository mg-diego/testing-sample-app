import json
import os
from .database import LanguageManagementDatabase

language_management_database = LanguageManagementDatabase()

def get_translations():
    active_language = language_management_database.get_active_language()
    return read_json_file(f'translations', f"{active_language}.json")

def set_active_language_service(new_active_language):
    return language_management_database.set_active_language(new_active_language)

def read_json_file(folder, filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, folder, filename)
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)
