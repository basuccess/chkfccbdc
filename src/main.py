#!/usr/bin/env python3

import argparse
import os
import re
from datetime import datetime
import locale
from constant import STATES_AND_TERRITORIES

DATE_FORMATS = [
    "%m/%d/%Y", "%m/%d/%Y-%I:%M %p", "%m/%d/%Y-%H:%M",
    "%Y-%m-%d", "%Y-%m-%d %H:%M", "%d/%m/%Y", "%d/%m/%Y %H:%M",
    "%b %d %Y", "%B %d %Y %I:%M %p", "%Y%m%d", "%m.%d.%Y", "%m/%d/%Y %H:%M:%S"
]

# Define and test the regex
FILE_PATTERN = re.compile(r'^\d{2}_[A-Z]{2}_BB(_4269\.|\.)(geojson|gpkg)$')
# Sanity check
print(f"Sanity check: {FILE_PATTERN.match('01_AL_BB_4269.geojson')}")
print(f"Sanity check: {FILE_PATTERN.match('01_AL_BB.geojson')}")
print(f"Sanity check: {FILE_PATTERN.match('01_AL_BB.gpkg')}")

def get_system_date_formats():
    try:
        loc = locale.getlocale(locale.LC_TIME)
        if not loc or loc[0] is None:
            locale.setlocale(locale.LC_TIME, '')
            loc = locale.getlocale(locale.LC_TIME)
        lang_country = loc[0].lower() if loc[0] else 'en_us'
        is_american = 'us' in lang_country
        if is_american:
            prioritized = ["%m/%d/%Y", "%m/%d/%Y-%I:%M %p", "%m/%d/%Y-%H:%M"]
        else:
            prioritized = ["%d/%m/%Y", "%d/%m/%Y %H:%M", "%Y-%m-%d"]
        return prioritized + [fmt for fmt in DATE_FORMATS if fmt not in prioritized]
    except locale.Error:
        print("Warning: Could not determine system locale. Using default format list.")
        return DATE_FORMATS

def parse_datetime(date_str, formats):
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError("Invalid date-time format. Supported formats: " +
                     ", ".join(f"'{fmt}'" for fmt in formats))

def check_directory(base_dir, cutoff_datetime, delete=False):
    affected_states = set()
    expected_dirs = {f"{fips}_{abbr}_{name}" for fips, abbr, name in STATES_AND_TERRITORIES}

    bdc_path = os.path.join(base_dir, "USA_FCC-bdc")
    print(f"Checking base path: {bdc_path}")
    print(f"Using FILE_PATTERN: {FILE_PATTERN.pattern}")

    for fips, abbr, name in STATES_AND_TERRITORIES:
        dir_name = f"{fips}_{abbr}_{name}"
        subdir = os.path.join(bdc_path, dir_name)
        
        if not os.path.isdir(subdir):
            affected_states.add(abbr)
            print(f"Missing directory: {subdir}")
            continue
        
        print(f"Processing directory: {subdir}")
        
        try:
            all_files = os.listdir(subdir)
            print(f"All files in {subdir}: {all_files}")
            files = []
            for f in all_files:
                match = FILE_PATTERN.match(f)
                print(f"Testing {f} (repr: {repr(f)}): {'Match' if match else 'No match'}")
                if match:
                    files.append(f)
            print(f"Matched files: {files}")
            
            if not files:
                affected_states.add(abbr)
                print(f"Missing files in {subdir}")
            else:
                for filename in files:
                    filepath = os.path.join(subdir, filename)
                    file_mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                    print(f"Matched file: {filepath} (mtime: {file_mtime})")
                    print(f"Cutoff: {cutoff_datetime}, File mtime: {file_mtime}, Older: {file_mtime < cutoff_datetime}")
                    
                    if file_mtime < cutoff_datetime:
                        affected_states.add(abbr)
                        print(f"Older file found: {filepath}")
                        if delete:
                            os.remove(filepath)
                            print(f"Deleted: {filepath}")
        except OSError as e:
            print(f"Error accessing {subdir}: {e}")
            affected_states.add(abbr)

    return sorted(affected_states)

def main():
    parser = argparse.ArgumentParser(description="Find missing or old files in FCC BDC directory structure.")
    parser.add_argument("--base-dir", required=True, help="Base directory containing USA_FCC-bdc")
    parser.add_argument("--date-time", required=True, 
                        help="Cutoff date-time (e.g., '03/17/2025' or '17/03/2025' based on system locale)")
    parser.add_argument("--delete", action="store_true", help="Delete files older than specified date-time")
    
    args = parser.parse_args()
    
    date_formats = get_system_date_formats()
    try:
        cutoff_datetime = parse_datetime(args.date_time, date_formats)
    except ValueError as e:
        print(e)
        return
    
    affected_states = check_directory(args.base_dir, cutoff_datetime, args.delete)
    print("Affected state abbreviations:", " ".join(affected_states))

if __name__ == "__main__":
    main()