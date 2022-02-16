# AEC Party Membership Test Methodology is Rigged! A Statistical Analysis of AEC Methodology and Graphs (of PMFs)

<p align="center">
    <a href="https://xertrov.github.io/aec-membership-test-simulator/">Website</a>
    |
    <a href="https://github.com/XertroV/aec-membership-test-simulator">Source Code</a>
    <br><br>
    <em>Max Kaye</em> (Philosopher)<br>
    2022-02-15
</p>

In Australia, to register a political party you need a minimum number of members.
Federally, that's *usually* 1500 (as of September 2021) -- the Australian Electoral Commission (AEC) will conduct membership tests to verify this minimum.
Political parties *with* a parliamentarian have no minimum membership limit and are not tested.
Political parties *without* a parliamentarian must go through a membership test when they register, and then once every election cycle thereafter.

This document evaluates the AEC's testing methodology for particular cases and finds that there are real-world situations where the testing methodology has a false negative (improper failure) rate over 50%, and often much higher.

Therefore, it is reasonable to conclude, for those cases: the methodology is *rigged* and a *farce*.

**Note: I am not accusing the AEC of doing the rigging; just proving that the method *is* rigged.**

To date, there is 1 known incident of a farce and *at least* 4 suspected incidents.
<!-- There may be many more as the results of most membership tests are not available.
(An FOI request may solve this.) -->

Additionally, experimental evidence shows that the confidence of Flux's 2021 membership test was 89.0%, which is less than the limit [previously advertised (90%)](https://web.archive.org/web/20120511194720/http://www.aec.gov.au/Parties_and_Representatives/party_registration/Registration_Decisions/registration-tests.htm).

The AEC's claim that their membership tests are conducted to a confidence of 90% are proven false. In actual fact, for a party that is capable of providing a list of 1,650 members wherein exactly 1,500 members will not deny membership (and 150 will): experimental evidence proves that the worst-case confidence of the AEC's membership test is just 15.1%, indicating a false negative rate of 84.9%. This is an indication of gross negligence or gross incompetence, or both.

## 1. Background Context

Recently (leading up to September 2021), parliamentarians (i.e., the 4 major parties) decided there was just too much competition! That would not do. So, a bunch of changes were made to the Electoral Act. Changes designed to make life harder for anyone who wanted to be part of our democracy, but did not want to participate in the rotten, tribalist, political cults that run the show. Some of those changes resulted in (as of Feb 2022) the pending deregistration of 12 parties, and the very real deregistration of 9 parties. In practice that is ~40% of parties, gone before the next election. Political elites will claim that this culling, and the subsequent entrenchment of the status quo, is a good thing. That it is making our democracy better. Just wait and watch.

## 2. Regular Membership Testing

Every few years, the Australian Electoral Commission (AEC) will check that each political party has enough members according to the legislative requirement. The party must provide a list of 1500 to 1650 names (inclusive) to use as evidence of their eligibility. The AEC will then filter out some names (duplicates, deceased members, etc). That produces a NEW list of <= 1650 names. Then, the AEC will do a statistical sampling of members and will use that to determine whether a party is eligible. Particularly, a small subset of members are selected and contacted, asking for a yes/no confirmation of membership. Non-responses are skipped. A "No" answer counts as a failure -- this is a *membership denial*. In this document and associated code: "failure rate" refers to the rate at which members respond "No".

The AEC does not accept lists larger than 1650; there is no chance for a party to replace any of those filtered members; that filtering process increases the chance of false negatives (when list length is limited + excluding duplicates); parties are not told which members were filtered (even those which are deceased) so they cannot be proactively removed; and, finally, the standard of statistical evaluation is to assume that the list of 1650 members were *the only members* of the party. Zero consideration is given beyond this (outside the chance to respond). How many parties have been wrongly denied registration? Nobody knows.

