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

Therefore, it is reasonable to conclude, for those cases, that the methodology is *rigged* and a *farce*.

**Note: I am not accusing the AEC of doing the rigging; just proving that the method *is* rigged.**

To date, there is 1 known incident of a farce and *at least* 2 suspected incidents.
<!-- There may be many more as the results of most membership tests are not available.
(An FOI request may solve this.) -->

## Background Context

Recently (leading up to September 2021), parliamentarians (i.e., the 4 major parties) decided there was just too much competition! That would not do. So, a bunch of changes were made to the Electoral Act. Changes designed to make life harder for anyone who wanted to be part of our democracy, but did not want to participate in the rotten, tribalist, political cults that run the show. Some of those changes resulted in (as of Feb 2022) the pending deregistration of 12 parties, and the very real deregistration of 9 parties. In practice that is ~40% of parties, gone before the next election. Political elites will claim that this culling, and the subsequent entrenchment of the status quo, is a good thing. That it is making our democracy better. Just wait and watch.

## Regular Membership Testing

Every few years, the Australian Electoral Commission (AEC) will check that each political party has enough members according to the legislative requirement. The party must provide a list of 1500 to 1650 names (inclusive) to use as evidence of their eligibility. The AEC will then filter out some names (duplicates, deceased members, etc). That produces a NEW list of <= 1650 names. Then, the AEC will do a statistical sampling of members and will use that to determine whether a party is eligible. Particularly, a small subset of members are selected and contacted, asking for a yes/no confirmation of membership. Non-responses are skipped. A "No" answer counts as a failure -- this is a *membership denial*. In this document and associated code: "failure rate" refers to the rate at which members respond "No".

The AEC does not accept lists larger than 1650; there is no chance for a party to replace any of those filtered members; that filtering process increases the chance of false negatives (when list length is limited + excluding duplicates); parties are not told which members were filtered (even those which are deceased) so they cannot be proactively removed; and, finally, the standard of statistical evaluation is to assume that the list of 1650 members were *the only members* of the party. Zero consideration is given beyond this (outside the chance to respond). How many parties have been wrongly denied registration? Nobody knows.

