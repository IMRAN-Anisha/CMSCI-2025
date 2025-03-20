class Player:
    def __init__(self, name):
        self.name = name
        self.position = (0, 0)  # Example start position
        self.score = 0
        self.performance = "neutral"
    
    def update_position(self, new_position):
        self.position = new_position
    
    def update_score(self, points):
        self.score += points
    
    def evaluate_performance(self):
        # Example: Update performance based on score or time
        if self.score > 100:
            self.performance = "quick"
        elif self.score < 50:
            self.performance = "struggling"
        else:
            self.performance = "neutral"