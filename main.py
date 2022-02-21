#!/usr/bin/env python3

from enum import Enum
import multiprocessing as mp
from dataclasses import dataclass
from itertools import dropwhile, repeat, takewhile
from multiprocessing import pool
import os
import sys
from time import perf_counter
from typing import Any, Optional, Union
from matplotlib.cbook import flatten
# import numpy as np
import pandas as pd
# import scipy as sp
# import scipy.stats as stats
import random as r
import matplotlib.pyplot as plt
import click


SIM_CHUNKS = max(1, mp.cpu_count() - 1)


class Timer():
    def __init__(self, timer_name=None, auto_print=False):
        self.started_at = None
        self.ended_at = None
        self.timer_name = timer_name
        self.auto_print = auto_print

    def __enter__(self):
        self.started_at = perf_counter()

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.ended_at = perf_counter()
        if self.auto_print:
            self.print_duration()

    @property
    def duration(self) -> Optional[float]:
        if self.started_at and self.ended_at:
            return self.ended_at - self.started_at
        return None

    def print_duration(self):
        name = "" if not self.timer_name else f"[{self.timer_name}] "
        print(f"{name}Duration: {self.duration}")


def calc_failing_members_n(total_members, failure_rate):
    return round(total_members * failure_rate)


def mk_members(total_members, failure_rate):
    # member: (id: int, response_to_aec: bool)
    n_non_members = calc_failing_members_n(total_members, failure_rate)
    n_members = total_members - n_non_members
    for i in range(n_non_members):
        yield (i, False)
    for i in range(n_members):
        yield (n_non_members + i, True)


def filter_out_n_members(f, members, n_to_filter):
    n_filtered = 0
    for m in members:
        if f(m) and n_filtered < n_to_filter:
            n_filtered += 1
            continue
        yield m


assert list(filter_out_n_members(lambda x: x%2 == 0, range(5), 0)) == [0,1,2,3,4]
assert list(filter_out_n_members(lambda x: x%2 == 0, range(5), 1)) == [1,2,3,4]
assert list(filter_out_n_members(lambda x: x%2 == 0, range(5), 2)) == [1,3,4]
assert list(filter_out_n_members(lambda x: x%2 == 0, range(5), 3)) == [1,3]
assert list(filter_out_n_members(lambda x: x%2 == 0, range(5), 4)) == [1,3]


AEC_TABLE_2021 = [
    (1500, 18, 0),
    (1506, 27, 1),
    (1523, 33, 2),
    (1543, 38, 3),
    (1562, 42, 4),
    (1582, 46, 5),
    (1599, 50, 6),
    (1616, 53, 7),
    (1633, 57, 8),
    (1647, 60, 9),
    (1651, 60, 9),  # we will subtract 1 later to calc an inclusive range
]

### ~~anomaly: https://www.aec.gov.au/Parties_and_Representatives/Party_Registration/Registration_Decisions/2017/sor-the-communists.pdf~~
### ~~-- 34 responses required, why would this table ever change? FOI~~
# https://web.archive.org/web/20200320074933/https://www.aec.gov.au/Parties_and_Representatives/Party_Registration/files/party-registration-guide.pdf
# https://web.archive.org/web/20210409193623/https://aec.gov.au/Parties_and_Representatives/Party_Registration/guide/files/party-registration-guide.pdf
# 2017 - 2020
AEC_TABLE_2017 = [
    (500, 18, 0),
    (503, 26, 1),
    (511, 32, 2),  # this was 26 responses in 2017 -- sor-australian-affordable-housing-party.pdf
    (519, 37, 3),
    (526, 41, 4),
    (534, 44, 5),  # 535 used to be 37, ?4?
    (541, 47, 6),
    (548, 50, 7),
    (551, 50, 7),  # we subtract 1 later for upper bound
]

# https://web.archive.org/web/20170521182536/http://www.aec.gov.au/Parties_and_Representatives/Party_Registration/files/party-registration-guide.pdf
# same as 2020
# AEC_TABLE_2017 = [
#     (500, 18, 0),
#     (503, 26, 1),
#     (512, 30, 2),
#     (521, 34, 3),
#     (529, 38, 3),
#     (537, 42, 5),
#     (543, 46, 6),
#     (548, 50, 7),
#     (551, 50, 7),  # we subtract 1 later for upper bound
# ]

# https://web.archive.org/web/20160314113418/http://aec.gov.au/Parties_and_Representatives/Party_Registration/files/party-registration-guide.pdf
# same as 2014
# AEC_TABLE_2016 = [
#     (500, 18, 0),
#     (503, 26, 1),
#     (512, 30, 2),
#     (521, 34, 3),
#     (529, 38, 3),
#     (537, 42, 5),
#     (543, 46, 6),
#     (548, 50, 7),
#     (551, 50, 7),  # we subtract 1 later for upper bound
# ]

AEC_TABLE_2012 = [
    (500, 18, 0),
    (503, 26, 1),
    (512, 30, 2),
    (521, 34, 3),
    (529, 38, 3),
    (537, 42, 5),
    (543, 46, 6),
    (548, 50, 7),
    (551, 50, 7),  # we subtract 1 later for upper bound
]

AEC_TABLE_2012_CORRECTED = [
    (500, 18, 0),
    (503, 26, 1),
    (512, 30, 2),
    (521, 34, 3),
    (529, 38, 4),  # max denials fixed
    (537, 42, 5),
    (543, 46, 6),
    (548, 50, 7),
    (551, 50, 7),  # we subtract 1 later for upper bound
]

AEC_TABLE_2011 = [
    (500, 18, 0),
    (505, 21, 1),
    (515, 26, 2),
    (520, 29, 2),
    (525, 32, 3),
    (530, 35, 4),
    (535, 37, 4),
    (540, 40, 5),
    (545, 43, 5),
    (551, 47, 6),  # we subtract 1 later for upper bound
]

def testing_table_to_ranges(testing_table):
    return list((lower, upper - 1, n, x) for ((lower, n, x), (upper, _, _)) in zip(testing_table, testing_table[1:]))

