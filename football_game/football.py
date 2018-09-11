import random
import numpy as np
class Football():

    def __init__(self, away, home):
        self.away = away
        self.home = home
        self.ls = 0 #line of scrimmage
        self.first_marker = 0 #first down marker
        self.down = 1 #down
        self.posession = None
        self.downs_ordinal = {1:'1st',2:'2nd', 3:'3rd', 4:'4th'}
        self.away_points = 0
        self.home_points = 0
        self.color_comment = ['What an amazing play!', 'That was incredible!']

    def start(self):
        self.coin_toss(self.away, self.home)

    def call_play(self):
        #strictly offense for now
        print("#"*10)
        print("The {0} have the ball at the {1} and it is {2} down and {3}.".format(self.posession, self.ls, self.downs_ordinal[self.down], self.first_marker - self.ls))

        while True:
                play_call = input('  Play option: Pass or Run (p/r)')
                if play_call in ['r','p']:
                    break
                else:
                    print("Not a valid input! Please enter p or r.")

        if play_call == 'p':
            self._pass()
            #the average completion percentage is around 65%. So we will use that as the decision line for completion.
            comp_determinant = np.random.random()
            if comp_determinant <= .65: #pass completed
                pass_complete = True
                gained_yards = round(np.random.normal(7,4),0)
            else: #pass incomplete
                pass_complete = False
                gained_yards = 0


        if play_call == 'r':
            self._run()
            gained_yards = round(np.random.normal(3.5,3),0)

        self.ls += gained_yards
        if self.ls > self.first_marker:
            self.down = 0
            self.first_marker = self.ls + 10
            if play_call == 'r':
                print("First Down!!! What a run!")

            else:
                print("First Down!!! What a catch!")

        self.down += 1
        if self.down < 4:
            if play_call == 'r':
                print(f"A run for {gained_yards} yards.")
            else:
                if pass_complete:
                    print(f"A pass and catch for {gained_yards} yards.")
                else:
                    print(f"Incomplete pass")
            self.call_play()
        else:
            if self.ls > 65:
                print("Kicking Field Goal")
                self.field_goal()
            else:
                print("Punting")
                self.punt()
                if self.posession == self.home:
                    self.posession = self.away
                else:
                    self.posession = self.home

    def _run(self):
        print('{} call a run play'.format(self.posession))

    def _pass(self):
        print('{} call a pass play'.format(self.posession))

    def coin_toss(self, away, home):
        coin = random.choice(['heads','tails'])
        away_choice = random.choice(['heads','tails'])

        #winning team prefers to kick-off.
        if away_choice == coin:
            print("{0} choose {1}. The coin flip is {2}. The {0} have chosen to kickoff.".format(self.away, away_choice, coin))
            self.kickoff(self.away, self.home)
        else:
            print("{0} choose {1}. The coin flip is {2}. The {3} have chosen to kickoff.".format(self.away, away_choice, coin, self.home))
            self.kickoff(self.home, self.away)

    def kickoff(self,kicking_off, returning):

        #using a normal distribution for the kick off distance, with a mean of 62.5 and standard deviation of 3
        kickoff = np.random.normal(62.5, 3)
        start = round(100 - 35 - kickoff,0)

        #using a beta distribution with alpha as 2 and beta as 5 for the return yards
        return_yards = round(np.random.beta(2,5) * 100,0)

        #making some adjustments for really long returns as they are more likely to score.
        if return_yards > 60:
            return_yards = round(np.random.beta(5,1) * 100,0)
        self.ls = max(min(start + return_yards,100),0)

        if self.ls == 100:
            print("\nTouchdown!!!! What an amazing return")
        else:
            print("\n{0} kicks off to the {2} yard line and the {1} have returned it for {3} yards. The {1} will start at the {4}.".format(kicking_off, returning, start, return_yards, self.ls))
            if return_yards > 40:
                print(random.choice(self.color_comment))
        self.first_marker = self.ls + 10
        self.posession = returning

    def punt(self):
        pass

    def fumble(self):
        pass

    def sack(self):
        pass

    def interception(self):
        pass

    def touchdown(self):
        pass

    def field_goal(self):
        pass

if __name__ == "__main__":
    game = Football('49ers', 'Raiders')
    game.start()
    game.call_play()
