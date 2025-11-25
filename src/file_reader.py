import csv
from typing import List, Dict, Any

def read_csv_file(file_paths: List[str]) -> List[Dict[str,Any]]:
    """
    Функция читает данные из нескольких csv файлов и возвращает объединенные данные из всех файлов
    param:
        file_paths: Список путей к csv файлам

    return:
        List[Dict[str,Any]]: Возвращает список словарей - объединенные данные из всех файлов
    """
    all_data = []

    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if 'completed_tasks' in row:
                        row['completed_tasks'] = int(row['completed_tasks'])
                    if 'performance' in row:
                        row['performance'] = int(row['performance'])
                    if 'expirience_years' in row:
                        row['expirience_years'] = int(row['expirience_years'])

                    all_data.append(row)
        except FileNotFoundError:
            raise FileNotFoundError(f'File {file_path} not found.')
        except Exception as e:
            raise Exception(f'Error reading {file_path}: {e}')

    return all_data