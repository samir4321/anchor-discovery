# hack_anchor_discovery.py
"""

"""
import json

def hack_anchor_discovery():
    # group by token
    sessions = {}
    with open("clean.log", 'r') as fl:
        for ln in fl:
            s = ln.strip().replace("\'", "\"")
            d = json.loads(s)
            token = d["token"]
            if len(token.strip()) > 0:
                if token.strip() not in sessions:
                    sessions[token.strip()] = {}
                    # ...

def clean():
    with open("server.log", "r") as fl:
        with open("clean.log", 'w') as fl2:
            for ln in fl:
                lnstr = ln.strip()
                if "DEBUG" in lnstr:
                    fl2.write(lnstr.split("DEBUG:app:")[1].strip().replace("\'", "\"") + "\n")


if __name__ == "__main__":
    hack_anchor_discovery()