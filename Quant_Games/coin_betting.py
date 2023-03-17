import numpy as np
import pandas as pd
import random
import math

class CoinBetting:
    def __init__(self, bias):
        if bias < 0 or bias > 1:
            print("Bias should be between 0 and 1.")