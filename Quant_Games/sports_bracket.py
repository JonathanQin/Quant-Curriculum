import numpy as np
import pandas as pd
import random
import math

class SportsBracket:
    def __init__(self, num_teams):
        if not math.log(num_teams, 2).is_integer():
            print("Please enter a power of 2 for the number of teams!")
            return
        self.total_teams = num_teams
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
        self.pricing = np.zeros((self.n, self.num_rounds))
        self.positions = np.zeros((self.n))
        self.generate_teams()
        self.generate_probabilities()
        self.total_bets = 0
        self.total_winnings = 0
                
    def generate_teams(self):
        for i in self.teams_in_play:
            self.team["id"][i] = int(i + 1)
            self.team["strength"][i] = int(100 * random.randint(1, self.total_teams))
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
        for i in self.teams_in_play:
            # print("Team {} has probability {} of winning!".format(i+1, round(self.roundwin[i][self.num_rounds-1], 4)))
            for j in range(0, self.num_rounds):
                if j == 0:
                    self.payout[i][j] = (self.roundwin[i][self.num_rounds-1-j]) * 100
                else:
                    self.payout[i][j] = (self.roundwin[i][self.num_rounds-1])/(self.roundwin[i][j-1]) * 100
                # self.pricing[i][j] = self.payout[i][j] 
                self.pricing[i][j] = self.payout[i][j] + random.normalvariate(2, 2)
                # print("Payout for round {} is {}".format(j, round(self.payout[i][j], 2)))
            # print("\n")
                
    def print_probabilities(self):
        for i in range(int(self.total_teams)):
            for j in range(int(self.num_rounds)):
                print("Round {} probabilities: ".format(j + 1))
                self.get_payouts(j + 1)

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
        # self.print_teams()
        self.rounds += 1
        
    def get_payouts(self, round_num = -1):
        if round_num == -1:
            round_num = self.rounds
        for i in range(0, len(self.team.index.to_list())):
            j = round_num - 1
            print("For Team {}, payout for round {} is {}".format(i + 1, round_num, round(self.payout[i][j], 2)))
        print("\n")
        
    def get_pricing(self, round_num = -1):
        if round_num == -1:
            round_num = self.rounds
            print("Betting is starting for round {}! Which teams you wish to bet on (in a list / 'none'): ".format(self.rounds) )
            betting = True
        for i in self.teams_in_play:
            j = round_num-1
            print("For Team {} with strength {}, a bet for round {} costs {}".format(i + 1, int(self.team["strength"][i]), round_num, round(self.pricing[i][j], 2)))
        print("\n")
        if betting:
            bet_list = input()
            if(bet_list.lower() == "none"):
                print("You have made no bets this round\n")
            else:
                for i in bet_list:
                    if(i == " "):
                        continue
                    pos = int(i)
                    self.total_bets += self.pricing[pos-1][round_num-1]
                    self.positions[pos-1] += 1
                    print("You have placed a bet on team {} for {}".format(i, self.pricing[pos-1][round_num-1]))
                print("\n")

    def not_over(self):
        if self.rounds <= self.num_rounds:
            return True
        else:
            winning_team = int(self.teams_in_play[0])
            self.total_winnings = self.positions[winning_team] * 100
            print("Team {} has won the game!".format(winning_team + 1))
            print("You had {} positions in team {}, giving profits of {}".format(self.positions[winning_team], winning_team + 1, self.total_winnings))
            print("However, you spent {} in total on bets, giving net profits of {}!".format(self.total_bets, self.total_winnings - self.total_bets))
            return False

if __name__ == "__main__":
    num_teams = 8
    game = SportsBracket(num_teams)
    game.print_teams()
    while(game.not_over()):
        game.get_pricing()
        game.simulate_round()
    game.print_probabilities()
    


