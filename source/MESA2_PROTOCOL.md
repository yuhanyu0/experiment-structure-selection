# MESA-2 Protocol

**MESA-2 — Information-Geometric Mechanism-Equivalence Experiment Synthesis**

MESA-2 tests whether an evidence-conditioned, cost-aware experiment synthesizer
can recover the appropriate experiment structure in three controlled cases:

- `ONE_STEP_SUFFICIENT`: a richer one-step final-state measurement is enough.
- `COMPOSITION_REQUIRED`: all one-step states are aliased; a multistep program is needed.
- `READOUT_REQUIRED`: extra depth is unnecessary; a richer one-step microgeometry readout is needed.

The policy sees a finite ensemble of mechanisms that exactly match the initial
coarse evidence. For each candidate physical experiment unit

`(context, intervention word, multivariate observation bundle)`

it computes the posterior predictive covariance after development-only scaling
and block-noise whitening:

`g_e = Cov_w[mu_e(M)]`

and selects

`0.5 * log det(I + g_e) / incremental physical cost`.

The hidden target parameter and its Jacobian are not used to score candidates.
The target result is revealed only after an experiment is selected, as the exact
target mean under the declared block-Gaussian likelihood.

Search uses three contexts and a frozen subset of depth-1-to-3 words. Evaluation
uses two disjoint contexts and disjoint depth-3/4 word families. One observation
bundle is purchased per physical program, so intervention cost is charged once.

Primary policies:

- `FULL`: adaptive complete grammar.
- `DEPTH1`: adaptive one-step-only grammar.
- `FINAL_STATE_ONLY`: all depths, final-state bundle only.
- `FIXED`: development-frozen non-adaptive set.
- `RANDOM_MEDIAN`: median of 32 frozen random policies per seed.

Development seeds are 1000–1007. Sealed Final seeds are 2000–2007.

A pass licenses only a synthetic controlled-method claim. It does not establish
global minimality, natural mechanism identification, a universal grammar, or
literature novelty.
