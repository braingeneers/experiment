import json


with open('b6528531-6291-4033-b7f1-b51a65cac1c3.json') as f:
    data = json.load(f)
    experiment = data["experiment"]

print(experiment["email"])


for k in experiment["payload"]:
    print(k["value"], k["hold"])

print(experiment)

if (experiment["type"] == "simulated"):
    print("True!!")
