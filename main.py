import argparse
import sys
from core.reader import load_videos_from_files
from core.reports import get_report
from tabulate import tabulate


def main():
    parser = argparse.ArgumentParser(description="Generate reports from YouTube metrics CSV files.")
    parser.add_argument("--files", nargs="+", required=True, help="List of CSV files to process")
    parser.add_argument("--report", required=True, help="Report type (e.g., clickbait)")

    args = parser.parse_args()

    try:
        videos = load_videos_from_files(args.files)
        report_func = get_report(args.report)
        result = report_func(videos)

        if result:
            table = tabulate(result, headers="keys", tablefmt="grid", floatfmt=".1f")
            print(table)
        else:
            print("No videos match the criteria for this report.")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()