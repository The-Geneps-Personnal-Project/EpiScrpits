# EpiScripts

## Overview

EpiScripts is a collection of Python scripts designed for various tasks and projects. This repository aims to provide solutions for common problems in data processing, analysis, and automation.

## Contents

- **HUB**: Hub activity calculator.
- **LOGTIME**: Scripts for logging and tracking time.
- **PCP**: PCP credits calculator.
- **STUMPER**: Group generator for Stumpers.
- **ZAPPY**: Run Epitech Zappy project scripts.

## Getting Started

### Prerequisites

- Python 3.x

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/The-Geneps-Personnal-Project/EpiScrpits.git
   ```

2. Navigate to the repository:
   ```bash
   cd EpiScripts
   ```


## Usage

```bash
python3 main.py [option] -h 
```

### Alert
If an issue occurs when running the script using an export from the intra. Open the csv manually, save as, change filter and select OK to reformat it correctly

## Exemples

### HUB

```bash
python3 main.py hub filename.csv [--promo] [--act] [--has-result] [--organisatiors_file]
```

Default values:
- `--promo`: All promos
- `--act`: fg (Focus Group)
- `--has-result`: All (display only those with a result)
- `--organisatiors_file`: `HUB/organisators.json` (file containing the list of organisers)

### LOGTIME

```bash
python3 main.py logtime filename.csv
```

### PCP

```bash
python3 main.py pcp filename.csv [--tek]
```

Default values:
- `--tek`: All (to specify a promo, use the format `--tek=tek3` and prepare a file PCP/tek[x].csv with export list of students)

### STUMPER

```bash
python3 main.py stumper filename.csv previous_group.csv registered.csv
```

### Synthesis Stumper
   
```bash
python3 main.py synthesis_stumper filename.csv
```

### ZAPPY

WIP: Testing the script in real conditions

```bash
python3 main.py zappy config.json
```

