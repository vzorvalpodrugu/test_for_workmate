import argparse
from tabulate import tabulate
from .file_reader import read_csv_file
from .reports import ReportFactory

def main():
    """
    Main function for run scripts with command line arguments
    """
    parser = argparse.ArgumentParser(
        description = 'Generator reports from CSV-files',
        formatter_class = argparse.RawDescriptionHelpFormatter,
        epilog="""
        Examples usage:
        python -m src.cli --files data1.csv data2.csv --report perfomance
        python -m src.cli -f employees.csv -r perfomance
        """
    )

    parser.add_argument(
        '--files', '-f',
        nargs = '+',
        required = True,
        help = 'Path to CSV-files'
    )

    parser.add_argument(
        '--report', '-r',
        required = True,
        help = f'Report name. Available reports: {",".join(ReportFactory.get_available_report())}'
    )

    args = parser.parse_args()

    try:
        data = read_csv_file(args.files)

        if not data:
            print('No data found')
            return

        report = ReportFactory.create_report(args.report)
        report_data = report.generate_report(data)

        if report_data:
            headers = report_data[0].keys()
            rows = [list(item.values()) for item in report_data]
            print(tabulate(rows, headers=headers, tablefmt='grid'))
        else:
            print('No data found')

    except Exception as e:
        print(f'Error: {e}')
        return 1

    return 0

if __name__ == '__main__':
    exit(main())
