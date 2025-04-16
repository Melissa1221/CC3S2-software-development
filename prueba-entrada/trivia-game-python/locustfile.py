from locust import HttpUser, task, between
import json

class TriviaApiUser(HttpUser):
    wait_time = between(1, 5)
    
    def on_start(self):
        self.client.post("/quiz/reset")
        
    @task(3)
    def get_random_questions(self):
        self.client.get("/questions/random?count=5")
        
    @task(1)
    def get_filtered_questions(self):
        difficulties = ["easy", "medium", "hard"]
        for difficulty in difficulties:
            self.client.get(f"/questions/random?count=3&difficulty={difficulty}")
    
    @task(2)
    def answer_question(self):
        response = self.client.get("/questions/random?count=1")
        if response.status_code == 200:
            questions = response.json()
            if questions and len(questions) > 0:
                question = questions[0]
                
                if question["options"] and len(question["options"]) > 0:
                    import random
                    option_index = random.randint(0, len(question["options"]) - 1)
                    selected_option = question["options"][option_index]
                    
                    self.client.post(
                        "/questions/answer",
                        json={
                            "question_id": question["id"],
                            "answer": selected_option
                        }
                    )

    @task(1)
    def get_quiz_summary(self):
        self.client.get("/quiz/summary")
        
    @task(1)
    def reset_quiz(self):
        self.client.post("/quiz/reset") 