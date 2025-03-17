# chkfccbdc

A Python script to check FCC Broadband Data Collection (BDC) directory structures for missing or outdated files.

## Overview

`chkfccbdc` scans a specified directory containing FCC BDC data, organized by state and territory, to identify:
- Missing directories or files matching the pattern `\d{2}_[A-Z]{2}_BB(_4269|\.)(geojson|gpkg)`.
- Files older than a user-specified cutoff date-time, with an optional delete feature.

The script uses a list of U.S. states and territories from `constants.py` and supports American or international date formats based on system locale.

## Features

- Validates directory structure against expected state/territory codes.
- Matches files like `01_AL_BB.geojson`, `01_AL_BB.gpkg`, `01_AL_BB_4269.geojson`.
- Checks file modification times against a cutoff date.
- Optionally deletes outdated files.
- Detailed debug output for troubleshooting.

## Prerequisites

- Python 3.6 or higher (uses standard libraries only).
- A directory structure like `/base-dir/USA_FCC-bdc/<FIPS>_<ABBR>_<NAME>/` containing BDC files.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/chkfccbdc.git
   cd chkfccbdc
(Optional) Create and activate a virtual environment:
bash

Collapse

Wrap

Copy
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies (none beyond Python standard libraries, but included for completeness):
bash

Collapse

Wrap

Copy
pip install -r requirements.txt
Usage
Run the script from the command line with required arguments:

bash

Collapse

Wrap

Copy
python src/main.py --base-dir <path-to-data> --date-time "<cutoff-date-time>" [--delete]
Arguments
--base-dir: Path to the directory containing USA_FCC-bdc/ (required).
--date-time: Cutoff date-time (e.g., "03/17/2025-11:59 pm" or "17/03/2025 23:59") (required).
--delete: Optional flag to delete files older than the cutoff.
Examples
Check for missing or old files:
bash

Collapse

Wrap

Copy
python src/main.py --base-dir "/Volumes/T7 Shield/SharedData" --date-time "03/13/2025-11:59 pm"
Delete outdated files:
bash

Collapse

Wrap

Copy
python src/main.py --base-dir "/Volumes/T7 Shield/SharedData" --date-time "03/13/2025-11:59 pm" --delete
Output
The script prints:

Base path and file pattern used.
Per-directory file listings and matches.
Modification time comparisons (e.g., Older: False).
Affected state abbreviations (e.g., AL AK OR).
Example:

text

Collapse

Wrap

Copy
Checking base path: /Volumes/T7 Shield/SharedData/USA_FCC-bdc
Using FILE_PATTERN: ^\d{2}_[A-Z]{2}_BB(_4269|\.)(geojson|gpkg)$
Processing directory: /Volumes/T7 Shield/SharedData/USA_FCC-bdc/01_AL_Alabama
All files in ...: ['01_AL_BB.geojson', '01_AL_BB.gpkg', '01_AL_BB_4269.geojson', ...]
Matched files: ['01_AL_BB.geojson', '01_AL_BB.gpkg', '01_AL_BB_4269.geojson']
Matched file: .../01_AL_BB.geojson (mtime: 2025-03-15 00:30:57.730000)
Cutoff: 2025-03-13 23:59:00, File mtime: ..., Older: False
Affected state abbreviations: ...
Project Structure
text

Collapse

Wrap

Copy
chkfccbdc/
├── src/
│   ├── main.py        # Main script
│   └── constants.py   # State/territory codes and other constants
├── README.md          # This file
└── requirements.txt   # Dependencies (empty for now)
Contributing
Fork the repository.
Create a feature branch (git checkout -b feature-branch).
Commit changes (git commit -m "Add feature").
Push to the branch (git push origin feature-branch).
Open a pull request.
License
This project is licensed under the MIT License. See LICENSE for details (add a LICENSE file if desired).

Contact
For issues or suggestions, open an issue on GitHub or contact <your-email> (optional).