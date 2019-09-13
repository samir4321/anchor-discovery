# hack_anchor_discovery.py
"""

"""
import json


def hack_anchor_discovery():
    # group logs by session
    sessions = {}
    with open("clean.log", 'r') as fl:
        for ln in fl:
            s = ln.strip().replace("\'", "\"")
            d = json.loads(s)
            token = d["token"].strip()
            resp_code = d["resp_code"]
            resp = d["resp"]
            url = d["url"]
            if len(token) > 0:
                if token not in sessions:
                    sessions[token] = {
                        "endpoints_codes": set(),
                        "endpoints_responses": []
                    }
                sessions[token]["endpoints_codes"].add((url, resp_code))
                sessions[token]["endpoints_responses"].append((url, resp))
    print(sessions)

def resp_obj_cond_counts():
    # Count(w|hash)
    pass

def hash_obj_cond_counts():
    # Count(hash|w)
    pass


def endpoints_codes_repr(endpoints_codes):
    # hash of set of tuples of (endpoint, code)
    return hash(frozenset(endpoints_codes))


def clean():
    with open("server.log", "r") as fl:
        with open("clean.log", 'w') as fl2:
            for ln in fl:
                lnstr = ln.strip()
                if "DEBUG" in lnstr:
                    fl2.write(lnstr.split("DEBUG:app:")[1].strip().replace("\'", "\"") + "\n")


if __name__ == "__main__":
    clean()
    hack_anchor_discovery()
