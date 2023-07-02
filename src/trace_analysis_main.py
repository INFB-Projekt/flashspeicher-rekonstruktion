import argparse

from dump_converter import Dump
from csv_exporter import Exporter

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="executes essential sub-scripts, filtering all write commands and gracefully saves the resulting trace to resources/filtered_trace")
    parser.add_argument('--logger_level', default="INFO", choices={"ERROR", "INFO", "DEBUG"}, help='ERROR = no logs, INFO = basic info (default), DEBUG = ultimate info')
    parser.add_argument('--hex', default=False, action='store_true', help='uses already converted hex files for analyzing,  if this flag is not set it uses a trace in binary and converts it to hex')
    parser.add_argument('--fname', required=True, help='Filename of trace which should be analyzed')

    args = parser.parse_args()
    config = vars(args)

    if config['hex']:
        d = Dump(f"../resources/hex/{config['fname']}", config['logger_level'], is_hex=True)
    else:
        d = Dump(f"../resources/bin/{config['fname']}", config['logger_level'], is_hex=False)

    trace = d.extract_writes()
    exporter = Exporter("../resources/filtered_trace")
    exporter.export_trace(trace)

