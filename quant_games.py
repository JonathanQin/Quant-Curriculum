import numpy as np
import pandas as pd
import random
import math

class SportsBracket:
    def __init__(self, num_teams):
        if not math.log(num_teams, 2).is_integer():
            print("Please enter a power of 2 for the number of teams!")
            return
        self.n = num_teams
        self.rounds = 1
        self.num_rounds = math.log(num_teams, 2)
        team = {"id" : np.zeros((self.n)), "strength" : np.zeros((self.n))}
        self.team = pd.DataFrame.from_dict(team)
        self.team.reset_index()
        self.teams_in_play = self.team.index.tolist()

        self.generate_teams()
                
    def generate_teams(self):
        for i in self.teams_in_play:
            self.team["id"][i] = int(i + 1)
            self.team["strength"][i] = int(100 * random.randint(1, 8))
    
    def print_teams(self):
        print("\nThere are {} teams in play!".format(len(self.team["id"])))
        for i in self.teams_in_play:
            print("Team {} has strength {}".format(int(self.team["id"][i]), int(self.team["strength"][i])))
        print("\n")
            
    def simulate_round(self):
        print("Round{}!\nSimulating Round...".format(self.rounds))
        new_teams = []
        idx = self.teams_in_play
        for i in range(0, self.n, 2):
            t1 = self.team["strength"][idx[i]]
            t2 = self.team["strength"][idx[i+1]]
            total = t1 + t2
            res = random.randint(1, total)
            if res <= t1:
                new_teams.append(idx[i])
                print("Team {} beat team {}!".format(int(self.team["id"][idx[i]]), int(self.team["id"][idx[i+1]])))
            else:
                new_teams.append(idx[i+1])
                print("Team {} beat team {}!".format(int(self.team["id"][idx[i+1]]), int(self.team["id"][idx[i]])))
        # self.team = self.team[self.team['id'].isin(new_teams)]
        self.teams_in_play = new_teams
        self.n = len(self.teams_in_play)
        self.print_teams()
        self.rounds += 1

    def over(self):
        if self.rounds <= self.num_rounds:
            return True
        else:
            print("Team {} has won the game!".format(int(self.teams_in_play[0])))

if __name__ == "__main__":
    num_teams = 4
    game = SportsBracket(num_teams)
    game.print_teams()
    while(game.over()):
        x = input()
        game.simulate_round()


