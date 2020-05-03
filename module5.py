import json
import os.path
import random
import requests

BASE_URL = "http://localhost:3030/widgets"
HTTP_HEADERS = {'Content-Type': 'application/json'}
AUTH_TOKEN = "YOUR_AUTH_TOKEN"  #security related item

# Get number of defects per subsystem

defects_a = random.randint(0, 10)
defects_b = random.randint(0, 25)

# Set limits for warning (yellow) and danger (red) per subsystem

if defects_a != 0:
    status_a = "warning" if defects_a <= 5 else "danger"
else:
    status_a = "default"

if defects_b != 0:
    status_b = "warning" if defects_b <= 15 else "danger"
else:
    status_b = "default"

# Get data for Function test and System test

ft_total = 450
st_total = 115

ft_exec = random.randint(300, ft_total)
st_exec = random.randint(50, st_total)

ft_exec_perc = int(round(100 * ft_exec / ft_total, 0))
st_exec_perc = int(round(100 * st_exec / st_total, 0))

ft_not_exec = ft_total - ft_exec
st_not_exec = st_total - st_exec

ft_pass = random.randint(10, ft_exec)
st_pass = random.randint(5, st_exec)

ft_fail = ft_exec - ft_pass
st_fail = st_exec - st_pass


# Send data to the widgets (HTTP post requests)

url = os.path.join(BASE_URL, "project_subsystem_a")
requests.post(url, headers=HTTP_HEADERS, data=json.dumps(
    {
    "auth_token": AUTH_TOKEN,  #security!
    "current": defects_a,
    "status": status_a
    }))

url = os.path.join(BASE_URL, "project_subsystem_b")
requests.post(url, headers=HTTP_HEADERS, data=json.dumps(
    {
    "auth_token": AUTH_TOKEN,
    "current": defects_b,
    "status": status_b
    }))

url = os.path.join(BASE_URL, "project_progress_ft")
requests.post(url, headers=HTTP_HEADERS, data=json.dumps(
    {
    "auth_token": AUTH_TOKEN,
    "value": ft_exec_perc,
    "moreinfo": "{} of {} test cases are executed".format(ft_exec, ft_total)
    }))

url = os.path.join(BASE_URL, "project_progress_st")
requests.post(url, headers=HTTP_HEADERS, data=json.dumps(
    {
    "auth_token": AUTH_TOKEN,
    "value": st_exec_perc,
    "moreinfo": "{} of {} test cases are executed".format(st_exec, st_total)
    }))

url = os.path.join(BASE_URL, "project_results_ft")
requests.post(url, headers=HTTP_HEADERS, data=json.dumps(
    {
    "auth_token": AUTH_TOKEN,
    "items": [{"label": "Pass","value": ft_pass},
              {"label": "Fail", "value": ft_fail},
              {"label": "Not executed", "value": ft_not_exec}],
    "moreinfo": "Total number of test cases: {}".format(ft_total)
    }))

url = os.path.join(BASE_URL, "project_results_st")
requests.post(url, headers=HTTP_HEADERS, data=json.dumps(
    {
    "auth_token": AUTH_TOKEN,
    "items": [{"label": "Pass","value": st_pass},
              {"label": "Fail", "value": st_fail},
              {"label": "Not executed", "value": st_not_exec}],
    "moreinfo": "Total number of test cases: {}".format(st_total)
    }))