[The method is detailed on pages 23 and 24 of "Guide for registering a
party".](https://www.aec.gov.au/Parties_and_Representatives/Party_Registration/guide/files/party-registration-guide.pdf)
([mirror](https://xertrov.github.io/aec-membership-test-simulator/docs/party-registration-guide.pdf))

## Flux's 2021 Membership Test -- A Known Farce

Flux failed its recent membership test. The only problem? We have at least 4680 members whose details have been matched against the electoral roll. It is the AEC's imposition of 1650 members maximum that is the problem.

<!--
FOI:
- all documents and communications regarding both policy changes and decisions that concern the upper limit of acceptable membership lists.
- all documents and communications regarding minimising the work of registering parties as relating to the upper limit of acceptable membership lists. example of mention: <https://www.aec.gov.au/Parties_and_Representatives/Party_Registration/Registration_Decisions/2018/2018-commonwealth-of-australia-party-statement-of-reasons.pdf>
  > This is considered to be to a party’s advantage, by minimising the work required of the party in confirming the enrolment status and contact details of additional other members
- all documents and communications regarding what is and is not in a party's advantage and/or disadvantage in relation to registration procedures and/or membership testing.
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

## TL;DR: It's rigged.

In this document and the associated code and graphs: a *farce* is defined as any case where the chance of a false negative is >= 50%.

----

## Running this simulator

Tested w/ python 3.9 and 3.10. (3.8 did not work.)

Install python3 deps: `pip3 install matplotlib pandas click`

For arguments, run `./main.py --help`

To add a set of parameters, add a new line in `main.py` under the `aec()` function.
Parameters are: number of trials in the simulation, the population size of members from which the party can choose a membership list to provide, the failure rate of members confirming their membership when contacted, and the number of members that are filtered out of the list (reasons include: they support the registration of another party, they're deceased, the details cannot be matched against the electoral roll, or duplicate entries).

## Major Findings

In the case of Flux's recent membership audit, the simulation shows that -- *on the assumption that Flux is an eligible party*, and that 17% of members provided will respond "No" -- there is a ~72% chance of the AEC reaching a *false negative* result. In such a case, overall Flux would have over 3,800 members that respond "Yes" (or do not respond). See <a href="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m4680-f796-s1649-r24-flux.png">Fig 1</a>.

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

---

<p align="center">
    <img src="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m4680-f2340-s1650-r0-flux+halfbadmembers.png" />
    <br>
    <em>
        <a href="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m4680-f2340-s1650-r0-flux+halfbadmembers.png">Fig 3</a>: If we assume that Flux provides 4680 members but only 50% of them will respond "Yes" or not respond -- indicating 2340 valid members and indicating that Flux is an eligible party -- the AEC's method fails 100% of the time.</em>
</p>

---

## Suspected Farces

Detecting previous farces is difficult because the AEC does not record the number of members a party *could* offer in support of their validity.
Instead, we only know the number of members that were submitted, which is always &lt;= 1650.

*Note: these cases occurred prior to the September 2021 increase in required members. Therefore they are judged against the previous requirements -- the test method was practically the same, the only difference being that it was calibrated for membership lists of 500-550 instead of 1500-1650.*

Since parties sometimes *max out* the number of members they may provide, the only reasonable conclusion is that they have *more* members they *could* provide if a more responsible method were used.

Therefore, parties are assumed to have *just enough* excess capacity in additional members to be eligible, and that those extra members *could* have been provided.

For comparison: in Flux's case, we had 3030 additional members (excess capacity of 184%) -- excluding those that we could not validate. The AEC is sometimes able to validate members that we cannot, and we have at least 4285 additional members that we could contact with a request for them to update their details.

What about cases where the member list submitted had a large number of duplicates? It is not safe to assume the absence of a farce in these cases: maintaining membership lists is difficult. In my case, I wrote **thousands of lines** of custom code to assist Flux in managing our member list -- and the proportion of our list that is automatically matched against the electoral roll is proof of this. But, even with multiple checks for duplicates (matching phone numbers, emails, first and last names, etc), still we would occasionally get duplicates. These stragglers were usually found through a manual process before submission. At some point it just isn't worth worrying about. *However*, due to the ambiguity of these cases (there is only 1 case I know of), this document will exclude them.

The two cases are:

1. (Fig 4) [30 June 2021 -- deregistration of Child Protection Party under s 137(6)](https://aec.gov.au/Parties_and_Representatives/Party_Registration/Deregistered_parties/files/statement-of-reasons-child-protection-party-s137-deregistration.pdf) ([mirror](docs/statement-of-reasons-child-protection-party-s137-deregistration.pdf)) -- excess capacity of 13.4% required
2. (Fig 5) [9 March 2021 -- deregistration of Seniors United Party under s 137(6)](https://aec.gov.au/Parties_and_Representatives/Party_Registration/Deregistered_parties/files/statement-of-reasons-seniors-united-party-of-australia-s137-deregistration.pdf) ([mirror](docs/statement-of-reasons-seniors-united-party-of-australia-s137-deregistration.pdf)) -- excess capacity of 14.4% required

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
        <a href="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m625-f125-s550-r2-cpp_measured.png">Fig 4</a>: The deregistration of CPP on 30 June 2021 is suspected to have been a farce.</em>
</p>

---

<p align="center">
    <img src="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m629-f129-s550-r11-sup_measured.png" />
    <br>
    <em>
        <a href="https://xertrov.github.io/aec-membership-test-simulator/png/aec-test-sim-FARCE-N500000-m629-f129-s550-r11-sup_measured.png">Fig 5</a>: The deregistration of SUP on 30 June 2021 is suspected to have been a farce.</em>
</p>

---


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


**rig** *verb*

[Cambridge Dictionary](https://dictionary.cambridge.org/dictionary/english/rig)
> - to arrange an event or amount in a dishonest way
> - to dishonestly influence or change something in order to get the result that you want

[Wiktionary](https://en.wiktionary.org/wiki/rig#Verb)
> - To manipulate something dishonestly for personal gain or discriminatory purposes.

---

**rigged** *adjective*

[Wiktionary](https://en.wiktionary.org/wiki/rigged)
> - Pre-arranged and fixed so that the winner or outcome is decided in advance.

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
