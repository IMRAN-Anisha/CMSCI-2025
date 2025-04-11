# yet to be implemented as waiting for SEM 2 to do multiplayer game, not required yet.
class ScoreManager:
    def __init__(self):
        self.score = 0

    def add_points(self, points):
        self.score += points

    def deduct_points(self, points):
        self.score = max(0, self.score - points)

    def get_score(self):
        return self.score

    def reset(self):
        self.score = 0