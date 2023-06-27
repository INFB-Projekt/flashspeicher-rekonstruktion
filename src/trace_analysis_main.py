import argparse

from dump_converter import Dump
from csv_exporter import Exporter

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--logger_level', default="ERROR", choices={"ERROR", "INFO", "DEBUG"}, help='ERROR = no logs, INFO = basic info, DEBUG = ultimate info')
    parser.add_argument('--hex', default=False, action='store_true')
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

