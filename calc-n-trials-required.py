from scipy import stats


def thresh_within(old, thresh, new):
    return old <= thresh <= new


def get_n_trials_req(p):
    conf = 0
    l_conf = 0
    r = []

    def check_thresh(i, old, p, new):
        if thresh_within(old, p, new):
            r.append((p, i))
            return True

    for i in range(100000):
        conf = stats.binom.sf(0, i, p)
        # check_thresh(i, l_conf, 0.4, conf)
        # check_thresh(i, l_conf, 0.48, conf)
        # check_thresh(i, l_conf, 0.49, conf)
        # check_thresh(i, l_conf, 0.5, conf)
        check_thresh(i, l_conf, 0.8, conf)
        check_thresh(i, l_conf, 0.9, conf)
        check_thresh(i, l_conf, 0.95, conf)
        if check_thresh(i, l_conf, 0.99, conf):
            break
        l_conf = conf

    print(r, 'trials req for confidence at p =', p)
    print(f"""
| Confidence | Tests Required for 1 Success (p={p:.3f}) |
|---|---|
| {r[0][0]:.0%} | {r[0][1]} |
| {r[1][0]:.0%} | {r[1][1]} |
| {r[2][0]:.0%} | {r[2][1]} |
| {r[3][0]:.0%} | {r[3][1]} |
""")

get_n_trials_req(0.283)
get_n_trials_req(0.104)
get_n_trials_req(0.0005)

# cpp
get_n_trials_req(0.176)
# sup
get_n_trials_req(0.071)
# cpp2013
get_n_trials_req(0.435)
# sam
get_n_trials_req(0.410)

# farce threshhold at 100 filtered members
get_n_trials_req(0.492)

# farce at 150 filtered members
get_n_trials_req(0.151)

# exactly 0.5 confidence
get_n_trials_req(0.5)
get_n_trials_req(0.89)

# australian democrats
get_n_trials_req(0.237)
