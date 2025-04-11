# yet to be implemented as waiting for SEM 2 to do multiplayer game, not required yet.
class ScoreManager:
    def __init__(self):
        self.__score = 0

    def get_score(self):
        return self.__score

    def add_points(self, points):
        self.__score += points

    def deduct_points(self, points):
        self.__score = max(0, self.__score - points)

    def reset(self):
        self.__score = 0