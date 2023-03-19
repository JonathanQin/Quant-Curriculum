import numpy as np
import pandas as pd
import random
import math

class CoinBetting:
    def __init__(self, bias = 0.7, num_players = 5):
        self.bias = bias
        self.players = np.zeros(num_players)
        # you are player 1, there are num_players-1 other players
        for i in range(num_players):
            self.players[i] = 1000
        self.round = 1
        self.bets = []
        self.inference_probability = 0.5
        self.heads = 1
        self.tails = 1
        self.flips = []
        self.start()
        
    def start(self):
        print("Round {} is starting! Place bets on H or T, and the corresponding value, i.e. H 20 for a bet of 20 on heads:".format(self.round))
        self.get_player_stack()
        print("\nPlace bet here: ")
        bet = input()
        self.bets.append(bet)
        print("You have bet ${} on {}!".format(float(bet[2:]), bet[0]))
        self.simulate_round()
        
    def get_player_stack(self):
        for i in range(len(self.players)):
            print("Player {} has ${} remaining!".format(i+1, round(self.players[i], 4)))
            
    def simulate_round(self):
        flip_res = ""
        res = random.random()
        if res > self.bias:
            flip_res = "T"
            self.tails += 1
        else:
            flip_res = "H"
            self.heads += 1
        self.flips.append(flip_res)
        pot, winnings, diff_res = self.get_bets()
        # pot += float(self.bets[-1][2:])
        print("\nRound {}: the coin landed {}!".format(self.round, flip_res))
        print("There is a total of ${} in the pot. Your net profit for the round is {}!".format(pot, round(winnings, 4)))
        self.inference_probability = self.heads / (self.heads + self.tails) # probability of heads
        
        # update player stacks
        self.players[0] += winnings
        for i in range(len(self.players)):
            if i > 0:
                self.players[i] += diff_res[i-1]
        
        self.round += 1
        self.start()
        
    
    def get_bets(self):
        # bets = []
        coin_res = self.flips[-1]
        my_bet = self.bets[-1]
        heads_bet = 0
        tails_bet = 0
        pot = 0
        flip_res = ["T", "H"]
        temp_bets = []
        temp_bet_res = []
        diff_res = []
        for i in range(len(self.players)):
            if i > 0:
                res = random.random()
                bet_res = (res <= self.inference_probability)
                p = bet_res * self.inference_probability + (1-bet_res) * (1-self.inference_probability)
                b = bet_res * (1 / self.inference_probability) + (1-bet_res) * (1 / self.inference_probability)
                bet_amount = self.players[i] * self.kelly(p, b) + random.normalvariate(0, 10)
                heads_bet += bet_res * bet_amount
                tails_bet += (1-bet_res) * bet_amount
                pot += bet_amount
                print("Player {} bet ${} on {} this round!".format(i+1, round(bet_amount, 4), flip_res[bet_res]))
                temp_bets.append(bet_amount)
                temp_bet_res.append(flip_res[bet_res])
        pot += float(my_bet[2:])
        winnings = 0
        if(my_bet[0] == coin_res):
            if coin_res == "H":
                winnings = pot * float(my_bet[2:])/(float(my_bet[2:]) + heads_bet) - float(my_bet[2:])
            else:
                winnings = pot * float(my_bet[2:])/(float(my_bet[2:]) + tails_bet) - float(my_bet[2:])
        else:
            winnings = 0 - float(my_bet[2:])
        for i in range(len(self.players)):
            if i > 0:
                diff = 0
                if(temp_bet_res[i-1] == coin_res):
                    if coin_res == "H":
                        diff = pot * (temp_bets[i-1]/(heads_bet)) - temp_bets[i-1]
                    else:
                        diff = pot * (temp_bets[i-1]/(tails_bet)) - temp_bets[i-1]
                else:
                    diff = 0 - temp_bets[i-1]
                diff_res.append(diff)
                # print(diff)
        return pot, winnings, diff_res
    
    def kelly(self, p, b):
        return max(min(p - ((1 - p)/b), 1/5), 1/50)
        
                    
if __name__ == "__main__":
    game = CoinBetting(0.75, 5)