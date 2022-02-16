#!/usr/bin/env python3

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


def filter_n_members(f, members, n_to_filter):
    n_filtered = 0
    for m in members:
        if f(m) and n_filtered < n_to_filter:
            n_filtered += 1
            continue
        yield m


assert list(filter_n_members(lambda x: x%2 == 0, range(5), 0)) == [0,1,2,3,4]
assert list(filter_n_members(lambda x: x%2 == 0, range(5), 1)) == [1,2,3,4]
assert list(filter_n_members(lambda x: x%2 == 0, range(5), 2)) == [1,3,4]
assert list(filter_n_members(lambda x: x%2 == 0, range(5), 3)) == [1,3]
assert list(filter_n_members(lambda x: x%2 == 0, range(5), 4)) == [1,3]


AEC_TESTING_TABLE = [
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

OLD_AEC_TESTING_TABLE = [
    (500, 18, 0),
    (503, 26, 1),
    (511, 32, 2),
    (519, 37, 3),
    (526, 41, 4),
    (534, 44, 5),
    (541, 47, 6),
    (548, 50, 7),
    (551, 50, 7),  # we subtract 1 later for upper bound
]

AEC_TESTING_RANGES = list((lower, upper - 1, n, x) for ((lower, n, x), (upper, _, _)) in zip(AEC_TESTING_TABLE, AEC_TESTING_TABLE[1:]))
OLD_AEC_TESTING_RANGES = list((lower, upper - 1, n, x) for ((lower, n, x), (upper, _, _)) in zip(OLD_AEC_TESTING_TABLE, OLD_AEC_TESTING_TABLE[1:]))


def lookup_aec_testing_parameters(sample_size, members_required: int):
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
    '''
    testing_ranges = {
        1500: AEC_TESTING_RANGES,
        500: OLD_AEC_TESTING_RANGES,
     }[members_required]
    for (l, u, n, x) in testing_ranges:
        if l <= sample_size <= u:
            return (n, x)
    raise Exception(f"Invalid sample size: {sample_size} -- should be between {members_required} and {members_required * 11 // 10} inclusive")


assert lookup_aec_testing_parameters(1_626, 1500) == (53, 7)


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
    min_list_limit: int = 1500

    def as_tuple(self):
        return self.total_members, self.failure_rate, self.sample_size, self.n_members_removed

    def title_line(self, party_name: Optional[str] = None):
        is_valid = self.total_members * (1 - self.failure_rate) >= self.min_list_limit
        return f"AEC membership test results PMF (Party {if_else(is_valid, 'IS', 'IS NOT')} eligible)" + if_else(party_name, f" | Based on: {party_name}", "")

    @property
    def max_list_limit(self):
        return self.min_list_limit * 11 // 10

    @property
    def sample_size(self):
        assert self._sample_size <= self.total_members
        return min(self.max_list_limit, self._sample_size)

    @property
    def n_failing_members(self):
        return calc_failing_members_n(self.total_members, self.failure_rate)

    @property
    def n_real_members(self):
        return self.total_members - self.n_failing_members

    @property
    def n_sample_real_m(self):
        return round(self.sample_size * self.n_real_members / self.total_members) - self.n_members_removed

    @property
    def n_sample_failing_m(self):
        return round(self.sample_size * self.n_failing_members / self.total_members)

    def subtitle_line(self):
        return " | ".join([
            f"N Members = {self.total_members} (Y: {self.n_real_members}, N: {self.n_failing_members})",
            f"List Sample: (Y: {self.n_sample_real_m}, N: {self.n_sample_failing_m})",
            f"P(member says 'No') = {self.failure_rate:.3f}",
            f"Members Filtered Out = {self.n_members_removed}",
        ])

    def out_fname(self, n_trials, party_name: Optional[str], is_farce: bool):
        failing_members = calc_failing_members_n(self.total_members, self.failure_rate)
        fname_suffix = f"{name_to_fname_sfx(party_name)}" if party_name else None
        fname_parts: list[str] = list(map(str, filter(lambda x: x is not None, [
            "aec-test-sim",
            "FARCE" if is_farce else None,
            f"N{n_trials}-m{self.total_members}-f{failing_members}-s{self.sample_size}-r{self.n_members_removed}",
            fname_suffix,
        ])))
        return "-".join(fname_parts)


default_run_spec = RunSpec(total_members=4_680, failure_rate=0.17, _sample_size=1_649, n_members_removed=24)
flux_run_spec = default_run_spec


def name_to_fname_sfx(n: str):
    return n.lower().strip().replace(' ', '-').replace('(', '').replace(')', '').replace('@', '_')


# shuffle members, take 1649, eliminate 24, sample 53, record X failures
# for trial_ix in range(n_trials):
def run_trials(n_trials, total_members, failure_rate, sample_size, n_members_removed, reduced_sample_size, n_to_sample):
    # generate a list of members with some given non-member rate (i.e. these members will always fail)
    members = list(mk_members(total_members, failure_rate))

    results = []
    for _ in range(n_trials):
        # take sample
        membership_sample = r.sample(members, sample_size)

        # remove n_members_removed true members (this is the worst case for the party).
        #   members can be removed b/c their details couldn't be matched, they're deceased, or b/c they've supported another party's rego.
        #   we always want to remove true members to measure worst case performance of methodology
        reduced_sample = list(filter_n_members(lambda m: m[1], membership_sample, n_members_removed))
        assert reduced_sample_size == len(reduced_sample)

        # perform check (contact member to confirm)
        actual_sample = r.sample(reduced_sample, n_to_sample)
        # count and failures
        n_failures = sum(0 if m[1] else 1 for m in actual_sample)

        # if trial_ix % status_after_trials == 0:
        #     pct_done = trial_ix / n_trials
        #     print(f"[{pct_done:6.2%}] Completed trial {trial_ix} of {n_trials}")

        # return n_failures
        results.append(n_failures)
    return results


def run(trial_pool: pool.Pool, n_trials: int, run_spec: RunSpec, graph_title=None, graph_fname=None, show=True, party_name=None, force=False):
    output_files_exist = any(all(os.path.exists(f'./{ext}/{run_spec.out_fname(n_trials, party_name, is_farce)}.{ext}') for ext in ['png', 'csv']) for is_farce in [True, False])
    if not force and output_files_exist:
        print(f"Output files exist (use --force to overwrite) -- skipping run: {run_spec}")
        return

    print(f"\n# Running {n_trials} rounds for {run_spec} #")
    total_members, failure_rate, sample_size, n_members_removed = run_spec.as_tuple()
    reduced_sample_size = sample_size - n_members_removed
    n_to_sample, max_failures = lookup_aec_testing_parameters(reduced_sample_size, run_spec.min_list_limit)
    status_after_trials = n_trials // 10

    n_failing_members = calc_failing_members_n(total_members, failure_rate)
    n_real_members = total_members - n_failing_members
    n_sample_real_m = round(sample_size * n_real_members / total_members) - run_spec.n_members_removed
    n_sample_failing_m = round(sample_size * n_failing_members / total_members)
    assert n_sample_real_m + n_sample_failing_m <= sample_size
    pass_expected = run_spec.n_sample_real_m >= run_spec.min_list_limit

    failure_counts = [0] * (n_to_sample + 1)

    print(f"Running trials --- n_jobs = {SIM_CHUNKS}.")
    with Timer(f"Simulation(N={n_trials})", auto_print=True):
        trial_chunk_params = (n_trials // SIM_CHUNKS), total_members, failure_rate, sample_size, n_members_removed, reduced_sample_size, n_to_sample
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
    plt.subplots_adjust(top=0.83)
    plt.legend()

    if is_farce:
        loc = (n_cols - 2, max_p / 2)
        bbox = {'facecolor': 'none', 'edgecolor': 'red', 'lw': 3}
        plt.text(loc[0], loc[1], "FARCE", ha='right', va='center', color='red', fontweight='black', fontsize=20, bbox=bbox)

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
def aec(n_trials, show, jobs, force):
    frs = flux_run_spec
    trial_pool = mp.Pool(jobs or SIM_CHUNKS)
    def _run(*args, **kwargs):
        _kwargs = dict(show=show, force=force)
        _kwargs.update(kwargs)
        run(trial_pool, n_trials, *args, **_kwargs)
    _run(default_run_spec, party_name="Flux")
    # _run(RunSpec(frs.total_members, 0.10, 1650, frs.n_members_removed), party_name="Flux@0.10")
    # _run(RunSpec(frs.total_members, 0.12, 1650, frs.n_members_removed), party_name="Flux@0.12")
    _run(RunSpec(frs.total_members, 0.14, 1650, frs.n_members_removed), party_name="Flux@0.14")
    _run(RunSpec(frs.total_members, 0.16, 1650, frs.n_members_removed), party_name="Flux@0.16")
    _run(RunSpec(frs.total_members, 0.18, 1650, frs.n_members_removed), party_name="Flux@0.18")
    _run(RunSpec(frs.total_members, frs.failure_rate, 1650, 0), party_name="Flux+NoFilter")
    _run(RunSpec(round(frs.total_members * 1.2), (796 + frs.total_members * 0.1) / frs.total_members / 1.2, 1650, 0), party_name="Flux+Gain20%Lose10%")
    _run(RunSpec(round(frs.total_members * 1.2), (796 + frs.total_members * 0.1) / frs.total_members / 1.2, 1650, 24), party_name="Flux+Gain20%Lose10%")
    _run(RunSpec(round(frs.total_members * 2), (796 + frs.total_members * 0.333) / frs.total_members / 2, 1650, 0), party_name="Flux+Gain100%Lose33%")
    _run(RunSpec(round(frs.total_members * 2), (796 + frs.total_members * 0.333) / frs.total_members / 2, 1650, 24), party_name="Flux+Gain100%Lose33%")
    _run(RunSpec(frs.total_members, 0.5, 1650, 0), party_name="Flux+HalfBadMembers")
    _run(RunSpec(frs.total_members, 150/1650, frs.sample_size, frs.n_members_removed), party_name="Flux@Thresh")
    # _run(RunSpec(1650, 150/1650, 1650, 0), party_name="1650@Thresh")
    # _run(RunSpec(1650, 150/1650, 1650, 25), party_name="1650@Thresh+F25")
    # _run(RunSpec(1625, 150/1625, 1625, 0), party_name="1625@Thresh")
    # _run(RunSpec(1600, 150/1600, 1600, 25))
    # _run(RunSpec(1650, 0.06, 1650, 0))
    # _run(RunSpec(1650, 0.09, 1650, 0))
    # _run(RunSpec(1650, 0.16, 1650, 0))
    # _run(RunSpec(1650, 0.17, 1650, 0))
    # _run(RunSpec(1650, 150/1650, 1650, 0))
    # _run(RunSpec(1650, 150/1650, 1650, 5))
    # _run(RunSpec(1650, 150/1650, 1650, 18))
    # _run(RunSpec(1650, (150-18)/1650, 1650, 18))
    # _run(RunSpec(1650, 150/1650, 1650, 25))
    # _run(RunSpec(1750, 200/1750, 1650, 25))
    # _run(RunSpec(1850, 200/1850, 1650, 0))
    # _run(RunSpec(1850, 200/1850, 1650, 25))
    # _run(RunSpec(2000, 150/2000, 1650, 25))
    # _run(RunSpec(2000, 300/2000, 1650, 0))
    # _run(RunSpec(2000, 300/2000, 1650, 5))
    # _run(RunSpec(2000, 300/2000, 1650, 6))
    # _run(RunSpec(2000, 300/2000, 1650, 7))
    # _run(RunSpec(2000, 300/2000, 1650, 8))
    # _run(RunSpec(2000, 300/2000, 1650, 10))
    # _run(RunSpec(2000, 300/2000, 1650, 15))
    # _run(RunSpec(2000, 300/2000, 1650, 25))
    _run(RunSpec(2000, 400/2000, 1650, 25))
    _run(RunSpec(2500, 300/2500, 1650, 25))
    _run(RunSpec(2500, 500/2500, 1650, 25))
    _run(RunSpec(2500, 1000/2500, 1650, 25))
    _run(RunSpec(20000, 0.5, 1650, 0))

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
    # add 20% bonus b/c they were at limit of 550
    # _run(RunSpec(550*3 * 12//10, 10/50, 550*3, 2*3), party_name="CPP@Measured (Scaled + Limit Bonus)")
    # _run(RunSpec(550*3 * 12//10, 50/550, 550*3, 2*3), party_name="CPP@Threshold (Scaled + Limit Bonus)")
    _run(RunSpec(550 * 12//10, 10/50, 550, 2, 500), party_name="CPP@Measured (Limit Bonus)")

    # https://aec.gov.au/Parties_and_Representatives/Party_Registration/Deregistered_parties/files/statement-of-reasons-australian-workers-party-s-137-deregistration.pdf
    # ambiguous case b/c there were 41 duplicates but another list was provided. laws were changed between the two lists.
    # add 20% bonus b/c they were at limit of 550
    # # _run(RunSpec(550*3 * 12//10, xxx/50, 550*3, xx*3), party_name="AWP@Measured (Scaled + Limit Bonus)")
    # # _run(RunSpec(550*3 * 12//10, xxx/550, 550*3, xx*3), party_name="AWP@Threshold (Scaled + Limit Bonus)")

    # https://aec.gov.au/Parties_and_Representatives/Party_Registration/Deregistered_parties/files/statement-of-reasons-seniors-united-party-of-australia-s137-deregistration.pdf
    # add 20% bonus for hitting limit
    # _run(RunSpec(550*3 * 12//10, 9/44, 550*3, 11*3), party_name="SUP@Measured (Scaled+Limit Bonus)")
    # _run(RunSpec(550*3 * 12//10, 5/55, 550*3, 11*3), party_name="SUP@Threshold (Scaled+Limit Bonus)")
    _run(RunSpec(550 * 12//10, 9/44, 550, 11, 500), party_name="SUP@Measured (Limit Bonus)")

if __name__ == "__main__":
    aec()
