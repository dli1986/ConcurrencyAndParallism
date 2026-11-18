from locust import HttpUser, task, between

class ApiUser(HttpUser):
    @task
    def hit_task(self):
        self.client.get("/api/task")

# usage: locust -f locustfile.py --host http://localhost:8080
# because nginx run on port 8080