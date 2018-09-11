import random
import numpy as np
from itertools import cycle

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
        self.scoring_points = {'touchdown':6, 'PAT':1, 'FG':3}


    def call_play(self):
        """
        Prompts the user for a play pass(p) or run(r). Does the play simulation and prints result.
        """

        self.score_board() #single line that simulates where the team is on the field and the score of the game

        #checks to see if we are at goalline, if not prints first and required yards for first down.
        if self.ls>=90:
            print("The {0} have the ball at the {1} and it's {2} down and goal.".format(self.posession, self.ls, self.downs_ordinal[self.down]))
        else:
            print("The {0} have the ball at the {1} and it's {2} down and {3}.".format(self.posession, self.ls, self.downs_ordinal[self.down], self.first_marker - self.ls))

        #prompts user for play call.
        while True:
                play_call = input('  Play option: Pass or Run (p/r)')
                if play_call in ['r','p']:
                    break
                else:
                    print("Not a valid input! Please enter p or r.")

        if play_call == 'p':
            gained_yards = self._pass()
        if play_call == 'r':
            gained_yards = self._run()

        self.ls += gained_yards

        if self.ls >= 100:
            self.touchdown()
        else:
            if self.ls > self.first_marker:
                self.down = 0
                self.first_marker = self.ls + 10
                if play_call == 'r':
                    print("First Down!!! What a run!")

                else:
                    print("First Down!!! What a catch!")

            self.down += 1
            if self.down < 4:
                self.call_play()
            else:
                if self.ls > 65:
                    self.field_goal()
                else:
                    self.punt()
                    if self.posession == self.home:
                        self.posession = self.away
                    else:
                        self.posession = self.home

    def _run(self):
        """
        Returns the result of a run play. Using a normal distribution for the run result.
        """
        print('{} call a run play'.format(self.posession))
        gained_yards = int(np.random.normal(3.5,3))
        print(f"A run for {gained_yards} yards.")
        return gained_yards

    def _pass(self):
        print('{} call a pass play'.format(self.posession))
        #the average completion percentage is around 65%. So we will use that as the decision line for completion.
        comp_determinant = np.random.random()
        if comp_determinant <= .65: #pass completed
            pass_complete = True
            gained_yards = int(np.random.beta(1.8,10) * (100 - self.ls + 10))
            if self.ls + gained_yards > 100:
                gained_yards = 100 - self.ls
        else: #pass incomplete
            pass_complete = False
            gained_yards = 0
        if pass_complete:
            print(f"A pass and catch for {gained_yards} yards.")
        else:
            print(f"Incomplete pass")
        return gained_yards

    def coin_toss(self):
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
        kickoff_dist = np.random.normal(62.5, 3)
        start = int(100 - 35 - kickoff_dist)

        #using a beta distribution with alpha as 2 and beta as 5 for the return yards
        return_yards = int(np.random.beta(2,5) * 100)

        #making some adjustments for really long returns as they are more likely to score.
        if return_yards > 60:
            return_yards = int(np.random.beta(5,1) * 100)
        self.ls = max(min(start + return_yards,100),0)

        if self.ls >= 100:
            self.touchdown()
        else:
            print("\n{0} kick off to the {2} yard line and the {1} have returned it for {3} yards. The {1} will start at the {4}.".format(kicking_off, returning, start, return_yards, self.ls))
            if return_yards > 40:
                print(random.choice(self.color_comment))
        self.first_marker = self.ls + 10
        self.posession = returning
        self.call_play()

    def punt(self):
        """
        Used when team punts to the other team. Using average of 45 and std of 5.
        """
        punt_yards = int(np.random.normal(45,5))
        #if the punt ends up in the endzone it is a touchback and team gets the ball at the 20 yard line.
        if self.ls + punt_yards >= 100:
            self.ls = 20
        #otherwise we will flip the field
        else:
            self.ls = 100 - self.ls - punt_yards


        punting_team, _ = self.posession_change()
        print(f"{punting_team} punt the ball for {punt_yards} yards.")
        self.call_play()

    def fumble(self):
        pass

    def sack(self):
        pass

    def interception(self):
        pass

    def touchdown(self):
        """Updates score for a touchdown and sets up kickoff.
        """
        print("TOUCHDOWN!!!")

        #updating score, no PAT for now
        self.update_score('touchdown')
        self.e('PAT') #point after
        self.score_board()

        #setting up kickoff
        kicking_off, returning_team = self.posession_change()
        self.kickoff(kicking_off, returning_team)

    def update_score(self, type):
        """
        Updates the score based on scoring type of field goal(FG), touchdown, or points after (PAT).
        input: string
        return: none
        """
        if self.posession == self.away:
            self.away_points += self.scoring_points[type]
        else:
            self.home_points += self.scoring_points[type]


    def field_goal(self):
        '''
        Adds three points to the team with the ball. It is a given for now.
        '''
        print(f"\nThe {self.posession} make the {100 - self.ls} yard field goal and score three points")
        self.update_score('FG')
        self.score_board()

        kicking_off, returning_team = self.posession_change()
        self.kickoff(kicking_off, returning_team)


    def score_board(self):
        covered = int(self.ls // 5)
        remaining = 20 - covered
        print(f"\n{self.posession}'s ball: {'>'*covered}{'|'*remaining}Endzone [Score {self.away}:{self.away_points} - {self.home}:{self.home_points}]")

    def posession_change(self):
        """
        Helps to update self.posession for posession change after punts, field goals, kickoffs, turnovers.
        """
        self.down = 1
        self.first_marker = self.ls + 10

        prev_posession = self.posession
        alternator = cycle((self.away,self.home))
        self.posession = next(alternator)
        if prev_posession == self.posession:
            self.posession = next(alternator)
        return prev_posession, self.posession

if __name__ == "__main__":
    game = Football('49ers', 'Raiders')
    game.coin_toss()
