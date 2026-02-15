class LiveScoreAggregator:

    def __init__(self):
        self.scores = []

    def add(self, score):
        self.scores.append(score)

    def average(self):
        if not self.scores:
            return 0
        return sum(self.scores) / len(self.scores)
