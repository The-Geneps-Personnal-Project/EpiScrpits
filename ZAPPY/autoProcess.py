import json
import random
import os, signal
from multiprocessing import Pool, Process
from subprocess import Popen, PIPE, STDOUT


# ========================================= WIP =========================================

class Team:
    def __init__(self, name: str, ia_path:str, args:str):
        self.name = name
        self.ia_path = ia_path
        self.ia_args = args
        self.ias = []

    def __dict__(self) -> dict:
        return {
            "name": self.name,
            "ia_path": self.ia_path,
            "ia_args": self.ia_args,
            "ias": self.ias
        }
    
    @property
    def ias(self):
        return self._ias

    @property
    def name(self):
        return self.name

    @staticmethod
    def run_command(cmd, log_file):
        with open(log_file, "a") as f:
            process = Popen(cmd, shell=True, stdout=f, stderr=f)
            process.wait()

    def start_IAS(self):
        cmds = [f"{self.ia_path} {self.ia_args}" for _ in range(6)]
        log_file = f"{os.getcwd()}/{self.name}.log"

        for cmd in cmds:
            p = Process(target=Team.run_command, args=(cmd, log_file))
            p.start()
            self.ias.append(p)

        for p in self.ias:
            p.join()

class Tournament:
    def __init__(self, teams: list, nb_teams: int, gui: dict, server:dict):
        self.teams = [Team(**team) for team in teams]
        self.nb_teams = nb_teams
        self.gui_cmd = {k: v for k, v in gui.items() if k in ["path", "args"]}
        self.GUI = None
        self.server_cmd = {k: v for k, v in server.items() if k in ["path", "args"]} 
        self.server = None
        self.tree = self.make_tree()

    def to_dict(self) -> dict:
        return {
            "teams": [team.to_dict() for team in self.teams],
            "nb_teams": self.nb_teams,
            "gui_path": self.gui,
            "server_path": self.server,
            "tree": [self.tree[i][j].to_dict() for i in range(len(self.tree)) for j in [0, 1]]
        }
    
    def make_tree(self) -> list:
        random.shuffle(self.teams)
        return [[self.teams[i], self.teams[i + 1]] for i in range(0, len(self.teams), 2)]
    
    def start_match(self, team1: int, team2: int) -> str:
        team1: Team = self.teams[team1]
        team2: Team = self.teams[team2]

        print(f"Starting IAS for team 1: {team1.__dict__()}")
        print(f"Starting IAS for team 2: {team2.__dict__()}")

        team1_process = Process(target=team1.start_IAS)
        team2_process = Process(target=team2.start_IAS)

        team1_process.start()
        team2_process.start()

        team1_process.join()
        team2_process.join()

        print("IAS finished")

    def start_process(self):
        with open("server.log", "a") as server_log, open("GUI.log", "a") as GUI_log:
            self.server = Popen(f"{self.server_cmd.get('path')} {self.server_cmd.get('args')}", shell=True, stdout=server_log, stderr=server_log)
            self.GUI = Popen(f"{self.gui_cmd.get('path')} {self.gui_cmd.get('args')}", shell=True, stdout=GUI_log, stderr=GUI_log)
        

def checkConfig(tournament: Tournament) -> bool:
    if not tournament:
        raise ValueError("Config is empty")
    
    if (len(tournament.teams) != tournament.nb_teams):
        raise ValueError("Number of teams does not match nb_teams")
    
    return True

def zappy():
    with open("config.json", "r") as f:
        tournament = Tournament(**json.load(f))

    if not checkConfig(tournament):
        print("Config is not valid")
        exit(1)

    signal.signal(signal.SIGINT, lambda x, y:
                [os.killpg(os.getpgid(tournament.server.pid), signal.SIGTERM),
                os.killpg(os.getpgid(tournament.GUI.pid), signal.SIGTERM),
                (os.killpg(os.getpgid(team.ias[i].pid), signal.SIGTERM) for team in tournament.teams for i in range(6))])

    tournament.start_process()
    try:
        team1 = int(input("Enter the index of the first team: "))
        team2 = int(input("Enter the index of the second team: "))
    except ValueError:
        print("Please enter a valid number")
        exit(1)
    
    tournament.start_match(team1, team2)