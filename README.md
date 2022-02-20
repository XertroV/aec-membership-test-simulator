# AEC Party Membership Test Methodology is Rigged! A Statistical Analysis of AEC Methodology and Graphs (of PMFs)

<p align="center">
    <a href="https://xertrov.github.io/aec-membership-test-simulator/">Website</a>
    |
    <a href="https://github.com/XertroV/aec-membership-test-simulator">Source Code</a>
    <br><br>
    <em>Max Kaye</em>
    <!-- (Philosopher) -->
    <br>
    2022-02-15 to 2022-02-20
</p>

## TOC

1. [Background Context](#1-background-context)
2. [Regular Membership Testing](#2-regular-membership-testing)
3. [Flux’s 2021 Membership Test: A Known Farce](#3-fluxs-2021-membership-test-a-known-farce)
4. [Analysis Methodology](#4-analysis-methodology)
5. [Major Findings](#5-major-findings)
6. [Suspected Farces](#6-suspected-farces)
7. [Flux’s 2021 Membership Test Assuming a Threshold (9.09%) Denial Rate (including worst-case)](#7-fluxs-2021-membership-test-assuming-a-threshold-909-denial-rate-including-worst-case)
8. [Feedback Loops Between AEC Policy and Party Behavior](#8-feedback-loops-between-aec-policy-and-party-behavior)
9. [Conclusion](#9-conclusion)
10. [Appendix: Definitions](#appendix-definitions)
11. [Appendix: AEC Membership Testing Tables](#appendix-aec-membership-testing-tables)
12. [Appendix: Errors in Feb 13 response to AEC](#appendix-errors-in-feb-13-response-to-aec)

## Abstract / Executive Summary

In Australia, to register a political party you need a minimum number of members.
Federally, that's *usually* 1500 (as of September 2021) -- the Australian Electoral Commission (AEC) will conduct membership tests to verify this minimum.
Political parties *with* a parliamentarian have no minimum membership limit and are not tested.
Political parties *without* a parliamentarian must go through a membership test when they register, and then once every election cycle thereafter.

This document evaluates the AEC's testing methodology for particular cases and finds that there are real-world situations where the testing methodology has a false negative (improper failure) rate over 50%, and often much higher.

Therefore, it is reasonable to conclude, for those cases: the methodology is *rigged* and a *farce*.

If something is *rigged* and a *farce* -- based on the definitions included and cited in the appendix -- then it is an *unfair, empty act*, done *for show* where the *outcome is already known*. This document proves that the current method has unfair and predetermined outcomes for many situations.

**Note: I am not accusing the AEC of doing the rigging; just proving that the method *is* rigged.**

To date, there is 1 known incident of a farce and *at least* 5 suspected incidents.
<!-- There may be many more incidents, but the results of most membership tests are not available.
(An FOI request may solve this.) -->

The Flux Party's recent 2021 membership test is analysed in multiple ways:

* **Measured case**: a 17% membership denial rate -- as measured by the AEC during this membership test.
* **More extreme -- but realistic -- cases**: These are more extreme cases than the measured case, but it is an assumption of *all* cases that the party is eligible under the Electoral Act.
* **Threshold case**: the assumption that 9.09% of any membership list submitted will result in membership denials. I *suspect* this is an AEC assumption used for calculating the maximum number of denials for [the AEC's table (given their advertised confidences)](https://web.archive.org/web/20120511194720/http://www.aec.gov.au/Parties_and_Representatives/party_registration/Registration_Decisions/registration-tests.htm).

Experimental evidence shows that the *measured* confidence of The Flux Party's 2021 membership test was **just 28.3%**. This is despite *the experimental assumption* that Flux has more than the legislatively required number of members.

Experimental evidence shows that the AEC's confidence of the *threshold* case was 89.0%, *which is less than the limit [previously advertised (90%)](https://web.archive.org/web/20120511194720/http://www.aec.gov.au/Parties_and_Representatives/party_registration/Registration_Decisions/registration-tests.htm)*. The confidence of the AEC's method is only that high because Flux has gone to a great deal of effort to increase the quality of our membership lists -- **in large part due to inadequacies of the AEC's methodology.**

**Experimental evidence proves that the AEC's claim** that their membership tests are conducted to a confidence of 90% **is false**. In actual fact, for a party that is capable of providing a list of 1,650 members wherein exactly 1,500 members will not deny membership (and 150 will): **the worst-case confidence of the AEC's membership test is just 15.1%, indicating a false negative rate of 84.9%.**

In other cases, where a party is capable of providing 1,500 members that will not deny membership (with no limit on the number of members that will deny membership), **the lower-bound on the confidence of the AEC's method is 0%.** That is: it fails 100% of the time for certain valid parties.

This is not a theoretical problem. It has been happening and continues to happen. The AEC has been enforcing a policy that compromises the integrity of our political process. The ABS has been complicit. Political elites have exploited this.

*Note: equivalent calculated values in this document (including graphs) are assumed to have a combined, codependent error of ±0.3 percentage points (i.e., as values, they differ by 0.003 at most). e.g., a graph might say the the false negative rate is 11.0%, but the accompanying text says 10.8%. This is taken to be negligible and a non-critical error.*

<!-- *Disclosure and context: My roles in The Flux Party (Flux) are: a founder, the deputy leader, the secretary, and the deputy registered officer.* -->

## 1. Background Context

Recently (leading up to September 2021), most parliamentarians (i.e., the 4 major parties) decided that we had too many political parties and that this was a problem! It would not do. So, a bunch of changes were made to the Electoral Act. Changes designed to make life harder for anyone who wanted to be part of our democracy, but did not want to participate in the rotten, tribalist, political cults that run the show. Some of those changes resulted in (as of Feb 2022) the pending deregistration of 12 parties, and the very real deregistration of 9 parties. In practice that is ~40% of parties, gone before the next election. Political elites will claim (and have claimed in Parliament already) that these changes, the culling, and the subsequent entrenchment of the status quo, is a good thing. That it is making our democracy better.

In September 2021, the legislatively required number of members for a political party was increased from 500 to 1500 with little warning and no grace period.
The AEC's policies -- going back at least a decade -- have encouraged parties not to bother going over 550 members (which are verifiable against the roll).

## 2. Regular Membership Testing

Every few years, the Australian Electoral Commission (AEC) will check that each political party has enough members according to the legislative requirement. The party must provide a list of 1500 to 1650 names (inclusive) to use as evidence of their eligibility. The AEC will then filter out some names (duplicates, deceased members, etc). That produces a NEW list of ≤ 1650 names. Then, the AEC will do a statistical sampling of members and will use that to determine whether a party is eligible. Particularly, a small subset of members are selected and contacted, asking for a yes/no confirmation of membership. Non-responses are skipped. A "No" answer counts as a failure -- this is a *membership denial*. In this document and associated code: "failure rate" refers to the rate at which members respond "No".

The AEC does not accept lists larger than 1650; there is no chance for a party to replace any of those filtered members; that filtering process increases the chance of false negatives (when list length is limited + excluding duplicates); parties are not told which members were filtered (even those which are deceased) so they cannot be proactively removed; and, finally, the standard of statistical evaluation is to assume that the list of 1650 members were *the only members* of the party. Zero consideration is given beyond this (outside the chance to respond). How many parties have been wrongly denied registration? Nobody knows.

[The method is detailed on pages 23 and 24 of "Guide for registering a
party".](https://www.aec.gov.au/Parties_and_Representatives/Party_Registration/guide/files/party-registration-guide.pdf)
([mirror](https://xertrov.github.io/aec-membership-test-simulator/docs/party-registration-guide.pdf))

## 3. Flux's 2021 Membership Test: A Known Farce

Flux failed its recent membership test. The only problem? We have at least 4680 members whose details have been matched against the electoral roll. It is the AEC's imposition of 1650 members maximum that is the problem.

Note that Flux is only in a position to offer so many members because of our unique membership system: free for life. Additionally, significant automation has been developed to assist members in verifying their details against the electoral roll and keeping their details up to date. This is a task too involved, expensive, and specialized for it to be practical for most political parties.

<!--
FOI:
- all documents and communications regarding both policy changes and decisions that concern the upper limit of acceptable membership lists.
- all documents and communications regarding minimising the work of new and existing parties as relating to the upper limit of acceptable membership lists as used for membership tests. example of mention: <https://www.aec.gov.au/Parties_and_Representatives/Party_Registration/Registration_Decisions/2018/2018-commonwealth-of-australia-party-statement-of-reasons.pdf>
  > This is considered to be to a party’s advantage, by minimising the work required of the party in confirming the enrolment status and contact details of additional other members
- all documents and communications regarding what is and is not in a party's advantage and/or disadvantage in relation to registration procedures and/or membership testing.
- all documents and communications regarding what is and is not in a AEC's advantage and/or disadvantage in relation to registration procedures and/or membership testing.
- all documents and communications regarding what is and is not in a Parliamentarian's advantage and/or disadvantage in relation to registration procedures and/or membership testing.
- all documents and communications regarding what is and is not to the advantage and/or disadvantage of a party other than the one undergoing testing in relation to registration procedures and/or membership testing.
- all documents and communications regarding what is and is not to the advantage and/or disadvantage of any other entity or person (including members of parties undergoing testing) that may be effected by the membership testing process, especially including those regarding potential discrimination or wrongful advantage on the basis of that entity's age, sex, gender, ethnicity, race, location, available methods of communication.
- historical records of all successful and unsuccessful membership tests conducted by the AEC, ever.
  - including: the party involved; the length of the membership list submitted; counts of how many members were filtered out and for which reasons; length of the membership list that was sampled from for the purposes of contacting members to confirm or deny their membership; the total number of contact attempts made; the number of successful attempts and aggregate result (indicating the total counts of which of the 3 possible responses were received: yes / no / other); the date that the results of the membership test were judged to satisfy or fail the legislative requirement for non-parliamentary party membership such that the date may be used to determine the exact standards by which the results were judged.
- all communications with new/existing parties (or a representative of it) undergoing testing wherein the party or a representative of it: expresses a desire to submit a larger membership list than AEC policy allowed; or indicates that their membership numbers exceed the limit imposed by AEC policy.
- all policy documents regarding the statistical measures by which the results of a membership test are judged (i.e., the policy documents that are based on ABS recommendations regarding the number of members contacted and the threshold of maximum denials received).
- all ABS recommendations and associated communications (with the AEC) regarding the AEC's membership testing process.
- all complaints (including expressions of concern) from anyone outside the AEC regarding the fairness, integrity, and/or validity of the membership testing process; communications regarding such complaints (including but not limited to those between AEC staff, AEC and ABS staff, AEC and APH staff, AEC and parliamentarians, and AEC and parliamentarians' staff); policy documents changed as a result of such complaints; the prior version of each policy document that was changed as a result of such complaints.
- all documents, including computer code and spreadsheets (including embedded formulas), regarding the mathematical/statistical elements (e.g., foundations, 'working out', justification for certain limits and/or parameters of the method, confidence intervals, calculations, how to apply results, etc) of the membership testing procedure held by the AEC, including all past, present, planned, experimental, considered, otherwise never-implemented, and abandoned versions.
- all 3rd party reviews, audits, or opinions of the AEC's testing procedure that were commissioned by the AEC.
- all communication with 3rd parties commissioned by the AEC for said reviews, audits, or opinions of the AEC's testing procedure.
- all documents and communications concerning the reasoning, motivation, and design goals of the membership testing process.
- all documents and communications regarding the removal of the "Random sample sizes for membership testing" table from the web page http://www.aec.gov.au/Parties_and_Representatives/party_registration/Registration_Decisions/registration-tests.htm which occurred between 2012-05-11 and 2013-07-02, as indicated by:
  - https://web.archive.org/web/20120511194720/http://www.aec.gov.au/Parties_and_Representatives/party_registration/Registration_Decisions/registration-tests.htm
  - https://web.archive.org/web/20130702172124/http://www.aec.gov.au/Parties_and_Representatives/party_registration/Registration_Decisions/registration-tests.htm#membership
- all AEC documents and internal communication regarding concerns about limiting the size of membership lists for the purpose of membership testing.
-->

* [AEC's Notice to Flux (with test results)](https://xertrov.github.io/aec-membership-test-simulator/docs/BDLPN0-aec-flux-jan-13_unencrypted.pdf)
* [Our Response](https://xertrov.github.io/aec-membership-test-simulator/docs/Response-to-AEC-rego-20220213.pdf)

From the AEC's notice (note that the AEC **refuses** membership lists with more than 1650 members):

> On 7 December 2021, the Party responded to the s 138A Notice by providing a list of
between 1,500 and 1,650 members of the Party.
>
> I am notifying you under s 137(1)(b) of the Electoral Act that the Electoral Commission is considering deregistering the Party, as the Electoral Commission is satisfied on reasonable grounds that the Party does not have at least 1,500 members. A copy of the s 137(1)(b) Notice is enclosed.

Here is an except from the first page of our response, to give you an idea of the gist:

> We have 3 arguments supporting our case. Each argument is *individually* sufficient to show
that a decision (by the AEC) to deregister the Party would not be based on reasonable
grounds; each argument is a *decisive criticism* of the current methodology.
>
> * The statistical method used fails ~10% of the time for borderline cases.
> * The statistical method uses an artificially limited sample size and thus does not estimate party membership, though does (roughly) measure membership attrition.
> * We have sufficient membership and provide evidence. **Attached is a list of 4680 members. Each entry was, at some point, verified against the electoral roll.**
>
> Unless each of these criticisms can be addressed, we do not believe that a decision by the AEC to deregister the Party would be based in reality.

(Note: there are at least two non-critical errors in our response -- the AEC has already been informed. See the end of the doc for what was sent to the AEC re those errors.)

Yesterday (2022-02-14) I was curious about the *actual* statistical properties of the AEC's process. How likely would it have been for us to succeed? (Given that we are **in fact** an eligible party.)

**Turns out there was a 71.9% chance that the AEC's method would find a false negative.**

### TL;DR: It's rigged.

In this document and the associated code and graphs: a *farce* is defined as any case where the chance of a false negative is ≥ 50%, i.e., statistical confidence is ≤ 50%.

## 4. Analysis Methodology

The code associated with this document produces statistical graphs (of the Probability Mass Function, specifically) based on 500,000 simulations of the AEC's method.

For each simulation, the number of failures is recorded as the output. Subsequently, these results are normalized to give the probability of X failures for the given input parameters.
These probabilities are then graphed, with the x-axis showing the number of failures, and the y-axis showing `P(x = X)` -- i.e., the probability of a membership test having a certain number of failures (membership denials).
As the AEC has limits on the acceptable number of membership denials based on the reduced membership list, the bars in these PMFs are colored blue or orange to indicate a pass or a failure. In cases where the party *does* meet legislative requirements, the blue bars (`P(success)`) should *always* sum to `> 0.9`. If `P(success) < 0.5`, the case is deemed a *farce* and marked as such.

The simulation is initialized with a membership list -- a list of N members where each member has a `failure_rate` chance (e.g., 0.0909) of responding "No" (i.e., a membership denial).

Each simulation proceeds thus:

1. randomly sample `sample_size` members from a party's membership list. `sample_size` is the maximum allowable by the AEC.
2. filter out `n_members_removed` members (e.g., 24 members were filtered out of Flux's most recent membership test). This is the "*reduced* membership list" mentioned above.
3. randomly sample `n_to_sample` members. `n_to_sample` is based on the AEC's published tables of sample sizes and the acceptable number of denials (these are dependant on the size of the reduced membership list).
4. count the number of failing members.

These results are compared against:

1. AEC published confidence claims
2. Reality

### Reason for this analysis method

This method is, in essence, the best that a party can do.
Perhaps they could spend a lot of time and effort contacting (and annoying) members to keep their details up to date.
However, revalidating 1650+ members against the roll takes considerable time and effort, especially when it is a manual process.
Additionally, this may not help a party avoid membership denials -- there really isn't any way for a party to know whether members will deny membership upon AEC contact, even if their details are up-to-date.
Furthermore, these sort of proactive actions can make it *more* difficult for a party to gain or maintain membership if there is an on-going griefing attack (which are impossible to detect).
Griefers *want* to be on the submitted membership list because that's how they grief.

Given that the AEC offers no feedback about which members are filtered out or which members deny membership, the best that a party can do is, essentially, randomly sample the subset of their membership list that has been validated against the electoral roll.

### Running this simulator

Tested w/ python 3.9 and 3.10. (3.8 did not work.)

Install python3 deps: `pip3 install matplotlib pandas click scipy`

For arguments, run `./main.py --help` ([source code](main.py))

To add a set of parameters, add a new line in `main.py` under the `aec()` function.
Parameters are: number of trials in the simulation, the population size of members from which the party can choose a membership list to provide, the failure rate of members confirming their membership when contacted, and the number of members that are filtered out of the list (reasons include: they support the registration of another party, they're deceased, the details cannot be matched against the electoral roll, or duplicate entries).

### Main Simulator Loop

This is the main loop of the simulation.
It has been run 500,000 times per graph unless otherwise mentioned.

```python
# take sample from full membership list (which can be more that 1650 / the AEC's limit)
# the sample size is, at most, the legislative limit (e.g., 1650)
membership_sample = r.sample(members, sample_size)

# remove n_members_removed true members (this is the worst case for the party).
#   members can be removed b/c their details couldn't be matched, they're deceased, or b/c they've supported another party's rego.
#   we always want to remove true members to measure worst case performance of methodology.
# why? because that's what happens in a griefing attack (your fake-members will be sure not to give you bad details).
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
```

## 5. Major Findings

In the case of Flux's recent membership audit, the simulation shows that -- *on the assumption that Flux is an eligible party*, and that 17% of members provided will respond "No" -- there is a 71.9% chance of the AEC reaching a *false negative* result. In such a case, overall Flux would have over 3,800 members that respond "Yes" (or do not respond). See <a href="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m4680-f796-s1649-r24-flux.png">Fig 5.1</a>.

What if we repeat the exercise? How many membership tests would be required to reach a positive result 90% of the time (i.e., 10% of the time Flux fails every test)?

| Confidence | Tests Required for 1 Success (p=0.283) |
|---|---|
| 80% | 5 |
| 90% | 7 |
| 95% | 10 |
| 99% | 14 |

So, 7 complete tests (of 1650 members randomly sampled from Flux's list of 4680) would be required to reach 1 successful test, 90% of the time.

### What happens if Flux gains more members?

Moreover, say that Flux is gaining members faster than it is losing them. ('Losing' members means that they will now answer "No" but do not revoke their membership.) It turns out that this makes the AEC's methodology *less likely to succeed.* See <a href="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m5616-f1264-s1650-r0-flux+gain20-pct-lose10-pct-.png">Fig 5.2</a>, [Example 5.2.1](https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m5616-f1264-s1650-r24-flux+gain20-pct-lose10-pct-.png), [Example 5.2.2 (Filtered=0)](https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m9360-f2354-s1650-r0-flux+gain100-pct-lose33-pct-.png), [Example 5.2.3 (Filtered=24)](https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m9360-f2354-s1650-r24-flux+gain100-pct-lose33-pct-.png).

### **The system is rigged. It's a farce.**

Finally, there are cases where the AEC's method fails even more spectacularly.

Say 50% of Flux's 4680 members submitted (as part of our objection to the AEC's consideration of involuntary deregistration) respond "No" -- the AEC's method fails 100% of the time in this case, even though Flux would exceed the legislative requirement by 1.56x. See <a href="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m4680-f2340-s1650-r0-flux+halfbadmembers.png">Fig 5.3</a>, and related: [Example 5.3.1](https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m20000-f10000-s1650-r0.png).

---

### Analysis of Flux's *actual* membership test

<p align="center">
    <img src="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m4680-f796-s1649-r24-flux.png" />
    <br>
    <em>
        <a href="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m4680-f796-s1649-r24-flux.png">Fig 5.1</a>: Even though an assumption of this simulation is that Flux is an eligible political party, the AEC's method fails 71.9% of the time. <strong>This is the real-world analysis of Flux's membership test.</strong><br>
        Note: Flux submitted 1649 members due to an off-by-one error (the spreadsheet had 1650 rows, including a row for the headings).</em>
</p>

---

### Predictive analysis if Flux's membership increases by 20% but members that will deny membership increases by 10%

<p align="center">
    <img src="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m5616-f1264-s1650-r0-flux+gain20-pct-lose10-pct-.png" />
    <br>
    <em>
        <a href="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m5616-f1264-s1650-r0-flux+gain20-pct-lose10-pct-.png">Fig 5.2</a>: This distribution shows that the AEC's validation method becomes less reliable as a party *gains* members.<br>
        <strong>Improvement makes life harder! Strength is weakness!</strong></em>
</p>

| Confidence | Tests Required for 1 Success (p=0.104) |
|---|---|
| 80% | 15 |
| 90% | 21 |
| 95% | 28 |
| 99% | 42 |

---
### Predictive analysis with a 50% denial rate

<p align="center">
    <img src="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m4680-f2340-s1650-r0-flux+halfbadmembers.png" />
    <br>
    <em>
        <a href="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m4680-f2340-s1650-r0-flux+halfbadmembers.png">Fig 5.3</a>: If we assume that Flux provides 4680 members but only 50% of them will respond "Yes" or not respond -- indicating 2340 valid members and indicating that Flux is an eligible party -- the AEC's method fails 100% of the time.</em>
</p>

| Confidence | Tests Required for 1 Success (p<0.0005) |
|---|---|
| 80% | at least 3,219 |
| 90% | at least 4,605 |
| 95% | at least 5,990 |
| 99% | at least 9,209 |

---

## 6. Suspected Farces

Detecting previous farces is difficult because the AEC does not publish the results of membership tests and, too my knowledge, does not record or ask for the number of members a party *could* offer in support of their validity.
Instead, we only know the number of members that were submitted, which is always &lt;= 1650 (or the limit in effect at the time), and we only know this when the AEC has published a statement of reasons which is only done when there is a request for review. If a party just gives up, or otherwise misses the deadline, then we don't hear about it and thus cannot evaluate whether a farce occurred.

*Note: these cases occurred prior to the September 2021 increase in required members. Therefore they are judged against the previous requirements -- the test method was practically the same, the only difference being that it was calibrated for membership lists of 500-550 instead of 1500-1650.*

Since parties sometimes *max out* the number of members they may provide, the only reasonable conclusion is that they have *more* members they *could* provide if a more responsible method were used.

Therefore, parties are assumed to have *just enough* excess capacity in additional members to be eligible, and that those extra members *could* have been provided.

### Excess Capacity Explanation

Excess capacity here refers to additional members that, if not for the AEC's limit, a party could provide -- expressed as a percentage of the limit. If a party requires 10% excess capacity, and the limit of a membership list is 1650, then that party must be capable of providing a list of 1815 members that a list of 1650 members is randomly sampled from.

For comparison: in Flux's case, we had 3030 additional members (excess capacity of 184%) -- excluding those that we could not validate. The AEC is sometimes able to validate members that we cannot, and we have at least 4285 additional members that we could contact with a request for them to update their details.

What about cases where the member list submitted had a large number of duplicates? It is not safe to assume the absence of a farce in these cases: maintaining membership lists is difficult. In my case, I wrote **thousands of lines** of custom code to assist Flux in managing our member list -- and the proportion of our list that is automatically matched against the electoral roll is proof of this. But, even with multiple checks for duplicates (matching phone numbers, emails, first and last names, etc), still we would occasionally get duplicates. These stragglers were usually found through a manual process before submission. At some point it just isn't worth worrying about. *However*, due to the ambiguity of these cases, this document will exclude them from "suspected" farces.

### The Suspected Farces

Since, in the following cases, the excess capacity of the party undergoing testing was not known, these are only *suspected* farces.

1. (Fig 6.1) [30 June 2021 -- deregistration of Child Protection Party under s 137(6)](https://aec.gov.au/Parties_and_Representatives/Party_Registration/Deregistered_parties/files/statement-of-reasons-child-protection-party-s137-deregistration.pdf) ([mirror](docs/statement-of-reasons-child-protection-party-s137-deregistration.pdf)) -- excess capacity of 13.4% required
2. (Fig 6.2) [9 March 2021 -- deregistration of Seniors United Party under s 137(6)](https://aec.gov.au/Parties_and_Representatives/Party_Registration/Deregistered_parties/files/statement-of-reasons-seniors-united-party-of-australia-s137-deregistration.pdf) ([mirror](docs/statement-of-reasons-seniors-united-party-of-australia-s137-deregistration.pdf)) -- excess capacity of 14.4% required
3. (Fig 6.3) [7 November 2013 -- refusal to register of Cheaper Petrol Party](https://www.aec.gov.au/Parties_and_Representatives/party_registration/Registration_Decisions/2013/5204.htm) ([mirror](https://web.archive.org/web/20140124195635/https://www.aec.gov.au/Parties_and_Representatives/party_registration/Registration_Decisions/2013/5204.htm)) -- excess capacity of 8.2% required
4. (Fig 6.4) [12 November 2010 -- refusal to register of Seniors Action Movement](https://www.aec.gov.au/Parties_and_Representatives/party_registration/Registration_Decisions/2010/3976.htm) ([mirror](https://web.archive.org/web/20140212151106/http://www.aec.gov.au/Parties_and_Representatives/party_registration/Registration_Decisions/2010/3976.htm)) -- excess capacity of 5.1% required
5. (Fig 6.5) [1 March 2016 -- deregistration of the Australian Democrats](https://www.aec.gov.au/Parties_and_Representatives/Party_Registration/Registration_Decisions/2016/files/statement-reasons-australian-democrats.pdf) ([mirror](https://web.archive.org/web/20170303052846/https://www.aec.gov.au/Parties_and_Representatives/Party_Registration/Registration_Decisions/2016/files/statement-reasons-australian-democrats.pdf)) -- excess capacity of 6.5% required


Note, the `@Measured` in the titles of the following graphs indicates that the failure rate is calculated directly from AEC reports of the ratio of membership denials to membership contacts.

<!--
Possible more:
- png/aec-test-sim-FARCE-N500000-m550-f42-s550-r43-aahp_measured-hypothetical.png
- VRP
- The Communists

-->

---

<p align="center">
    <img src="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m625-f125-s550-r2-cpp_measured.png" />
    <br>
    <em>
        <a href="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m625-f125-s550-r2-cpp_measured.png">Fig 6.1</a>: The deregistration of Child Protection Party on 30 June 2021 is suspected to have been a farce.</em>
</p>

| Confidence | Tests Required for 1 Success (p=0.176) |
|---|---|
| 80% | 9 |
| 90% | 12 |
| 95% | 16 |
| 99% | 24 |

---

<p align="center">
    <img src="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m629-f129-s550-r11-sup_measured.png" />
    <br>
    <em>
        <a href="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m629-f129-s550-r11-sup_measured.png">Fig 6.2</a>: The deregistration of SUP on 30 June 2021 is suspected to have been a farce.</em>
</p>

| Confidence | Tests Required for 1 Success (p=0.071) |
|---|---|
| 80% | 22 |
| 90% | 32 |
| 95% | 41 |
| 99% | 63 |

---

<p align="center">
    <img src="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m595-f95-s550-r1-cpp2013_measured.png" />
    <br>
    <em>
        <a href="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m595-f95-s550-r1-cpp2013_measured.png">Fig 6.3</a>: The refusal to register Cheaper Petrol Party on 7 November 2013 is suspected to have been a farce.</em>
</p>


| Confidence | Tests Required for 1 Success (p=0.435) |
|---|---|
| 80% | 3 |
| 90% | 5 |
| 95% | 6 |
| 99% | 9 |

---

<p align="center">
    <img src="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m578-f78-s550-r15-sam_measured.png" />
    <br>
    <em>
        <a href="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m578-f78-s550-r15-sam_measured.png">Fig 6.4</a>: The refusal to register SAM on 12 November 2010 is suspected to have been a farce.</em>
</p>

| Confidence | Tests Required for 1 Success (p=0.410) |
|---|---|
| 80% | 4 |
| 90% | 5 |
| 95% | 6 |
| 99% | 9 |

---

<p align="center">
    <img src="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m586-f86-s550-r24-fANY-democrats_2016.png" />
    <br>
    <em>
        <a href="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m586-f86-s550-r24-fANY-democrats_2016.png">Fig 6.5</a>: The affirmation of the decision to deregister of the Australian Democrats on 1 March 2016 is suspected to have been a farce. Note: this uses the AEC measured <code>P(denial)</code>, as with graphs including <code>@Measured</code>.</em>
</p>

| Confidence | Tests Required for 1 Success (p=0.237) |
|---|---|
| 80% | 6 |
| 90% | 9 |
| 95% | 12 |
| 99% | 18 |

---

### Possible Farces

These are cases where the available information regarding the membership test is incomplete, so some assumptions have had to be made.
Based on AEC measurements, if the party had some minimum number of members (such that it had at least 500 non-denying members), then these cases are farces.

1. [2017-08-09 Affirmation of refusal to register the Australian Affordable Housing Party](https://web.archive.org/web/20210125002714/https://www.aec.gov.au/Parties_and_Representatives/Party_Registration/Registration_Decisions/2017/sor-australian-affordable-housing-party.pdf) -- [Figure](png/aec-test-sim-FARCE-N500000-m542-f42-s542-r35-fANY-aahp_measured.png)
1. [2016-05-04 Set aside of decision to deregister Australian First Party](https://web.archive.org/web/20210412213513/https://aec.gov.au/Parties_and_Representatives/Party_Registration/Registration_Decisions/2016/files/statement-reasons-australia-first.pdf) -- [Figure](png/aec-test-sim-FARCE-N500000-m550-f49-s550-r38-fANY-af_2016.png) *Note: this is a farcical situation because, although the party was successful, the confidence in a true positive was only 48.8%. In essence, it was a 50/50 coin-flip.*
1. [2017-08-09 Refusal to register The Communists](https://web.archive.org/web/20210906200545/https://www.aec.gov.au/Parties_and_Representatives/party_registration/Registration_Decisions/2017/sor-the-communists.pdf) -- [Figure](png/aec-test-sim-FARCE-N500000-m708-f208-s550-r35-fANY-communists2017_measured.png)
1. [2018-08-30 Refusal to register Voter Rights Party](https://web.archive.org/web/20220115081534/https://www.aec.gov.au/parties_and_representatives/party_registration/Registration_Decisions/2018/2018-voter-rights-party-statement-of-reasons.pdf) -- [Figure](png/aec-test-sim-FARCE-N500000-m732-f232-s550-r22-fANY-vrp_measured.png)
1. [2016-08-24 Affirmation of deregistration of the Republican Party of Australia](https://web.archive.org/web/20190412211155/https://aec.gov.au/Parties_and_Representatives/Party_Registration/Registration_Decisions/2016/files/statement-reasons-rpa.pdf) -- [Figure](png/aec-test-sim-FARCE-N500000-m760-f260-s550-r20-fANY-rpa_2016.png)

## 7. Flux's 2021 Membership Test Assuming a Threshold (9.09%) Denial Rate (including worst-case)

Flux is a party that has -- with regards to membership lists -- excess capacity; if filtered members could be replaced, we could provide them.
Note that filtered members are never replaced in the AEC's method.

Given this, combined with the artificial limit on sample size, what are the true confidence values for the AEC's test?

As it turns out, it depends on the quality of Flux's membership list. We have a high-quality list -- thanks to a lot of management code written to help with that -- but many parties do not have the skills or resources to do that.

Fig 7.1 shows that, for Flux's recent membership test, the true confidence of the AEC's method -- *assuming that Flux's members have `P(denial) = 0.0909`* -- was **89.0%**; which is lower than the 90% confidence interval that's been advertised in the past. That means that the results of the AEC's test would find Flux ineligible 11% of the time.

Additionally, Fig 7.2 and 7.3 show that, as the number of members filtered out increases, confidence drops -- a lot.

`@Thresh` in these titles indicates a 9.09% denial rate (which is not what was measured during Flux's recent membership test). 9.09% = 150 / 1650.

`+F__` indicates that the number in place of `__` is the number of members that were filtered out (e.g., duplicates, deceased members, etc).

---

<p align="center">
    <img src="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-N500000-m4680-f425-s1649-r24-flux_thresh.png" />
    <br>
    <em>
        <a href="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-N500000-m4680-f425-s1649-r24-flux_thresh.png">Fig 7.1</a>: Assuming that 91.9% of the members (randomly sampled from the full list) on Flux's 2021 membership test will not deny membership when contacted (1500/1650): 500,000 simulations of Flux's membership test show that it has a confidence of 89.0% (i.e., false negative rate of 11.0%), which is less than the AEC's <a href="https://web.archive.org/web/20120511194720/http://www.aec.gov.au/Parties_and_Representatives/party_registration/Registration_Decisions/registration-tests.htm">previously advertised</a> 90% confidence.</em>
</p>

| Confidence | Tests Required for 1 Success (p=0.890) |
|---|---|
| 80% | 1 |
| 90% | 2 |
| 95% | 2 |
| 99% | 3 |

---

<p align="center">
    <img src="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m4680-f425-s1649-r99-flux_thresh+f99.png" />
    <br>
    <em>
        <a href="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m4680-f425-s1649-r99-flux_thresh+f99.png">Fig 7.2</a>: Assuming that 91.9% of the members on Flux's  2021 membership test members will not deny membership when contacted (1500/1650), and that 99 members were filtered out instead of 24: 500,000 simulations show that it has a confidence of 49.2%, <strong>which would constitute a farce.</strong> With a membership list of this quality, 4 membership tests would be required for 90% confidence of 1 success.</em>
</p>

| Confidence | Tests Required for 1 Success (p=0.492) |
|---|---|
| 80% | 3 |
| 90% | 4 |
| 95% | 5 |
| 99% | 7 |

---

<p align="center">
    <img src="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m4680-f425-s1649-r149-flux_thresh+f149.png" />
    <br>
    <em>
        <a href="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m4680-f425-s1649-r149-flux_thresh+f149.png">Fig 7.3</a>: Assuming that 91.9% of the members on Flux's  2021 membership test members will not deny membership when contacted (1500/1650), and that a worst-case 149 members were filtered out instead of 24: 500,000 simulations show that it has a confidence of just 15.1%, <strong>which would constitute a farce.</strong> With a membership list of this quality, <strong>15 membership tests would be required for 90% confidence of 1 success.</strong></em>
</p>

| Confidence | Tests Required for 1 Success (p=0.151) |
|---|---|
| 80% | 10 |
| 90% | 15 |
| 95% | 19 |
| 99% | 29 |

---

<!-- aec-test-sim-N500000-m1650-f150-s1650-r50-1650_thresh+f50 -->

<!--
# other cases

- TNL 2021, confidence: 86.6% - png/aec-test-sim-N500000-m550-f30-s550-r27-fANY-tnl_2021.png

-->

## 8. Feedback Loops Between AEC Policy and Party Behavior

To my knowledge, parties typically don't try to build membership to many thousands of members. That's because it's expensive, time consuming, and difficult to manage. Most importantly -- **there's no point when it comes to registration**.

The fact that the AEC has imposed this flawed method for years means that non-parliamentary parties' common practices are based around meeting the AEC's policies. When the limit was 550 (and 500 members required), there literally was no point building beyond that because it *would not help you* in registering or maintaining registration -- it was largely wasted effort.

<!-- **The AEC must acknowledge that, due to its poor judgement, it has impacted the operations and dynamics of political parties in a way that violates its responsibility of neutrality.** -->

Additionally, the AEC's policies have entrenched these common practices which enabled the political elite to change the legislative requirements **suddenly and dramatically** -- effectively eliminate competition. *The AEC is complicit.*

If *the previous status quo was 550 members due to the AEC* promulgating a culture of not going beyond this, and then *parliament decides to radically change the limit* (there is no reason they could not have done this gradually over, say, 10 years with a small bump each year), *at what point do we acknowledge that something is rotten?*

The AEC is on record about why it imposes a limit on membership lists used for verification:

> &emsp; 26. In respect of the assertion in the application for review that the AEC failed to test the lists provided by the Party on 12 June 2017 (which contained 650 members) and on 20 August 2017 (which contained 739 members), the Commission notes that the ‘Party Registration Guide’ requests that parties provide a list of between 500 to 550 members. This is considered to be to a party’s advantage, by minimising the work required of the party in confirming the enrolment status and contact details of additional other members.

Source: <https://www.aec.gov.au/Parties_and_Representatives/Party_Registration/Registration_Decisions/2018/2018-commonwealth-of-australia-party-statement-of-reasons.pdf> ([mirror](https://web.archive.org/web/20190403114018/https://www.aec.gov.au/Parties_and_Representatives/Party_Registration/Registration_Decisions/2018/2018-commonwealth-of-australia-party-statement-of-reasons.pdf))

*Note: this case cannot be analyzed as the AEC neglected to include any results of membership tests.*

How about the AEC stop making decisions on behalf of parties?
Especially when those decisions have been *proven* (by this document) to have systemically disadvantaged non-parliamentary parties, to have decreased the true confidence of the AEC membership test, to be based on falsehoods, and, ultimately, to be a reflection of a condescension and hubris that has no place *running a democracy*.

## 9. Conclusion

With the AEC's existing policies, and on the assumption that Flux is a valid party, it is only reasonable to conclude that Flux will find it increasingly difficult to remain registered and pass registration tests, even if it grows in membership. That is to say: the process has a predetermined outcome, and is an empty act done for show. *It is rigged, and a farce.*

With currently measured values (based on AEC results), it would take (on average) 7 repeated trials for Flux to have 1 successful membership test. So this is not a problem that can be solved by repeating the membership test.

At least 5 past cases have been identified with farcical properties -- they are *suspected* farces -- and at least 5 additional cases have incomplete information but may be farcical.

That is: in these cases the AEC's test had a confidence of less than 50% provided that those parties had additional members (which the party would have been prevented from submitting only due to AEC policy).
All 5 suspected cases required less than 15% additional members -- i.e., the membership test was a farce for all cases if N ≥ 630. *Note that all 5 cases predate the September 2021 change to membership requirements; at the time the required number of members was 500.*

**It has thus been found that the AEC's method is rigged and a farce, and that there is sufficient evidence to back this up.**

<!-- don't really need this next bit. does it really help? -->

<!--
## Appendix: Some State ECs are Worse

The Electoral Commissions of both NSW and Victoria have verification methods that are **deliberately** designed to **prevent** valid parties from registering -- or, at the very least, the methods are dishonestly defended.

Here is an example from Flux's attempt to register in Victoria.
This is what happens if you volunteer to play by their rules.

There's no author attributed to this excerpt from [Electoral Regulation Research Network newsletter - April 2019](https://law.unimelb.edu.au/__data/assets/pdf_file/0015/3052014/ERRN-newsletter-April-2019-final.pdf) (perhaps they knew they were being dishonest, though I doubt it).

> VCAT decided on an application to review a decision of the Victorian Electoral Commission (VEC) to refuse to register The Flux Party – Victoria as a political party.
>
> [...]
>
> In her Order, made on 23 October 2018, Justice Hampel, Vice President of VCAT, refuted every one of Mr Millington’s arguments.

[Source material (VCAT Judgement)](https://www.austlii.edu.au/cgi-bin/viewdoc/au/cases/vic/VCAT/2018/1661.html?context=1;query=Millington%20v%20Victorian%20Electoral%20Commission;mask_path=)

Here's a sample of such a "refutation":

> [...] This submission is equally flawed. An argument based on probabilities is unsound.
>
> ---
>
> <p align="right"><a href="https://www.austlii.edu.au/cgi-bin/viewdoc/au/cases/vic/VCAT/2018/1661.html?context=1;query=Millington%20v%20Victorian%20Electoral%20Commission;mask_path=">Her Honour Judge Hampel, Vice President VCAT</a></p>

I wonder what she thinks **beyond reasonable doubt** means, and what she thought the VEC's argument (in support of its determination) was based on.

It is clear that Hampel has literally no understanding of statistics or probabilities.

Perhaps, if she had a high-school level understanding of probability theory, then she would know about the binomial theorem and maybe gain a small intuition for how wrong she is.

As a witness in this case, my evidence was dismissed because I did not work as a statistician.
No effort was made to enquire into the method.
That's the sort of piss-poor thinking that leads to problems the AEC's method being used.

Say you wanted to verify my account of the case?
How would you verify the record of the tribunal?
You can't -- it's not public. Tough.

To be clear: I do not think the VEC or VCAT broke the law at any point.
I do think they are heavily biased towards the status quo, though.
I do not think they are honest with themselves regarding these biases.

I'm sure Hampel is a very nice person and does lots of nice things.
It does not change the fact that she is unable to tell the boundaries of her own incompetence. -->

## Appendix: Definitions


**rigged** *adjective*

[Wiktionary](https://en.wiktionary.org/wiki/rigged)
> - Pre-arranged and fixed so that the winner or outcome is decided in advance.

[Urban Dictionary](https://www.urbandictionary.com/define.php?term=rigged)
> -  The word rigged is used to describe situations where unfair advantages are given to one side of a conflict.

*Note: Urban Dictionary is included here as Cambridge and Merriam-Webster didn't seem to have specific definitions for the adjective.*

---

**rig** *verb*

(Note: *rigging* is the gerundive of *rig*)

[Cambridge Dictionary](https://dictionary.cambridge.org/dictionary/english/rig)
> - to arrange an event or amount in a dishonest way
> - to dishonestly influence or change something in order to get the result that you want

[Wiktionary](https://en.wiktionary.org/wiki/rig#Verb)
> - To manipulate something dishonestly for personal gain or discriminatory purposes.

---

**farce** *noun*

[Cambridge Dictionary](https://dictionary.cambridge.org/dictionary/english/farce)
> - a situation that is very badly organized or unfair
> - a ridiculous situation or event, or something considered a waste of time

[Wiktionary](https://en.wiktionary.org/wiki/farce)
> - A situation abounding with ludicrous incidents.
> - A ridiculous or empty show.

[Merriam-Webster](https://www.merriam-webster.com/dictionary/farce)
> - an empty or patently ridiculous act, proceeding, or situation

<!--

## Appendix: CAP 2018

### Some Dishonesty from the AEC

>  26. In respect of the assertion in the application for review that the AEC failed to test the lists provided by the Party on 12 June 2017 (which contained 650 members) and on 20 August 2017 (which contained 739 members), the Commission notes that the ‘Party Registration Guide’ requests that parties provide a list of between 500 to 550 members. This is considered to be to a party’s advantage, by minimising the work required of the party in confirming the enrolment status and contact details of additional other members.

Source <https://www.aec.gov.au/Parties_and_Representatives/Party_Registration/Registration_Decisions/2018/2018-commonwealth-of-australia-party-statement-of-reasons.pdf>

Note: this was in 2018. I strongly disagreed then, and I ofc still do now.

### "a lie"

> 24. In respect of the assertion in the application for review that the results of the membership testing conducted by the AEC was a "false and misleading statement [a lie]”, the Commission is satisfied that the methodology developed by the ABS, which was correctly applied in this case, is consistent with the Electoral Act and provides the AEC with a statistical degree of certainty about a party’s number of members.
> 25. Accordingly, the Commission rejects the assertion that the membership testing conducted by the AEC was a “false and misleading statement [a lie]”,

<https://www.aec.gov.au/Parties_and_Representatives/Party_Registration/Registration_Decisions/2018/2018-commonwealth-of-australia-party-statement-of-reasons.pdf>

> [...] the Commission is satisfied that the methodology developed by the ABS [...]

It should never have been, and the ABS should never have put it forward.

It **is** dishonest (or at least incompetent) of the ABS to claim that that the method provides a "statistical degree of certainty about a party’s number of members".

It is *irresponsible* of the AEC to wilfully turn a blind eye to criticisms of their methodology (have they ever had a 3rd party review? FOI).

> [...] and provides the AEC with a statistical degree of certainty about a party’s number of members [...]

This is false, as proven by this document.

-->

## Appendix: AEC Membership Testing Tables

Note: the first column of these tables ("Members lodged", "Eligible membership") is the reduced membership list after filtering out e.g., duplicates, members supporting the registration of other parties, deceased members, etc.

It is ["AEC Policy"](https://web.archive.org/web/20140220005415/http://aec.gov.au/Parties_and_Representatives/Party_Registration/Registration_Decisions/registration-tests.htm) that lists are no more than 1.1x the legislative limit (e.g., a maximum of 550 prior to September 2021, and 1650 after September 2021). That is: lists with more members than this are rejected.

### September 2021 to February 2022

Source: Page 24 of <https://web.archive.org/web/20220206003633/https://www.aec.gov.au/Parties_and_Representatives/Party_Registration/guide/files/party-registration-guide.pdf>

| Members lodged | Random sample size | Maximum denials to pass |
|---|---|---|
| 1,500 | 18 | 0 |
| 1,506 | 27 | 1 |
| 1,523 | 33 | 2 |
| 1,543 | 38 | 3 |
| 1,562 | 42 | 4 |
| 1,582 | 46 | 5 |
| 1,599 | 50 | 6 |
| 1,616 | 53 | 7 |
| 1,633 | 57 | 8 |
| 1,647 | 60 | 9 |
| 1,650 | 60 | 9 |

### Circa 2017 to September 2021

Sources:
* Page 26 of <https://web.archive.org/web/20210409193623/https://aec.gov.au/Parties_and_Representatives/Party_Registration/guide/files/party-registration-guide.pdf>
* <https://web.archive.org/web/20200320074933/https://www.aec.gov.au/Parties_and_Representatives/Party_Registration/files/party-registration-guide.pdf>


| Members lodged | Random Sample | Max Denials to Pass |
|---|---|---|
| 500 | 18 | 0 |
| 503 | 26 | 1 |
| 511 | 32 | 2 |
| 519 | 37 | 3 |
| 526 | 41 | 4 |
| 534 | 44 | 5 |
| 541 | 47 | 6 |
| 548 | 50 | 7 |
| 550 | 50 | 7 |

### Circa 2012 to 2016

Sources:
* Page 33 of <https://web.archive.org/web/20160314113418/http://aec.gov.au/Parties_and_Representatives/Party_Registration/files/party-registration-guide.pdf>
* Page 32 of <https://web.archive.org/web/20140212032435/http://www.aec.gov.au/Parties_and_Representatives/Party_Registration/files/party-registration-guide.pdf> (Note: this source includes risk columns)
* <https://web.archive.org/web/20130208013723/http://aec.gov.au/Parties_and_Representatives/party_registration/guide/forms.htm#table> (Note: this source includes risk columns)
* <https://web.archive.org/web/20120425182026/http://www.aec.gov.au/Parties_and_Representatives/party_registration/guide/forms.htm> (Note: this source includes risk columns)

| Members lodged | Random Sample | Max Denials to Pass | accepting only 400 – risk % | rejecting 500 – risk % |
|---|---|---| ---|--- |
| 500 | 18 | 0 | 1.80 | 0.00 |
| 503 | 26 | 1 | 1.99 | 1.05 |
| 512 | 30 | 2 | 2.64 | 3.26 |
| 521 | 34 | 3 | 2.86 | 4.68 |
| 529 | 38 | 3 | 2.85 | 5.52 |
| 537 | 42 | 5 | 2.60 | 6.65 |
| 543 | 46 | 6 | 2.43 | 6.86 |
| 548 | 50 | 7 | 2.27 | 6.78 |
| 550 | 50 | 7 | 2.07 | 8.05 |

### Circa 2011

Source: <https://web.archive.org/web/20110220143705/http://www.aec.gov.au/Parties_and_Representatives/Party_Registration/Registration_Decisions/registration-tests.htm>

> The table below is an extract from a table based on a formula provided by the Australian Bureau of Statistics, giving approximately a 10% risk of refusing a party which has 500 members and a 2% risk of registering a party with only 400 members.

| Eligible membership | Size of random sample | Denials permitted | Confirmations required |
|---|---|---|---|
| 500 | 18 | 0 | 18 |
| 505 | 21 | 1 | 20 |
| 515 | 26 | 2 | 24 |
| 520 | 29 | 2 | 27 |
| 525 | 32 | 3 | 29 |
| 530 | 35 | 4 | 31 |
| 535 | 37 | 4 | 33 |
| 540 | 40 | 5 | 35 |
| 545 | 43 | 5 | 38 |
| 550 | 47 | 6 | 41 |

## Appendix: Errors in Feb 13 response to AEC


<blockquote>
<p>
First, in the section "The AEC’s membership test methodology artificially reduces sample size":
</p>

<blockquote>
Keep in mind that – given this experimental setup – we’d expect 9 or more failures 10% of
the time. If we were doing this experiment in real life, 10% of the time we would
underestimate the number of cars by a factor of more than 2500x.
</blockquote>

<p>
This is a typo -- we'd expect 8 or more failures 10% of the time, and 9 or more failures ~5% of the time.
</p>

<p>
Second, in the section "Closing remarks":
</p>

<blockquote>
Consider a soon-to-be-registered party with 1650 valid members (assume this is true). What
happens if 200 malicious members join (prior to registration), with the sole purpose of
preventing that party from registering? Then, it’s expected that ~10.8% of the membership
list provided to the AEC as part of their registration application are these malicious members.
Thus the failure rate according to the AEC’s methodology is expected to exceed the current
threshold (set by the AEC) – the AEC would conclude that the party does not meet
requirements.
</blockquote>

<p>
The italicized part is not correct. The AEC's method is much better than this -- it only fails 10% to 20% of the time (the above quote implies that the method fails more than 50% of the time). The exact false negative rate depends on the number of members filtered by the AEC, similar to how our December 2021 list of 1649 names had 24 entries filtered. The AEC's method is more reliable when fewer names are filtered, with the 20% false negative rate corresponding to 25 members filtered out. (0 names filtered corresponds to a 10% false negative rate.)
</p>

<p>
It is worth pointing out that there are similar (though slightly more extreme) parameters that do result in a >50% failure rate of the AEC's method. For example a party of 2000 members, 300 of which are malicious, and 15 names filtered has a failure rate of 50.4%.
</p>
</blockquote>

Note, there are some other errors too, like the method mentioned in the *The AEC’s membership test methodology artificially reduces sample size* section uses the random sampling size that was used in Flux's test, but it probably should have been 60 instead of 53. Not really a big deal.


<!--
Math symbols:
≤
≥
±
 -->
