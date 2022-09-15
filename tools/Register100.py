import random
import threading
import time
import faker
import requests

f = faker.Faker(locale='zh_CN')


def BOOM(r):
    for _ in range(r):
        e = f.email()
        p = 'Feather@123456'
        n = f.last_name()+f.name()
        r = requests.post("http://localhost:14524/api/user/register", json={
            'name': n,
            'pw': p,
            'email': e,
        }, headers={"user-agent": f.user_agent()})
        # print("FAKE {}:{}:{} CODE:{},TIME:{}".format(
        #     n, e, p, r.status_code, r.elapsed))
        time.sleep(random.randint(1, 100)/100)


class Thread(threading.Thread):
    def __init__(self, func, *args, **kwargs):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.func(*self.args, **self.kwargs)


p = []
for i in range(10):
    p.append(Thread(BOOM, 10))
    p[i].start()
