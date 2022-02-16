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
        check_thresh(i, l_conf, 0.8, conf)
        check_thresh(i, l_conf, 0.9, conf)
        check_thresh(i, l_conf, 0.95, conf)
        if check_thresh(i, l_conf, 0.99, conf):
            break
        l_conf = conf

    print(r, 'trials req for confidence at p =', p)

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