# AEC_RANGE_2021 = list((lower, upper - 1, n, x) for ((lower, n, x), (upper, _, _)) in zip(AEC_TABLE_2021, AEC_TABLE_2021[1:]))
# AEC_RANGE_2017 = list((lower, upper - 1, n, x) for ((lower, n, x), (upper, _, _)) in zip(AEC_TABLE_2017, AEC_TABLE_2017[1:]))
# AEC_TABLE_2011 = list((lower, upper - 1, n, x) for ((lower, n, x), (upper, _, _)) in zip(AEC_TABLE_2011, AEC_TABLE_2011[1:]))
AEC_RANGE_2021 = testing_table_to_ranges(AEC_TABLE_2021)
AEC_RANGE_2017 = testing_table_to_ranges(AEC_TABLE_2017)
AEC_RANGE_2012 = testing_table_to_ranges(AEC_TABLE_2012)
AEC_RANGE_2012_CORRECTED = testing_table_to_ranges(AEC_TABLE_2012_CORRECTED)
AEC_RANGE_2011 = testing_table_to_ranges(AEC_TABLE_2011)


class TestingStandard(Enum):
    SEPT2021 = 1
    C2017 = 2
    C2012 = 3
    C2011 = 4
    C2012Corrected = 5


TESTING_RANGE_LOOKUP = {
    TestingStandard.SEPT2021: AEC_RANGE_2021,
    TestingStandard.C2017: AEC_RANGE_2017,
    TestingStandard.C2012: AEC_RANGE_2012,
    TestingStandard.C2011: AEC_RANGE_2011,
    TestingStandard.C2012Corrected: AEC_RANGE_2012_CORRECTED,
}


TESTING_N_REQUIRED_LOOKUP = {
    TestingStandard.SEPT2021: 1500,
    TestingStandard.C2017: 500,
    TestingStandard.C2012: 500,
    TestingStandard.C2011: 500,
    TestingStandard.C2012Corrected: 500,
}


def test_std_to_n_members_required(test_std: TestingStandard):
    return TESTING_N_REQUIRED_LOOKUP[test_std]


def lookup_aec_testing_parameters(sample_size, testing_std: TestingStandard):
    '''
    Source: Page 24 of https://www.aec.gov.au/Parties_and_Representatives/Party_Registration/guide/files/party-registration-guide.pdf
    Members lodged, Random sample size, Maximum denials to pass
    1,500 18 0
    1,506 27 1
    1,523 33 2
    1,543 38 3
    1,562 42 4
    1,582 46 5
    1,599 50 6
    1,616 53 7
    1,633 57 8
    1,647 60 9
    1,650 60 9
    https://web.archive.org/web/20210409193623/https://aec.gov.au/Parties_and_Representatives/Party_Registration/guide/files/party-registration-guide.pdf
    Members lodged Random Sample Max Denials to Pass
    500 18 0
    503 26 1
    511 32 2
    519 37 3
    526 41 4
    534 44 5
    541 47 6
    548 50 7
    550 50 7
    https://web.archive.org/web/20110220143705/http://www.aec.gov.au/Parties_and_Representatives/Party_Registration/Registration_Decisions/registration-tests.htm
    > The table below is an extract from a table based on a formula provided by the Australian Bureau of Statistics, giving approximately a 10% risk of refusing a party which has 500 members and a 2% risk of registering a party with only 400 members.
    Eligible membership 	Size of random sample 	Denials permitted 	Confirmations required
    500 	18 	0 	18
    505 	21 	1 	20
    515 	26 	2 	24
    520 	29 	2 	27
    525 	32 	3 	29
    530 	35 	4 	31
    535 	37 	4 	33
    540 	40 	5 	35
    545 	43 	5 	38
    550 	47 	6 	41
    '''

    members_required = test_std_to_n_members_required(testing_std)
    testing_ranges = TESTING_RANGE_LOOKUP[testing_std]
    l, u = 0, 0
    for (l, u, n, x) in testing_ranges:
        if l <= sample_size <= u:
            return (n, x)
    raise Exception(f"Invalid sample size: {sample_size} -- should be between {members_required} and {members_required * 11 // 10} inclusive (last l={l}, last u={u})")


assert lookup_aec_testing_parameters(1_626, TestingStandard.SEPT2021) == (53, 7)


def if_else(c: Union[bool, Optional[Any]], a, b):
    return a if c else b


@dataclass
class GraphDetails:
    title: str


@dataclass
class RunSpec:
    total_members: int  # 4_680
    failure_rate: float  # 0.17
    _sample_size: int  # 1_649
    n_members_removed: int  # 24
    testing_std: TestingStandard = TestingStandard.SEPT2021
    filter_any: bool = False

    def as_tuple(self):
        return self.total_members, self.failure_rate, self.sample_size, self.n_members_removed, self.filter_any

    def title_line(self, party_name: Optional[str] = None):
        is_valid = self.n_real_members >= self.min_list_limit
        return f"AEC membership test results PMF\nParty {if_else(is_valid, 'IS', 'IS NOT')} eligible" + if_else(party_name, f" | Based on: {party_name}", "")

    @property
    def min_list_limit(self):
        return test_std_to_n_members_required(self.testing_std)

    @property
    def max_list_limit(self):
        return self.min_list_limit * 11 // 10

    @property
    def sample_size(self):
        assert self._sample_size <= self.total_members
        return min(self.max_list_limit, self._sample_size)

    @property
    def filtered_sample_size(self):
        return self.sample_size - self.n_members_removed

    @property
    def n_failing_members(self):
        return calc_failing_members_n(self.total_members, self.failure_rate)

    @property
    def n_real_members(self):
        return self.total_members - self.n_failing_members

    @property
    def n_sample_real_m(self):
        if self.filter_any:
            return round(self.filtered_sample_size * self.n_real_members / self.total_members)
        # filtered members are always removed from real members because they must be assumed to be replaceable (by the party) w/ real members
        return round(self.sample_size * self.n_real_members / self.total_members) - self.n_members_removed

    @property
    def n_sample_failing_m(self):
        ss = self.filtered_sample_size if self.filter_any else self.sample_size
        return round(ss * self.n_failing_members / self.total_members)

    def subtitle_line(self):
        assert self.sample_size - self.n_members_removed == self.n_sample_real_m + self.n_sample_failing_m
        return " | ".join([
            f"N Members = {self.total_members} (Y: {self.n_real_members}, N: {self.n_failing_members})",
            f"Submitted = {self.sample_size}",
            f"Filtered Out{' Any' if self.filter_any else ''} = {self.n_members_removed}",
            # f"Remaining = {self.sample_size - self.n_members_removed}",
            f"Sample: {self.sample_size - self.n_members_removed} (Y: {self.n_sample_real_m}, N: {self.n_sample_failing_m})",
            f"P(denial) = {self.failure_rate:.3f}",
        ])

    def out_fname(self, n_trials, party_name: Optional[str], is_farce: bool):
        failing_members = calc_failing_members_n(self.total_members, self.failure_rate)
        fname_suffix = f"{name_to_fname_sfx(party_name)}" if party_name else None
        fname_parts: list[str] = list(map(str, filter(lambda x: x is not None, [
            "aec-test-sim",
            "FARCE" if is_farce else None,
            f"N{n_trials}-m{self.total_members}-f{failing_members}-s{self.sample_size}-r{self.n_members_removed}",
            "fANY" if self.filter_any else None,
            fname_suffix,
        ])))
        return "-".join(fname_parts)


