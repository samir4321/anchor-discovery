# hack_anchor_discovery.py
"""
 group user flows by taking a hash of their respective
 set of tuples (endpoint, response status code)

 hack anchor discovery by finding anchor as
 endpoint and response key that is most constant within
 hash groups and varies the most across hash groups
"""
import json
import math

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

    # make flow hashes
    for token in sessions.keys():
        sessions[token]["flow_hash"] = endpoints_codes_repr(sessions[token]["endpoints_codes"])

    # compute conditional counts
    resp_d = resp_obj_cond_counts(sessions)  # count (w|hash)
    flow_hash_d = flow_hash_obj_cond_counts(sessions)  # count(hash|w)
    anchor = find_anchor(resp_d, flow_hash_d)
    print(f"Anchor endpoint and response key found: \n{anchor}")


def find_anchor(resp_d, flow_hash_d):
    """
    find w that is constant within a flow hash
    and varies across flow hashes
    """
    anchor_candidates = set()
    for h in resp_d.keys():
        v_ent_dict = {}
        for w, ct in resp_d[h].items():
            url, k, v = w
            if (url, k) not in v_ent_dict:
                v_ent_dict[(url, k)] = []
            v_ent_dict[(url, k)].append(ct)
        anchor_candidate = None
        anchor_ent = -1
        for vk, cts in v_ent_dict.items():
            sm = sum(cts)
            ent = - sum(ct * 1. / sm * math.log(ct * 1. / sm) for ct in cts)
            if anchor_candidate is None or ent < anchor_ent:
                anchor_candidate = vk
                anchor_ent = ent
        anchor_candidates.add(anchor_candidate)

    candidate_distinct_values = {}
    for w in flow_hash_d.keys():
        url, k, v = w
        if (url, k) in anchor_candidates:
            if (url, k) not in candidate_distinct_values:
                candidate_distinct_values[(url, k)] = 0
            candidate_distinct_values[(url, k)] += 1
    anchor = max(candidate_distinct_values.items(), key=lambda e: e[1])[0]
    return anchor


def resp_obj_cond_counts(sessions):
    # Count(w|hash)
    d = {}
    for token in sessions.keys():
        flow_hash = sessions[token]["flow_hash"]
        if flow_hash not in d.keys():
            d[flow_hash] = {}
        for url, resp in sessions[token]["endpoints_responses"]:
            for k, v in resp.items():
                if type(v) == dict:
                    v = hash(frozenset(v.items()))
                d[flow_hash][(url, k, v)] = d[flow_hash].get((url, k, v), 0) + 1
    return d


def flow_hash_obj_cond_counts(sessions):
    # Count(hash|w)
    d = {}
    for token in sessions.keys():
        flow_hash = sessions[token]["flow_hash"]
        for url, resp in sessions[token]["endpoints_responses"]:
            for k, v in resp.items():
                if type(v) == dict:
                    v = hash(frozenset(v.items()))
                if (url, k, v) not in d.keys():
                    d[(url, k, v)] = {}
                d[(url, k, v)][flow_hash] = d[(url, k, v)].get(flow_hash, 0) + 1
    return d


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
