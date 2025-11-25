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

class PerfomanceReport(Report):
    """
    Perfomance report class
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
            perfomance = employee["perfomance"]

            if position not in position_stats:
                position_stats[position] = {
                    'perfomance_sum': 0,
                    'count': 0
                }

            position_stats[position]['perfomance_sum'] += perfomance
            position_stats[position]['count'] += 1

        report_data = []
        for position, stats in position_stats.items():
            avg_perfomance = stats['perfomance_sum'] / stats['count']
            report_data.append({
                'position': position,
                'avg_perfomance': round(avg_perfomance, 2),
                'employee_count': stats['count']
            })

        report_data.sort(key=lambda x: x['avg_perfomance'], reverse=True)

        return report_data

    def get_name(self):
        return "Perfomance Report"