[The method is detailed on pages 23 and 24 of "Guide for registering a
party".](https://www.aec.gov.au/Parties_and_Representatives/Party_Registration/guide/files/party-registration-guide.pdf)
([mirror](https://xertrov.github.io/aec-membership-test-simulator/docs/party-registration-guide.pdf))

## 3. Flux's 2021 Membership Test -- A Known Farce

Flux failed its recent membership test. The only problem? We have at least 4680 members whose details have been matched against the electoral roll. It is the AEC's imposition of 1650 members maximum that is the problem.

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

* [AEC's Notice to Flux (with results)](https://xertrov.github.io/aec-membership-test-simulator/docs/BDLPN0-aec-flux-jan-13_unencrypted.pdf)
* [Our Response](https://xertrov.github.io/aec-membership-test-simulator/docs/Response-to-AEC-rego-20220213.pdf)

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

Turns out there was a ~72% chance that the AEC's method would find a false negative.

### TL;DR: It's rigged.

In this document and the associated code and graphs: a *farce* is defined as any case where the chance of a false negative is >= 50%.

## 4. Running this simulator

Tested w/ python 3.9 and 3.10. (3.8 did not work.)

Install python3 deps: `pip3 install matplotlib pandas click`

For arguments, run `./main.py --help`

To add a set of parameters, add a new line in `main.py` under the `aec()` function.
Parameters are: number of trials in the simulation, the population size of members from which the party can choose a membership list to provide, the failure rate of members confirming their membership when contacted, and the number of members that are filtered out of the list (reasons include: they support the registration of another party, they're deceased, the details cannot be matched against the electoral roll, or duplicate entries).

## 5. Major Findings

In the case of Flux's recent membership audit, the simulation shows that -- *on the assumption that Flux is an eligible party*, and that 17% of members provided will respond "No" -- there is a ~72% chance of the AEC reaching a *false negative* result. In such a case, overall Flux would have over 3,800 members that respond "Yes" (or do not respond). See <a href="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m4680-f796-s1649-r24-flux.png">Fig 1</a>.

What if we repeat the exercise? How many membership tests would be required to reach a positive result 90% of the time (i.e., 10% of the time Flux fails every test)?

| Confidence | Tests Required for 1 Success (p=0.283) |
|---|---|
| 80% | 5 |
| 90% | 7 |
| 95% | 10 |
| 99% | 14 |

So, 7 complete tests (of 1650 members randomly sampled from Flux's list of 4680) would be required to reach 1 successful test, 90% of the time.

### What happens if Flux gains more members?

Moreover, say that Flux is gaining members faster than it is losing them. ('Losing' members means that they will now answer "No" but do not revoke their membership.) It turns out that this makes the AEC's methodology *less likely to succeed.* See <a href="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m5616-f1264-s1650-r0-flux+gain20%lose10%.png">Fig 2</a>, [Example 2.1](https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m5616-f1264-s1650-r24-flux+gain20%lose10%.png), [Example 2.2 (Filtered=0)](https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m9360-f2354-s1650-r0-flux+gain100%lose33%.png), [Example 2.3 (Filtered=24)](https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m9360-f2354-s1650-r24-flux+gain100%lose33%.png).

### **The system is rigged. It's a farce.**

Finally, there are even more cases where the AEC's method fails spectacularly.

Say 50% of Flux's 4680 members submitted (as part of our objection to the AEC's consideration of involuntary deregistration) respond "No" -- the AEC's method fails 100% of the time in this case, even though Flux would exceed the legislative requirement by 1.56x. See <a href="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m4680-f2340-s1650-r0-flux+halfbadmembers.png">Fig 3</a>, and related: [Example 3.1](https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m20000-f10000-s1650-r0.png).

---

<p align="center">
    <img src="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m4680-f796-s1649-r24-flux.png" />
    <br>
    <em>
        <a href="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m4680-f796-s1649-r24-flux.png">Fig 1</a>: Even though an assumption of this simulation is that Flux is an eligible political party, the AEC's method fails ~72% of the time.</em>
</p>

---

<p align="center">
    <img src="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m5616-f1264-s1650-r0-flux+gain20%25lose10%25.png" />
    <br>
    <em>
        <a href="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m5616-f1264-s1650-r0-flux+gain20%lose10%.png">Fig 2</a>: This distribution shows that the AEC's validation method becomes less reliable as a party *gains* members.<br><strong>Improvement makes life harder! Strength is weakness!</strong></em>
</p>

| Confidence | Tests Required for 1 Success (p=0.104) |
|---|---|
| 80% | 15 |
| 90% | 21 |
| 95% | 28 |
| 99% | 42 |

---

<p align="center">
    <img src="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m4680-f2340-s1650-r0-flux+halfbadmembers.png" />
    <br>
    <em>
        <a href="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m4680-f2340-s1650-r0-flux+halfbadmembers.png">Fig 3</a>: If we assume that Flux provides 4680 members but only 50% of them will respond "Yes" or not respond -- indicating 2340 valid members and indicating that Flux is an eligible party -- the AEC's method fails 100% of the time.</em>
</p>

| Confidence | Tests Required for 1 Success (p=0.0005) |
|---|---|
| 80% | 3,219 |
| 90% | 4,605 |
| 95% | 5,990 |
| 99% | 9,209 |

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

What about cases where the member list submitted had a large number of duplicates? It is not safe to assume the absence of a farce in these cases: maintaining membership lists is difficult. In my case, I wrote **thousands of lines** of custom code to assist Flux in managing our member list -- and the proportion of our list that is automatically matched against the electoral roll is proof of this. But, even with multiple checks for duplicates (matching phone numbers, emails, first and last names, etc), still we would occasionally get duplicates. These stragglers were usually found through a manual process before submission. At some point it just isn't worth worrying about. *However*, due to the ambiguity of these cases (there is only 1 case I know of), this document will exclude them.

### The Suspected Farces

Since, in the following cases, the excess capacity of the party undergoing testing was not known, these are only *suspected* farces.

1. (Fig 4) [30 June 2021 -- deregistration of Child Protection Party under s 137(6)](https://aec.gov.au/Parties_and_Representatives/Party_Registration/Deregistered_parties/files/statement-of-reasons-child-protection-party-s137-deregistration.pdf) ([mirror](docs/statement-of-reasons-child-protection-party-s137-deregistration.pdf)) -- excess capacity of 13.4% required
2. (Fig 5) [9 March 2021 -- deregistration of Seniors United Party under s 137(6)](https://aec.gov.au/Parties_and_Representatives/Party_Registration/Deregistered_parties/files/statement-of-reasons-seniors-united-party-of-australia-s137-deregistration.pdf) ([mirror](docs/statement-of-reasons-seniors-united-party-of-australia-s137-deregistration.pdf)) -- excess capacity of 14.4% required
3. (Fig 6) [7 November 2013 -- refusal to register of Cheaper Petrol Party](https://www.aec.gov.au/Parties_and_Representatives/party_registration/Registration_Decisions/2013/5204.htm) ([mirror](https://web.archive.org/web/20140124195635/https://www.aec.gov.au/Parties_and_Representatives/party_registration/Registration_Decisions/2013/5204.htm)) -- excess capacity of 8.2% required
4. (Fig 7) [12 November 2010 -- refusal to register of Seniors United Party](https://www.aec.gov.au/Parties_and_Representatives/party_registration/Registration_Decisions/2010/3976.htm) ([mirror](https://web.archive.org/web/20140212151106/http://www.aec.gov.au/Parties_and_Representatives/party_registration/Registration_Decisions/2010/3976.htm)) -- excess capacity of 5.1% required

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
        <a href="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m625-f125-s550-r2-cpp_measured.png">Fig 4</a>: The deregistration of Child Protection Party on 30 June 2021 is suspected to have been a farce.</em>
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
        <a href="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m629-f129-s550-r11-sup_measured.png">Fig 5</a>: The deregistration of SUP on 30 June 2021 is suspected to have been a farce.</em>
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
        <a href="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m595-f95-s550-r1-cpp2013_measured.png">Fig 6</a>: The refusal to register Cheaper Petrol Party on 7 November 2013 is suspected to have been a farce.</em>
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
        <a href="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m578-f78-s550-r15-sam_measured.png">Fig 7</a>: The refusal to register SAM on 12 November 2010 is suspected to have been a farce.</em>
</p>

| Confidence | Tests Required for 1 Success (p=0.410) |
|---|---|
| 80% | 4 |
| 90% | 5 |
| 95% | 6 |
| 99% | 9 |

---

## 7. Flux's 2021 Membership Test

<p align="center">
    <img src="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m578-f78-s550-r15-sam_measured.png" />
    <br>
    <em>
        <a href="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m578-f78-s550-r15-sam_measured.png">Fig 7.1</a>: Assuming that 91.9% of the members on Flux's  2021 membership test members will not deny membership when contacted (1500/1650): 500,000 simulations of Flux's membership test show that it has a confidence of 89.0%, which is less than the AEC's [previously advertised](https://web.archive.org/web/20120511194720/http://www.aec.gov.au/Parties_and_Representatives/party_registration/Registration_Decisions/registration-tests.htm) 90%.</em>
</p>

| Confidence | Tests Required for 1 Success (p=0.890) |
|---|---|
| 80% | 4 |
| 90% | 5 |
| 95% | 6 |
| 99% | 9 |

<!-- aec-test-sim-N500000-m1650-f150-s1650-r50-1650_thresh+f50 -->

<!-- ## Potential Farces -->

<!--
## Feedback Between AEC Policy and Party Behavior
-->





<!-- don't really need this bit. does it really help? -->

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

---

**rig** *verb*

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