default_run_spec = RunSpec(total_members=4_680, failure_rate=0.17, _sample_size=1_649, n_members_removed=24)
flux_run_spec = default_run_spec


def name_to_fname_sfx(n: str):
    return n.lower().strip().replace(' ', '-').replace('(', '').replace(')', '').replace('@', '_').replace('%', '-pct-')


def run_trials(n_trials, total_members, failure_rate, sample_size, n_members_removed, reduced_sample_size, n_to_sample, filter_any):
    # generate a list of members with some given non-member rate (i.e. these members will always fail)
    members = list(mk_members(total_members, failure_rate))

    results = []
    for _ in range(n_trials):
        # take sample from full membership list (which can be more that 1650 / the AEC's limit)
        # the sample size is, at most, the legislative limit (e.g., 1650)
        membership_sample = r.sample(members, sample_size)

        # remove n_members_removed true members (this is the worst case for the party).
        #   members can be removed b/c their details couldn't be matched, they're deceased, or b/c they've supported another party's rego.
        #   we always want to remove true members to measure worst case performance of methodology.
        # why? because that's what happens in a griefing attack (your fake-members will be sure not to give you bad details).\
        # since there is no way to detect this and it is not random or uniformly distributed, it must be assumed.
        if not filter_any:
            reduced_sample = list(filter_out_n_members(lambda m: m[1], membership_sample, n_members_removed))
        else:
            # the following line will remove n_members_removed indiscriminantly
            # note: it makes little difference -- only in borderline cases.
            reduced_sample = list(membership_sample[n_members_removed:])
        assert reduced_sample_size == len(reduced_sample)

        # perform check (contact member to confirm)
        actual_sample = r.sample(reduced_sample, n_to_sample)
        # count failures
        n_failures = sum(0 if m[1] else 1 for m in actual_sample)

        # if trial_ix % status_after_trials == 0:
        #     pct_done = trial_ix / n_trials
        #     print(f"[{pct_done:6.2%}] Completed trial {trial_ix} of {n_trials}")

        # return n_failures
        results.append(n_failures)
    return results


