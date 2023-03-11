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
        self.num_rounds = int(math.log(num_teams, 2))
        team = {"id" : np.zeros((self.n)), "strength" : np.zeros((self.n))}
        self.team = pd.DataFrame.from_dict(team)
        self.team.reset_index()
        self.teams_in_play = self.team.index.tolist()
        self.pwin = np.zeros((self.n, self.n))
        self.roundwin = np.zeros((self.n, self.num_rounds))
        self.totalwin = np.ones((self.n, self.num_rounds))
        self.payout = np.zeros((self.n, self.num_rounds))
        self.generate_teams()
        self.generate_probabilities()
                
    def generate_teams(self):
        for i in self.teams_in_play:
            self.team["id"][i] = int(i + 1)
            self.team["strength"][i] = int(100 * random.randint(1, 8))
        # self.team["strength"][0] = 100
        # self.team["strength"][1] = 400
        # self.team["strength"][2] = 300 
        # self.team["strength"][3] = 400
        
    def generate_probabilities(self):
        played = np.zeros((self.n, self.n))
        for i in self.teams_in_play:
            for j in self.teams_in_play:
                self.pwin[i][j] = (self.team["strength"][i]) / (self.team["strength"][i] + self.team["strength"][j])
        for i in self.teams_in_play:
            if i%2:
                self.roundwin[i][0] = self.pwin[i][i-1]
                played[i][i-1] = 1
            else:
                self.roundwin[i][0] = self.pwin[i][i+1]
                played[i][i+1] = 1
        for j in range(1, self.num_rounds):
            for i in self.teams_in_play:
                counter = math.pow(2, j+1)
                res = int(i/counter)
                a = int(res * counter)
                b = int(a + counter)
                for k in range(a, b):
                    if i != k and played[i][k] == 0:
                        self.roundwin[i][j] += self.roundwin[i][j-1] * self.roundwin[k][j-1] * self.pwin[i][k]
                    played[i][k] = 1
                # print(self.roundwin[i][j])
        for i in self.teams_in_play:
            print("Team {} has probability {} of winning!".format(i+1, round(self.roundwin[i][self.num_rounds-1], 4)))
            for j in range(0, self.num_rounds):
                if j == 0:
                    self.payout[i][j] = (self.roundwin[i][self.num_rounds-1-j]) * 100
                else:
                    self.payout[i][j] = (self.roundwin[i][self.num_rounds-1])/(self.roundwin[i][j-1]) * 100
                print("Payout for round {} is {}".format(j, round(self.payout[i][j], 2)))
            print("\n")
                
            

    def print_teams(self):
        print("\nThere are {} teams in play!".format(len(self.teams_in_play)))
        for i in self.teams_in_play:
            print("Team {} has strength {}".format(int(self.team["id"][i]), int(self.team["strength"][i])))
        print("\n")
            
    def simulate_round(self):
        if not self.not_over():
            print("Game is already over!")
            return
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

    def not_over(self):
        if self.rounds <= self.num_rounds:
            return True
        else:
            print("Team {} has won the game!".format(int(self.teams_in_play[0])))
            return False

if __name__ == "__main__":
    num_teams = 4
    game = SportsBracket(num_teams)
    game.print_teams()
    while(game.not_over()):
        game.simulate_round()
    


