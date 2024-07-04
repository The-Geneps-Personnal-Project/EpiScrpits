import argparse
import sys
from HUB.autoHub import hub
from PCP.autoPCP import pcp
from STUMPER.autoStumper import stumper
from STUMPER.synStumper import synstumper
from LOGTIME.autoLogtime import logtime
from ZAPPY.autoProcess import zappy

def main():
    parser = argparse.ArgumentParser(description='Process Intra Informations.')
    subparsers = parser.add_subparsers(dest='script', help='sub-command help')

    pcp_parser = subparsers.add_parser('pcp', help='Process PCP data')
    pcp_parser.add_argument('filename', type=str, help='Path to the PCP file to process')
    pcp_parser.add_argument('--tek',type=int, help='Promo year to filter on', default=None)

    hub_parser = subparsers.add_parser('hub', help='Process HUB data')
    hub_parser.add_argument('filename', type=str, help='Path to the CSV file to process')
    hub_parser.add_argument('--promo', type=int, help='Filter by promo year', default=None)
    hub_parser.add_argument('--act', type=str, choices=['fablab', 'fg', 'both'], help='Activity type: "fablab", "fg" (focus group), or "both"', default='fg')
    hub_parser.add_argument('--has_result', type=str, choices=['all', 'yes', 'no'] ,help='Print only those with activities', default='all')
    hub_parser.add_argument('--organisators_file', type=str, help='Path to the organisators file', default="HUB/organisators.csv")

    stumper_parser = subparsers.add_parser('stumper', help='Process Stumper data')
    stumper_parser.add_argument('previous_duo', type=str, help='Path to the CSV file containing the previous duo')
    stumper_parser.add_argument('current_list', type=str, help='Path to the CSV file containing the registered students')

    logtime_parser = subparsers.add_parser('logtime', help='Process Logtime data')
    logtime_parser.add_argument('filename', type=str, help='Path to the CSV file to process')

    zappy_parser = subparsers.add_parser('zappy', help='Run Zappy tournament')
    zappy_parser.add_argument('filename', type=str, help='Path to the config file', default='ZAPPY/config.json')


    args = parser.parse_args()

    if args.script == 'hub':
        if args.act in ['fg', 'both'] and args.organisators_file is None:
            parser.error("--organisators_file is required when --act is 'fg' or 'both'.")

    # Call the function depenging on the args.script value => value = hub it calls function hub
    getattr(sys.modules[__name__], args.script)(args)

    pass

if __name__ == "__main__":
    main()