def run(trial_pool: pool.Pool, n_trials: int, run_spec: RunSpec, graph_title=None, graph_fname=None, show=True, party_name=None, force=False, farce_extra=None):
    output_files_exist = any(all(os.path.exists(f'./{ext}/{run_spec.out_fname(n_trials, party_name, is_farce)}.{ext}') for ext in ['png', 'csv']) for is_farce in [True, False])
    use_cached_results = False

    if not force and output_files_exist:
        print(f"Output files exist (use --force to overwrite) -- skipping simulation: {run_spec}")
        use_cached_results = True
        return

    print(f"\n# Running {n_trials} rounds for {run_spec} #")
    total_members, failure_rate, sample_size, n_members_removed, filter_any = run_spec.as_tuple()
    reduced_sample_size = sample_size - n_members_removed
    n_to_sample, max_failures = lookup_aec_testing_parameters(reduced_sample_size, run_spec.testing_std)
    status_after_trials = n_trials // 10

    n_real_members = run_spec.n_real_members
    assert run_spec.n_sample_real_m + run_spec.n_sample_failing_m <= sample_size
    pass_expected = run_spec.n_sample_real_m >= run_spec.min_list_limit

    # init results list of zeros -- failure count is index in list
    failure_counts = [0] * (n_to_sample + 1)

    # if not use_cached_results:
    print(f"Running trials --- n_jobs = {SIM_CHUNKS}.")
    with Timer(f"Simulation(N={n_trials})", auto_print=True):
        trial_chunk_params = (n_trials // SIM_CHUNKS), total_members, failure_rate, sample_size, n_members_removed, reduced_sample_size, n_to_sample, filter_any
        results = flatten(trial_pool.starmap(run_trials, repeat(trial_chunk_params, SIM_CHUNKS)))
        for n_failures in results:
            failure_counts[n_failures] += 1

    ys_w_tail = list(c / n_trials for c in failure_counts)
    raw_ys = list(list(dropwhile(lambda y: y == 0, ys_w_tail[::-1]))[::-1]) + [0]
    max_p = max(raw_ys)
    n_cols = len(raw_ys)
    xs = list(range(n_cols))
    ys_passed = list(raw_ys[i] if i <= max_failures else 0 for i in xs)
    ys_failed = list(raw_ys[i] if i > max_failures else 0 for i in xs)
    _cum_passed = sum(ys_passed)
    cum_passed = (1 - sum(ys_failed) + _cum_passed) / 2  # average to avoid small floating point errors
    cum_failed = 1 - cum_passed  # by definition -- ensures they add to 1
    pass_l = f'$P(pass)$ = {cum_passed:.3f}'
    fail_l = f'$P(fail)$ = {cum_failed:.3f}'
    df = pd.DataFrame(data={pass_l: ys_passed, fail_l: ys_failed}, index=xs)

    # draw data
    df.plot.bar(stacked=True, figsize=(8, 5))
    plt.xlabel('AEC Contact -- Membership Denials')
    plt.ylabel("$P(x = X)$")

    # set a title if one was passed
    plt.suptitle(graph_title or run_spec.title_line(party_name))
    party_valid = n_real_members >= run_spec.min_list_limit
    aec_false_neg = cum_failed if party_valid else 0
    aec_false_pos = 0 if party_valid else cum_passed
    aec_failure_rate = cum_failed if pass_expected else cum_passed
    aec_nonreality_rate = cum_failed if party_valid else cum_passed
    # this is generous, but it's definitely a farce in these cases
    is_farce = aec_false_neg >= 0.5
    is_bad_conf = aec_false_neg >= 0.1
    title = \
        run_spec.subtitle_line() \
        + "\n" + " | ".join([
            f"Simulations = {n_trials}",
            f"Party {if_else(party_valid, 'IS', 'IS NOT')} valid (if filtered members are valid)",
            f"Exhaustive test, $N \\leq {run_spec.max_list_limit}$, would: {if_else(pass_expected, 'Pass', 'Fail')}",
            # f"P(AEC false neg) = {aec_false_neg:.1%}",
            # f"P(AEC false pos) = {aec_false_pos:.1%}",
        ]) \
        + "\n" + " | ".join([
            f"P(Conflict: AEC Method $\\longleftrightarrow$ Exhaustive) = {aec_failure_rate:.1%}",
            f"P(Conflict: AEC Method $\\longleftrightarrow$ Reality) = {aec_nonreality_rate:.1%}",
         ]) \
        # + "\n"
    plt.title(title, fontdict=dict(fontsize=8), linespacing=1.4)
    plt.subplots_adjust(top=0.80)
    plt.legend()

    loc = (n_cols - 2, max_p / 2)
    bbox = {'facecolor': 'none', 'edgecolor': 'red', 'lw': 3}
    def notice_box(farce_or):
        return "\n".join(if_else(farce_extra, [farce_extra], []) + [farce_or] + if_else(farce_extra, extra_end, []))
    if is_farce: # or is_bad_conf:
        farce_txt = None
        if is_farce:
            extra_end = [f"if $N \\gtrsim {total_members}$"] if "CONFIRMED" not in (farce_extra or "") else []
            farce_txt = notice_box("FARCE")
        # elif is_bad_conf:
        #     farce_txt = notice_box("")
        assert farce_txt is not None
        plt.text(loc[0], loc[1], farce_txt, ha='right', va='center', color='red', fontweight='black', fontsize=20, bbox=bbox)

    fname = run_spec.out_fname(n_trials, party_name, is_farce)
    print(f"Writing files out under ./png/{fname}.png (also csv/*.csv)")
    plt.savefig(f"png/{fname}.png", dpi=200)
    df.to_csv(f"csv/{fname}.csv")
    if show:
        plt.show()
    plt.close()
    print("Done\n")


@click.command()
@click.option('-T', '--n-trials', default=10_000, type=int, help='The number of simulations to run when building distribution')
@click.option('-S', '--show', is_flag=True, help='Show the plot when done')
@click.option('-j', '--jobs', type=int, required=False, help='The number of parallel jobs to run (default: N_CPUS - 1)')
@click.option('-F', '--force', is_flag=True, help='Run the simulation even if the output files already exist')
@click.option('-N', '--non-essential', is_flag=True, help='Also generate non-essential graphs')
@click.option('--only-flux', is_flag=True, help='Only generate essential Flux graphs')
def aec(n_trials, show, jobs, force, non_essential, only_flux):
    frs = flux_run_spec
    trial_pool = mp.Pool(jobs or SIM_CHUNKS)
    def _run(*args, **kwargs):
        _kwargs = dict(show=show, force=force)
        _kwargs.update(kwargs)
        run(trial_pool, n_trials, *args, **_kwargs)
    _run(default_run_spec, party_name="Flux", farce_extra="CONFIRMED\nREAL-WORLD")
    _run(RunSpec(frs.total_members, frs.failure_rate, frs._sample_size, frs.n_members_removed, filter_any=True), party_name="Flux", farce_extra="CONFIRMED\nREAL-WORLD")
    _run(RunSpec(frs.total_members, frs.failure_rate, 1650, 0), party_name="Flux+NoFilter")
    _run(RunSpec(frs.total_members, frs.failure_rate, 1650, 0, filter_any=True), party_name="Flux+NoFilter")
    _run(RunSpec(round(frs.total_members * 1.2), (796 + frs.total_members * 0.1) / frs.total_members / 1.2, 1650, 0), party_name="Flux+Gain20%Lose10%")
    _run(RunSpec(round(frs.total_members * 1.2), (796 + frs.total_members * 0.1) / frs.total_members / 1.2, 1650, 24), party_name="Flux+Gain20%Lose10%")
    _run(RunSpec(frs.total_members, 0.5, 1650, 0), party_name="Flux+HalfBadMembers")
    _run(RunSpec(frs.total_members, 150/1650, frs.sample_size, frs.n_members_removed), party_name="Flux@Thresh")
    _run(RunSpec(frs.total_members, 150/1650, frs.sample_size, frs.n_members_removed, filter_any=True), party_name="Flux@Thresh")
    _run(RunSpec(frs.total_members, 150/1650, frs.sample_size, 49), party_name="Flux@Thresh+F50")
    _run(RunSpec(frs.total_members, 150/1650, frs.sample_size, 49, filter_any=True), party_name="Flux@Thresh+F50")
    _run(RunSpec(frs.total_members, 150/1650, frs.sample_size, 99), party_name="Flux@Thresh+F99")
    _run(RunSpec(frs.total_members, 150/1650, frs.sample_size, 99, filter_any=True), party_name="Flux@Thresh+F99")
    _run(RunSpec(frs.total_members, 150/1650, frs.sample_size, 149), party_name="Flux@Thresh+F149")
    _run(RunSpec(frs.total_members, 150/1650, frs.sample_size, 149, filter_any=True), party_name="Flux@Thresh+F149")

    _run(RunSpec(round(frs.total_members * 2), (796 + frs.total_members * 0.333) / frs.total_members / 2, 1650, 0), party_name="Flux+Gain100%Lose33%")
    _run(RunSpec(round(frs.total_members * 2), (796 + frs.total_members * 0.333) / frs.total_members / 2, 1650, 24), party_name="Flux+Gain100%Lose33%")

    _run(RunSpec(20000, 0.5, 1650, 0))

    if not only_flux:
        # https://aec.gov.au/Parties_and_Representatives/Party_Registration/Deregistered_parties/files/statement-of-reasons-australian-peoples-party-s137-deregistration.pdf
        # Note: no way they were valid with 25 denials to 12 confirmations
        # _run(RunSpec(541*3, 36/536, 536*3, 5*3), party_name="APP@Threshold (Scaled)")
        # _run(RunSpec(541*3, 25/37, 536*3, 5*3), party_name="APP@Measured (Scaled)")

        # https://aec.gov.au/Parties_and_Representatives/Party_Registration/Deregistered_parties/files/statement-of-reasons-australian-better-families.pdf
        # _run(RunSpec(505*3, 1/26, 505*3, 0), party_name="ABF@AEC Threshold (Scaled)")
        # _run(RunSpec(505*3, 2/26, 505*3, 0), party_name="ABF@Measured (Scaled)")
        # _run(RunSpec(505*3, 5/505, 505*3, 0), party_name="ABF@Threshold (Scaled)")

        # https://aec.gov.au/Parties_and_Representatives/Party_Registration/Deregistered_parties/files/statement-of-reasons-the-small-business-party-s137-deregistration.pdf
        # _run(RunSpec(511*3, 2/32, 511*3, 0), party_name="SBP@AEC Threshold (Scaled)")
        # _run(RunSpec(511*3, 3/32, 511*3, 0), party_name="SBP@Measured (Scaled)")
        # _run(RunSpec(511*3, 11/511, 511*3, 0), party_name="SBP@Threshold (Scaled)")

        # https://aec.gov.au/Parties_and_Representatives/Party_Registration/Deregistered_parties/files/statement-of-reasons-child-protection-party-s137-deregistration.pdf
        # add bonus b/c they were at limit of 550
        # 2021
        _run(RunSpec(550 * 91//80, 10/50, 550, 2, TestingStandard.C2017), party_name="CPP@Measured", farce_extra="SUSPECTED")
        _run(RunSpec(550 * 91//80, 10/50, 550, 2, TestingStandard.C2017, True), party_name="CPP@Measured", farce_extra="SUSPECTED")

        # https://aec.gov.au/Parties_and_Representatives/Party_Registration/Deregistered_parties/files/statement-of-reasons-australian-workers-party-s-137-deregistration.pdf
        # ambiguous case b/c there were 41 duplicates but another list was provided. laws were changed between the two lists.
        # add 20% bonus b/c they were at limit of 550
        # # _run(RunSpec(550*3 * 12//10, xxx/50, 550*3, xx*3), party_name="AWP@Measured (Scaled + Limit Bonus)")
        # # _run(RunSpec(550*3 * 12//10, xxx/550, 550*3, xx*3), party_name="AWP@Threshold (Scaled + Limit Bonus)")

        # https://aec.gov.au/Parties_and_Representatives/Party_Registration/Deregistered_parties/files/statement-of-reasons-seniors-united-party-of-australia-s137-deregistration.pdf
        # add bonus for hitting limit
        # 2021
        _run(RunSpec(629, 9/44, 550, 11, TestingStandard.C2017), party_name="SUP@Measured", farce_extra="SUSPECTED")
        _run(RunSpec(629, 9/44, 550, 11, TestingStandard.C2017, True), party_name="SUP@Measured", farce_extra="SUSPECTED")

        # mb (but unlikely with so many denials): no free tax (https://www.aec.gov.au/Parties_and_Representatives/Party_Registration/Registration_Decisions/2019/statement-of-reasons-the-no-tax-free-electricity.com-refusal.pdf)
        # mb: https://www.aec.gov.au/Parties_and_Representatives/Party_Registration/Registration_Decisions/2019/statement-of-reasons-put-wa-first-party-signed-redacted.pdf

        # https://www.aec.gov.au/Parties_and_Representatives/Party_Registration/Registration_Decisions/2018/2018-voter-rights-party-statement-of-reasons.pdf
        # this one is signed by Kalisch...
        # VRP possible farce but has 35% extra members
        _run(RunSpec(732, 13/41, 550, 22, TestingStandard.C2017), party_name="VRP@Measured", farce_extra="POSSIBLE")
        _run(RunSpec(732, 13/41, 550, 22, TestingStandard.C2017, True), party_name="VRP@Measured", farce_extra="POSSIBLE")

        # https://www.aec.gov.au/Parties_and_Representatives/Party_Registration/Registration_Decisions/2017/sor-australian-affordable-housing-party.pdf
        # possible farce initially
        # note: table of max denials might have been different
        # final list between 511 and 503? avg 507
        _run(RunSpec(550, 2/26, 550, 550-507, TestingStandard.C2017), party_name="AAHP@Measured", farce_extra="POSSIBLE")
        _run(RunSpec(550, 2/26, 550, 550-507, TestingStandard.C2017, True), party_name="AAHP@Measured", farce_extra="POSSIBLE")
        _run(RunSpec(542, 2/26, 542, 542-507, TestingStandard.C2017), party_name="AAHP@Measured", farce_extra="POSSIBLE")
        _run(RunSpec(542, 2/26, 542, 542-507, TestingStandard.C2017, True), party_name="AAHP@Measured", farce_extra="POSSIBLE")

        # https://www.aec.gov.au/Parties_and_Representatives/Party_Registration/Registration_Decisions/2017/sor-the-communists.pdf
        # note: unsure of acceptable number of denials
        # lots of assumptions here, but possible
        _run(RunSpec(708, 10/34, 550, 550-515, TestingStandard.C2017), party_name="Communists2017@Measured", farce_extra="POSSIBLE")
        _run(RunSpec(708, 10/34, 550, 550-515, TestingStandard.C2017, True), party_name="Communists2017@Measured", farce_extra="POSSIBLE")

        # https://www.aec.gov.au/Parties_and_Representatives/party_registration/Registration_Decisions/2013/5204.htm
        # cheaper petrol party
        _run(RunSpec(595, 8/50, 550, 1, TestingStandard.C2012), party_name="CPP2013@Measured", farce_extra="SUSPECTED")
        _run(RunSpec(595, 8/50, 550, 1, TestingStandard.C2017), party_name="CPP2013@Measured with newer testing table", farce_extra="SUSPECTED")
        _run(RunSpec(595, 8/50, 550, 1, TestingStandard.C2012, True), party_name="CPP2013@Measured", farce_extra="SUSPECTED")

        # https://www.aec.gov.au/Parties_and_Representatives/party_registration/Registration_Decisions/2010/3976.htm
        # seniors action movement
        _run(RunSpec(578, 5/37, 550, 15, TestingStandard.C2011), party_name="SAM@Measured", farce_extra="SUSPECTED")
        _run(RunSpec(578, 5/37, 550, 15, TestingStandard.C2011, True), party_name="SAM@Measured", farce_extra="SUSPECTED")

        if non_essential:
            # https://www.aec.gov.au/Parties_and_Representatives/Party_Registration/Registration_Decisions/2021/the-new-liberals-statement-of-reasons.pdf
            # TLN 2021
            # max confidence of 86.6%
            _run(RunSpec(550, 2/37, 550, 27, TestingStandard.C2017), party_name="TNL@2021", farce_extra="POSSIBLE")
            _run(RunSpec(550, 2/37, 550, 27, TestingStandard.C2017, filter_any=True), party_name="TNL@2021", farce_extra="POSSIBLE")

            # https://www.aec.gov.au/Parties_and_Representatives/Party_Registration/Registration_Decisions/2016/files/statement-reasons-australia-first.pdf
            # 512-521 members after filtering
            # max confidence 64.1% (only checked fANY)
            _run(RunSpec(550, 3/34, 550, 29, TestingStandard.C2012, filter_any=True), party_name="AF@2016", farce_extra="POSSIBLE")
            # possible farce
            _run(RunSpec(550, 3/34, 550, 38, TestingStandard.C2012, filter_any=True), party_name="AF@2016", farce_extra="POSSIBLE")

            # https://www.aec.gov.au/Parties_and_Representatives/Party_Registration/Registration_Decisions/2016/files/statement-reasons-rpa.pdf
            # note: party rep did not mention having more than 550 members in AEC report (N unknown)
            _run(RunSpec(550, 13/38, 550, 20, TestingStandard.C2012, filter_any=True), party_name="RPA@2016", farce_extra="POSSIBLE")
            _run(RunSpec(760, 13/38, 550, 20, TestingStandard.C2012, filter_any=True), party_name="RPA@2016", farce_extra="POSSIBLE")

            # https://www.aec.gov.au/Parties_and_Representatives/Party_Registration/Registration_Decisions/2016/files/statement-reasons-dlp.pdf
            # DLP
            # 42 / 540 contacted
            # review successful
            # note: should not have succeeded based on measured P(denial)
            _run(RunSpec(550, 5/42, 550, 10, TestingStandard.C2012, filter_any=True), party_name="DLP@2016", farce_extra="POSSIBLE")
            # confidence 61.1%
            _run(RunSpec(568, 5/42, 550, 10, TestingStandard.C2012, filter_any=True), party_name="DLP@2016", farce_extra="POSSIBLE")

            # https://www.aec.gov.au/Parties_and_Representatives/Party_Registration/Registration_Decisions/2016/files/statement-reasons-australian-democrats.pdf
            # democrats
            # we assume they have more than 550 members b/c of NSW requirements
            _run(RunSpec(550, 5/34, 550, 24, TestingStandard.C2012, filter_any=True), party_name="Democrats@2016", farce_extra="SUSPECTED")
            _run(RunSpec(586, 5/34, 550, 24, TestingStandard.C2012, filter_any=True), party_name="Democrats@2016", farce_extra="SUSPECTED")

        # check 98% confidence of not registering a party with only 400 members
        # note: seems to pan out
        _run(RunSpec(550, 150/550, 550, 0, TestingStandard.C2017), party_name="400of550")
        _run(RunSpec(550, 150/550, 550, 50, TestingStandard.C2017, filter_any=True), party_name="400of550+F50")
        _run(RunSpec(500, 100/500, 500, 0, TestingStandard.C2017), party_name="400of500")
        _run(RunSpec(1650, 450/1650, 1650, 0), party_name="1200of1650")
        _run(RunSpec(1650, 450/1650, 1650, 150, filter_any=True), party_name="1200of1650+F150")
        _run(RunSpec(1500, 300/1500, 1500, 0), party_name="1200of1500")

        # eval table C2012
        _run(RunSpec(500, (500-400) / 500, 500, 0, TestingStandard.C2012), party_name="400of500-C2012")
        _run(RunSpec(503, (503-400) / 503, 503, 0, TestingStandard.C2012), party_name="400of503-C2012")
        _run(RunSpec(512, (512-400) / 512, 512, 0, TestingStandard.C2012), party_name="400of512-C2012")
        _run(RunSpec(521, (521-400) / 521, 521, 0, TestingStandard.C2012), party_name="400of521-C2012")
        _run(RunSpec(529, (529-400) / 529, 529, 0, TestingStandard.C2012), party_name="400of529-C2012")
        _run(RunSpec(529, (529-400) / 529, 529, 0, TestingStandard.C2012Corrected), party_name="400of529-C2012-Corrected")
        _run(RunSpec(537, (537-400) / 537, 537, 0, TestingStandard.C2012), party_name="400of537-C2012")
        _run(RunSpec(543, (543-400) / 543, 543, 0, TestingStandard.C2012), party_name="400of543-C2012")
        _run(RunSpec(548, (548-400) / 548, 548, 0, TestingStandard.C2012), party_name="400of548-C2012")
        _run(RunSpec(550, (550-400) / 550, 550, 0, TestingStandard.C2012), party_name="400of550-C2012")

        # eval table C2012
        _run(RunSpec(500, (500-500) / 500, 500, 0, TestingStandard.C2012), party_name="500of500-C2012")
        _run(RunSpec(503, (503-500) / 503, 503, 0, TestingStandard.C2012), party_name="500of503-C2012")
        _run(RunSpec(512, (512-500) / 512, 512, 0, TestingStandard.C2012), party_name="500of512-C2012")
        _run(RunSpec(521, (521-500) / 521, 521, 0, TestingStandard.C2012), party_name="500of521-C2012")
        _run(RunSpec(529, (529-500) / 529, 529, 0, TestingStandard.C2012), party_name="500of529-C2012")
        _run(RunSpec(529, (529-500) / 529, 529, 0, TestingStandard.C2012Corrected), party_name="500of529-C2012-Corrected")
        _run(RunSpec(537, (537-500) / 537, 537, 0, TestingStandard.C2012), party_name="500of537-C2012")
        _run(RunSpec(543, (543-500) / 543, 543, 0, TestingStandard.C2012), party_name="500of543-C2012")
        _run(RunSpec(548, (548-500) / 548, 548, 0, TestingStandard.C2012), party_name="500of548-C2012")
        _run(RunSpec(550, (550-500) / 550, 550, 0, TestingStandard.C2012), party_name="500of550-C2012")

        # eval table C2012 - threshold + filtering
        _run(RunSpec(1100, 50/550, 550, (550-500), TestingStandard.C2012, filter_any=True), party_name="550of1100-C2012")
        _run(RunSpec(1100, 50/550, 550, (550-503), TestingStandard.C2012, filter_any=True), party_name="550of1100-C2012")
        _run(RunSpec(1100, 50/550, 550, (550-512), TestingStandard.C2012, filter_any=True), party_name="550of1100-C2012")
        _run(RunSpec(1100, 50/550, 550, (550-521), TestingStandard.C2012, filter_any=True), party_name="550of1100-C2012")
        _run(RunSpec(1100, 50/550, 550, (550-529), TestingStandard.C2012, filter_any=True), party_name="550of1100-C2012")
        _run(RunSpec(1100, 50/550, 550, (550-529), TestingStandard.C2012Corrected, filter_any=True), party_name="550of1100-C2012-Corrected")
        _run(RunSpec(1100, 50/550, 550, (550-537), TestingStandard.C2012, filter_any=True), party_name="550of1100-C2012")
        _run(RunSpec(1100, 50/550, 550, (550-543), TestingStandard.C2012, filter_any=True), party_name="550of1100-C2012")
        _run(RunSpec(1100, 50/550, 550, (550-548), TestingStandard.C2012, filter_any=True), party_name="550of1100-C2012")
        _run(RunSpec(1100, 50/550, 550, (550-550), TestingStandard.C2012, filter_any=True), party_name="550of1100-C2012")

        # eval table C2012 - p(denial) = 0.2 + filtering
        _run(RunSpec(1100, 0.2, 550, (550-500), TestingStandard.C2012, filter_any=True), party_name="550of1100-C2012")
        _run(RunSpec(1100, 0.2, 550, (550-503), TestingStandard.C2012, filter_any=True), party_name="550of1100-C2012")
        _run(RunSpec(1100, 0.2, 550, (550-512), TestingStandard.C2012, filter_any=True), party_name="550of1100-C2012")
        _run(RunSpec(1100, 0.2, 550, (550-521), TestingStandard.C2012, filter_any=True), party_name="550of1100-C2012")
        _run(RunSpec(1100, 0.2, 550, (550-529), TestingStandard.C2012, filter_any=True), party_name="550of1100-C2012")
        _run(RunSpec(1100, 0.2, 550, (550-529), TestingStandard.C2012Corrected, filter_any=True), party_name="550of1100-C2012-Corrected")
        _run(RunSpec(1100, 0.2, 550, (550-537), TestingStandard.C2012, filter_any=True), party_name="550of1100-C2012")
        _run(RunSpec(1100, 0.2, 550, (550-543), TestingStandard.C2012, filter_any=True), party_name="550of1100-C2012")
        _run(RunSpec(1100, 0.2, 550, (550-548), TestingStandard.C2012, filter_any=True), party_name="550of1100-C2012")
        _run(RunSpec(1100, 0.2, 550, (550-550), TestingStandard.C2012, filter_any=True), party_name="550of1100-C2012")

        # eval table SEPT2021 - threshold + filtering
        _run(RunSpec(3300, 150/1650, 1650, (1650-1500), TestingStandard.SEPT2021, filter_any=True), party_name="1500of3300-SEPT2021")
        _run(RunSpec(3300, 150/1650, 1650, (1650-1506), TestingStandard.SEPT2021, filter_any=True), party_name="1500of3300-SEPT2021")
        _run(RunSpec(3300, 150/1650, 1650, (1650-1523), TestingStandard.SEPT2021, filter_any=True), party_name="1500of3300-SEPT2021")
        _run(RunSpec(3300, 150/1650, 1650, (1650-1543), TestingStandard.SEPT2021, filter_any=True), party_name="1500of3300-SEPT2021")
        _run(RunSpec(3300, 150/1650, 1650, (1650-1582), TestingStandard.SEPT2021, filter_any=True), party_name="1500of3300-SEPT2021")
        _run(RunSpec(3300, 150/1650, 1650, (1650-1599), TestingStandard.SEPT2021, filter_any=True), party_name="1500of3300-SEPT2021")
        _run(RunSpec(3300, 150/1650, 1650, (1650-1562), TestingStandard.SEPT2021, filter_any=True), party_name="1500of3300-SEPT2021")
        _run(RunSpec(3300, 150/1650, 1650, (1650-1616), TestingStandard.SEPT2021, filter_any=True), party_name="1500of3300-SEPT2021")
        _run(RunSpec(3300, 150/1650, 1650, (1650-1633), TestingStandard.SEPT2021, filter_any=True), party_name="1500of3300-SEPT2021")
        _run(RunSpec(3300, 150/1650, 1650, (1650-1647), TestingStandard.SEPT2021, filter_any=True), party_name="1500of3300-SEPT2021")
        _run(RunSpec(3300, 150/1650, 1650, (1650-1650), TestingStandard.SEPT2021, filter_any=True), party_name="1500of3300-SEPT2021")

        # eval table SEPT2021 - p(denial)=0.2 + filtering
        _run(RunSpec(3300, 0.2, 1650, (1650-1500), TestingStandard.SEPT2021, filter_any=True), party_name="1500of3300-SEPT2021")
        _run(RunSpec(3300, 0.2, 1650, (1650-1506), TestingStandard.SEPT2021, filter_any=True), party_name="1500of3300-SEPT2021")
        _run(RunSpec(3300, 0.2, 1650, (1650-1523), TestingStandard.SEPT2021, filter_any=True), party_name="1500of3300-SEPT2021")
        _run(RunSpec(3300, 0.2, 1650, (1650-1543), TestingStandard.SEPT2021, filter_any=True), party_name="1500of3300-SEPT2021")
        _run(RunSpec(3300, 0.2, 1650, (1650-1582), TestingStandard.SEPT2021, filter_any=True), party_name="1500of3300-SEPT2021")
        _run(RunSpec(3300, 0.2, 1650, (1650-1599), TestingStandard.SEPT2021, filter_any=True), party_name="1500of3300-SEPT2021")
        _run(RunSpec(3300, 0.2, 1650, (1650-1562), TestingStandard.SEPT2021, filter_any=True), party_name="1500of3300-SEPT2021")
        _run(RunSpec(3300, 0.2, 1650, (1650-1616), TestingStandard.SEPT2021, filter_any=True), party_name="1500of3300-SEPT2021")
        _run(RunSpec(3300, 0.2, 1650, (1650-1633), TestingStandard.SEPT2021, filter_any=True), party_name="1500of3300-SEPT2021")
        _run(RunSpec(3300, 0.2, 1650, (1650-1647), TestingStandard.SEPT2021, filter_any=True), party_name="1500of3300-SEPT2021")
        _run(RunSpec(3300, 0.2, 1650, (1650-1650), TestingStandard.SEPT2021, filter_any=True), party_name="1500of3300-SEPT2021")

        # eval table SEPT2021 risk of rejecting 1500 (P(fail))
        _run(RunSpec(1500, (1500-1500) / 1500, 1500, 0, TestingStandard.SEPT2021), party_name="1500of1500-SEPT2021")
        _run(RunSpec(1506, (1506-1500) / 1506, 1506, 0, TestingStandard.SEPT2021), party_name="1500of1506-SEPT2021")
        _run(RunSpec(1523, (1523-1500) / 1523, 1523, 0, TestingStandard.SEPT2021), party_name="1500of1523-SEPT2021")
        _run(RunSpec(1543, (1543-1500) / 1543, 1543, 0, TestingStandard.SEPT2021), party_name="1500of1543-SEPT2021")
        _run(RunSpec(1562, (1562-1500) / 1562, 1562, 0, TestingStandard.SEPT2021), party_name="1500of1562-SEPT2021")
        _run(RunSpec(1582, (1582-1500) / 1582, 1582, 0, TestingStandard.SEPT2021), party_name="1500of1582-SEPT2021")
        _run(RunSpec(1599, (1599-1500) / 1599, 1599, 0, TestingStandard.SEPT2021), party_name="1500of1599-SEPT2021")
        _run(RunSpec(1616, (1616-1500) / 1616, 1616, 0, TestingStandard.SEPT2021), party_name="1500of1616-SEPT2021")
        _run(RunSpec(1633, (1633-1500) / 1633, 1633, 0, TestingStandard.SEPT2021), party_name="1500of1633-SEPT2021")
        _run(RunSpec(1647, (1647-1500) / 1647, 1647, 0, TestingStandard.SEPT2021), party_name="1500of1647-SEPT2021")
        _run(RunSpec(1650, (1650-1500) / 1650, 1650, 0, TestingStandard.SEPT2021), party_name="1500of1650-SEPT2021")

        # eval table SEPT2021 risk of accepting 1200 (P(pass))
        _run(RunSpec(1500, (1500-1200) / 1500, 1500, 0, TestingStandard.SEPT2021), party_name="1200of1500-SEPT2021")
        _run(RunSpec(1506, (1506-1200) / 1506, 1506, 0, TestingStandard.SEPT2021), party_name="1200of1506-SEPT2021")
        _run(RunSpec(1523, (1523-1200) / 1523, 1523, 0, TestingStandard.SEPT2021), party_name="1200of1523-SEPT2021")
        _run(RunSpec(1543, (1543-1200) / 1543, 1543, 0, TestingStandard.SEPT2021), party_name="1200of1543-SEPT2021")
        _run(RunSpec(1562, (1562-1200) / 1562, 1562, 0, TestingStandard.SEPT2021), party_name="1200of1562-SEPT2021")
        _run(RunSpec(1582, (1582-1200) / 1582, 1582, 0, TestingStandard.SEPT2021), party_name="1200of1582-SEPT2021")
        _run(RunSpec(1599, (1599-1200) / 1599, 1599, 0, TestingStandard.SEPT2021), party_name="1200of1599-SEPT2021")
        _run(RunSpec(1616, (1616-1200) / 1616, 1616, 0, TestingStandard.SEPT2021), party_name="1200of1616-SEPT2021")
        _run(RunSpec(1633, (1633-1200) / 1633, 1633, 0, TestingStandard.SEPT2021), party_name="1200of1633-SEPT2021")
        _run(RunSpec(1647, (1647-1200) / 1647, 1647, 0, TestingStandard.SEPT2021), party_name="1200of1647-SEPT2021")
        _run(RunSpec(1650, (1650-1200) / 1650, 1650, 0, TestingStandard.SEPT2021), party_name="1200of1650-SEPT2021")

        if non_essential:
            _run(RunSpec(frs.total_members, 0.10, 1650, frs.n_members_removed), party_name="Flux@0.10")
            _run(RunSpec(frs.total_members, 0.12, 1650, frs.n_members_removed), party_name="Flux@0.12")
            _run(RunSpec(frs.total_members, 0.14, 1650, frs.n_members_removed), party_name="Flux@0.14")
            _run(RunSpec(frs.total_members, 0.16, 1650, frs.n_members_removed), party_name="Flux@0.16")
            _run(RunSpec(frs.total_members, 0.18, 1650, frs.n_members_removed), party_name="Flux@0.18")
            _run(RunSpec(1650, 150/1650, 1650, 0), party_name="1650@Thresh")
            _run(RunSpec(1650, 150/1650, 1650, 25), party_name="1650@Thresh+F25")
            _run(RunSpec(1650, 150/1650, 1650, 50), party_name="1650@Thresh+F50")
            _run(RunSpec(1625, 150/1625, 1625, 0), party_name="1625@Thresh")
            _run(RunSpec(1600, 150/1600, 1600, 25))
            _run(RunSpec(1650, 0.06, 1650, 0))
            _run(RunSpec(1650, 0.09, 1650, 0))
            _run(RunSpec(1650, 0.16, 1650, 0))
            _run(RunSpec(1650, 0.17, 1650, 0))
            _run(RunSpec(1650, 150/1650, 1650, 0))
            _run(RunSpec(1650, 150/1650, 1650, 5))
            _run(RunSpec(1650, 150/1650, 1650, 18))
            _run(RunSpec(1650, (150-18)/1650, 1650, 18))
            _run(RunSpec(1650, 150/1650, 1650, 25))
            _run(RunSpec(1750, 200/1750, 1650, 25))
            _run(RunSpec(1850, 150/1650, 1650, 50), party_name="1850@Thresh+F50")
            _run(RunSpec(1850, 200/1850, 1650, 0))
            _run(RunSpec(1850, 200/1850, 1650, 25))
            _run(RunSpec(2000, 150/2000, 1650, 25))
            _run(RunSpec(2000, 300/2000, 1650, 0))
            _run(RunSpec(2000, 300/2000, 1650, 5))
            _run(RunSpec(2000, 300/2000, 1650, 6))
            _run(RunSpec(2000, 300/2000, 1650, 7))
            _run(RunSpec(2000, 300/2000, 1650, 8))
            _run(RunSpec(2000, 300/2000, 1650, 10))
            _run(RunSpec(2000, 300/2000, 1650, 15))
            _run(RunSpec(2000, 300/2000, 1650, 25))
            _run(RunSpec(2000, 400/2000, 1650, 25))
            _run(RunSpec(2500, 300/2500, 1650, 25))
            _run(RunSpec(2500, 500/2500, 1650, 25))
            _run(RunSpec(2500, 1000/2500, 1650, 25))


if __name__ == "__main__":
    aec()
