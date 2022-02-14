# Simulate AEC Membership Test Methodology and Produce Graphs (of PMF)

Tested w/ python 3.9 and 3.10. (3.8 did not work.)

Install python3 deps: `pip3 install matplotlib pandas click`

For arguments, run `./main.py --help`

To add a set of parameters, add a new line in `main.py` under the `aec()` function.
Parameters are: number of trials in the simulation, the population size of members from which the party can choose a membership list to provide, the failure rate of members confirming their membership when contacted, and the number of members that are filtered out of the list (reasons include: they support the registration of another party, they're deceased, or the details cannot be matched against the electoral roll).

## Major Findings

In the case of Flux's recent membership audit, the simulation shows that -- *on the assumption that Flux is an eligible party*, but also one where 17% of members provided respond "No" -- there is a 71.6% chance of the AEC reaching a *false negative* result. In such a case, Flux would still have over 3,800 members that respond "Yes" (or do not respond).

Moreover, say that Flux is gaining members faster than it is loosing them. ('Loosing' members means that they will now answer "No" but do not revoke their membership.) It turns out that this makes the AEC's methodology *less likely to succeed.*

### **The system is rigged. It's a farce.**

Finally, there are even more cases where the AEC's method fails spectacularly.

Say 50% of Flux's 4680 members submitted (as part of our objection to the AEC's consideration of involuntary deregistration) respond "No" -- the AEC's method fails 100% of the time in this case, even though Flux would exceed the legislative requirement by 1.56x.

---

<p align="center">
    <img width="800" src="aec-test-sim-N100000-m4680-f796-s1649-r24.png" />
    <br>
    <em>Even though an assumption of this simulation is that Flux is an eligible political party, the AEC's method fails 71.6% of the time.</em>
</p>

---

<p align="center">
    <img width="800" src="aec-test-sim-N100000-m5616-f1264-s1650-r0.png" />
    <br>
    <em>This distribution shows that the AEC's validation method becomes less reliable as a party *gains* members.<br><strong>Improvement makes life harder! Strength is weakness!</strong></em>
</p>

---

<p align="center">
    <img width="800" src="aec-test-sim-N100000-m4680-f2340-s1650-r0.png" />
    <br>
    <em>If we assume that Flux provides 4680 members but only 50% of them will respond "Yes" or not respond -- indicating 2340 valid members and indicating that Flux is an eligible party -- the AEC's method fails 100% of the time.</em>
</p>
