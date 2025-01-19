def check_missing_index(t):
    if t == "No collection":
        return 1
    else:
        t = sorted(t, key=int)
        last_id = int(t[-1])
        if last_id > len(t):
            while str(last_id - 1) in t:
                last_id -= 1
            return last_id - 1
        else:
            return last_id + 1