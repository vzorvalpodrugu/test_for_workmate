import pytest
from src.reports import PerformanceReport, ReportFactory, Report


class TestPerformanceReport:
    """Тесты для отчета по эффективности."""

    def test_generate_report(self):
        """Тест генерации отчета по эффективности."""
        test_data = [
            {
                'name': 'Alex Ivanov',
                'position': 'Backend Developer',
                'completed_tasks': 45,
                'performance': 4.8,
                'skills': 'Python, Django',
                'team': 'API Team',
                'experience_years': 5
            },
            {
                'name': 'Maria Petrova',
                'position': 'Frontend Developer',
                'completed_tasks': 38,
                'performance': 4.7,
                'skills': 'React, CSS',
                'team': 'Web Team',
                'experience_years': 4
            },
            {
                'name': 'John Smith',
                'position': 'Backend Developer',
                'completed_tasks': 50,
                'performance': 4.9,
                'skills': 'Python, SQL',
                'team': 'API Team',
                'experience_years': 3
            }
        ]

        report = PerformanceReport()
        result = report.generate_report(test_data)

        # Проверяем количество позиций
        assert len(result) == 2

        # Проверяем что позиции есть в результате
        positions = [item['position'] for item in result]
        assert 'Backend Developer' in positions
        assert 'Frontend Developer' in positions

        # Проверяем вычисление средней эффективности
        backend_data = next(
            item for item in result if item['position'] == 'Backend Developer')
        frontend_data = next(item for item in result if
                             item['position'] == 'Frontend Developer')

        assert backend_data['average_performance'] == 4.85  # (4.8 + 4.9) / 2
        assert backend_data['employee_count'] == 2
        assert frontend_data['average_performance'] == 4.7
        assert frontend_data['employee_count'] == 1

        # Проверяем сортировку (по убыванию эффективности)
        assert result[0]['average_performance'] >= result[1][
            'average_performance']

    def test_empty_data(self):
        """Тест с пустыми данными."""
        report = PerformanceReport()
        result = report.generate_report([])
        assert result == []

    def test_get_name(self):
        """Тест получения названия отчета."""
        report = PerformanceReport()
        assert report.get_name() == 'performance'


class TestReportFactory:
    """Тесты для фабрики отчетов."""

    def test_create_existing_report(self):
        """Тест создания существующего отчета."""
        report = ReportFactory.create_report('performance')
        assert isinstance(report, PerformanceReport)

    def test_create_nonexistent_report(self):
        """Тест создания несуществующего отчета."""
        with pytest.raises(ValueError):
            ReportFactory.create_report('nonexistent')

    def test_register_new_report(self):
        """Тест регистрации нового отчета."""

        class TestReport(Report):
            def generate_report(self, data):
                return [{'test': 'data'}]

            def get_name(self):
                return 'test'

        # Регистрируем новый отчет
        ReportFactory.register_report('test_report', TestReport)

        # Проверяем что можно создать
        report = ReportFactory.create_report('test_report')
        assert isinstance(report, TestReport)

        # Проверяем что появился в списке доступных
        available_reports = ReportFactory.get_available_reports()
        assert 'test_report' in available_reports

    def test_register_invalid_report(self):
        """Тест регистрации некорректного отчета."""

        class InvalidClass:
            pass

        with pytest.raises(ValueError,
                           match="Report class must be a subclass of Report"):
            ReportFactory.register_report('invalid', InvalidClass)