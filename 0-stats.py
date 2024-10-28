#!/usr/bin/python3
import sys
import re
from signal import signal, SIGINT

# Initialize variables for metrics
total_file_size = 0
line_count = 0
status_codes_count = {code: 0 for code in [200, 301, 400, 401, 403, 404, 405, 500]}

def print_stats():
    """Prints the collected statistics."""
    print(f"File size: {total_file_size}")
    for code in sorted(status_codes_count):
        if status_codes_count[code] > 0:
            print(f"{code}: {status_codes_count[code]}")

def process_line(line):
    """Processes each line to update metrics."""
    global total_file_size, line_count
    # Regular expression pattern to match log lines
    pattern = r'(\d+\.\d+\.\d+\.\d+) - \[(.*?)\] "GET /projects/260 HTTP/1\.1" (\d{3}) (\d+)'
    match = re.match(pattern, line)
    if match:
        status_code = int(match.group(3))
        file_size = int(match.group(4))
        
        # Update metrics
        total_file_size += file_size
        if status_code in status_codes_count:
            status_codes_count[status_code] += 1
        line_count += 1

def main():
    global line_count

    # Signal handler for KeyboardInterrupt (CTRL+C)
    def signal_handler(sig, frame):
        print_stats()
        sys.exit(0)

    signal(SIGINT, signal_handler)

    # Read from stdin line by line
    try:
        for line in sys.stdin:
            process_line(line)
            # Every 10 lines, print the stats
            if line_count % 10 == 0:
                print_stats()
    except KeyboardInterrupt:
        # Print stats on keyboard interrupt
        print_stats()
        sys.exit(0)

if __name__ == "__main__":
    main()
