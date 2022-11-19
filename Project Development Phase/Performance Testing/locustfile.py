from locust import *
import random
import time

data=({'uname':'shirls','password':'123'},{'uname':'shirlsrocks','password':'123'},{'uname':'csesan','password':'123'})
post_headers={'Content-Type':'application/x-www-form-urlencoded'}

class SmartFashion(HttpUser):

    @task
    def login_test(self):
        time.sleep(2)
        self.client.post("/login",
                         data=data[random.randint(0,2)],headers=post_headers)

    @task(20)
    def stattest(self):
        self.client.get("/")


