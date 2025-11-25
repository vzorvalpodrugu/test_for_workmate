import pytest
import tempfile
import os
from src.file_reader import read_csv_file


def create_test_csv(content: str) -> str:
    """Создает временный CSV файл с заданным содержимым."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv',
                                     delete=False) as f:
        f.write(content)
        return f.name


class TestFileReader:
    """Тесты для модуля чтения файлов."""

    def test_read_single_file(self):
        """Тест чтения одного файла."""
        csv_content = """name,position,completed_tasks,performance,skills,team,experience_years
Alex Ivanov,Backend Developer,45,4.8,"Python, Django, PostgreSQL, Docker",API Team,5
Maria Petrova,Frontend Developer,38,4.7,"React, TypeScript, Redux, CSS",Web Team,4
John Smith,Data Scientist,29,4.6,"Python, ML, SQL, Pandas",AI Team,3
Anna Lee,DevOps Engineer,52,4.9,"AWS, Kubernetes, Terraform, Ansible",Infrastructure Team,6
Mike Brown,QA Engineer,41,4.5,"Selenium, Jest, Cypress, Postman",Testing Team,4
"""

        file_path = create_test_csv(csv_content)

        try:
            data = read_csv_file([file_path])

            assert len(data) == 2
            assert data[0]['name'] == 'Alex Ivanov'
            assert data[0]['position'] == 'Backend Developer'
            assert data[0]['completed_tasks'] == 45
            assert data[0]['performance'] == 4.8
            assert data[0]['experience_years'] == 5

            assert data[1]['name'] == 'Maria Petrova'
            assert data[1]['position'] == 'Frontend Developer'
            assert data[1]['completed_tasks'] == 38
            assert data[1]['performance'] == 4.7
            assert data[1]['experience_years'] == 4

        finally:
            os.unlink(file_path)

    def test_read_multiple_files(self):
        """Тест чтения нескольких файлов."""
        csv_content1 = """name,position,completed_tasks,performance,skills,team,experience_years
Alex Ivanov,Backend Developer,45,4.8,"Python, Django",API Team,5"""

        csv_content2 = """name,position,completed_tasks,performance,skills,team,experience_years
Maria Petrova,Frontend Developer,38,4.7,"React, CSS",Web Team,4"""

        file1 = create_test_csv(csv_content1)
        file2 = create_test_csv(csv_content2)

        try:
            data = read_csv_file([file1, file2])

            assert len(data) == 2
            positions = [item['position'] for item in data]
            assert 'Backend Developer' in positions
            assert 'Frontend Developer' in positions

        finally:
            os.unlink(file1)
            os.unlink(file2)

    def test_file_not_found(self):
        """Тест обработки отсутствующего файла."""
        with pytest.raises(FileNotFoundError):
            read_csv_file(['nonexistent_file.csv'])

    def test_data_conversion(self):
        """Тест конвертации числовых полей."""
        csv_content = """name,position,completed_tasks,performance,skills,team,experience_years
John Smith,Data Scientist,29,4.6,"Python, ML",AI Team,3"""

        file_path = create_test_csv(csv_content)

        try:
            data = read_csv_file([file_path])

            assert isinstance(data[0]['completed_tasks'], int)
            assert isinstance(data[0]['performance'], float)
            assert isinstance(data[0]['experience_years'], int)

        finally:
            os.unlink(file_path)