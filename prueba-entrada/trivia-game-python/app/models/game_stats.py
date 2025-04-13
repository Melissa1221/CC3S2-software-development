from app.models.difficulty import DifficultyLevel

class GameStats:
    def __init__(self):
        self.total_rounds = 0
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.total_score = 0
        self.difficulty_stats = {
            DifficultyLevel.EASY: {'correct': 0, 'total': 0},
            DifficultyLevel.MEDIUM: {'correct': 0, 'total': 0},
            DifficultyLevel.HARD: {'correct': 0, 'total': 0}
        }

    def update_stats(self, question, is_correct):
        self.total_rounds += 1
        if is_correct:
            self.correct_answers += 1
            self.total_score += question.get_points()
            self.difficulty_stats[question.difficulty]['correct'] += 1
        else:
            self.incorrect_answers += 1
        self.difficulty_stats[question.difficulty]['total'] += 1

    def get_summary(self):
        return {
            'total_rounds': self.total_rounds,
            'correct_answers': self.correct_answers,
            'incorrect_answers': self.incorrect_answers,
            'total_score': self.total_score,
            'accuracy': (self.correct_answers / self.total_rounds * 100) if self.total_rounds > 0 else 0,
            'difficulty_stats': self.difficulty_stats
        } 