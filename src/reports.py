from typing import List, Dict, Any
from abc import ABC, abstractmethod

class Report(ABC):
    """
    Abstract report class for all reports
    """
    @abstractmethod
    def generate_report(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate report from data

        :param:
            data: list of data

        return:
            List[Dict[str, Any]]: Sorted report
        """
        pass

    @abstractmethod
    def get_name(self):
        pass

class PerformanceReport(Report):
    """
    Performance report class
    """
    def generate_report(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate report from data

        :param:
            data: list of data
        return:
            List[Dict[str, Any]]: Sorted report
        """
        position_stats: {}

        for employee in data:
            position = employee["position"]
            performance = employee["performance"]

            if position not in position_stats:
                position_stats[position] = {
                    'performance_sum': 0,
                    'count': 0
                }

            position_stats[position]['performance_sum'] += performance
            position_stats[position]['count'] += 1

        report_data = []
        for position, stats in position_stats.items():
            avg_performance = stats['performance_sum'] / stats['count']
            report_data.append({
                'position': position,
                'avg_performance': round(avg_performance, 2),
                'employee_count': stats['count']
            })

        report_data.sort(key=lambda x: x['avg_performance'], reverse=True)

        return report_data

    def get_name(self):
        return "Performance Report"

class ReportFactory:
    """
    Fabric for creating reports
    """
    _reports = {
        'performance': PerformanceReport,
    }

    @classmethod
    def create_report(cls, report_name: str):
        """
        Create report instance by name
        :param
            report_name: name of report
        :return:
            report instance
        """
        if report_name not in cls._reports:
            available_reports = ', '.join(cls._reports.keys())
            raise Exception(
                f'Report named "{report_name}" not found, but has been added in the list. Now available reports: {available_reports}'
            )

        return cls._reports[report_name]()

    @classmethod
    def register_report(cls, report_name: str, report_class):
        """
        Register new type of report
        :param
            report_name: report name
            report_class: report class
        """
        if not issubclass(report_class, Report):
            raise ValueError("Report class must be a subclass of Report")

        cls._reports[report_name] = report_class

    @classmethod
    def get_available_report(cls) -> List[str]:
        """
        Return list of available reports
        """
        return list(cls._reports.keys())