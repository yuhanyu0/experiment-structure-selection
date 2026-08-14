# Frozen Methods Summary

## Problem

MESA-2 starts from a finite mechanism version space whose members exactly match the initial coarse evidence. It asks what *kind* of experiment must become richer to reduce uncertainty on held future programs.

The three controlled source families are:

- `ONE_STEP_SUFFICIENT`: a richer one-step final-state measurement is sufficient;
- `COMPOSITION_REQUIRED`: all one-step states are aliased and a multistep intervention word is required;
- `READOUT_REQUIRED`: additional depth is unnecessary, but a richer one-step microgeometry observation is required.

## Experiment grammar

A candidate physical experiment unit is

```text
(context, intervention word, multivariate observation bundle)
```

with an incremental physical cost. One observation bundle is purchased per physical program, so intervention cost is charged once rather than once per scalar coordinate.

## Selection score

For candidate experiment `e`, the frozen policy computes posterior-predictive covariance across currently surviving mechanism candidates after development-only scaling and block-noise whitening:

```text
g_e = Cov_w[mu_e(M)]
```

and scores the candidate by

```text
0.5 * log det(I + g_e) / incremental physical cost
```

The hidden target parameter and hidden target Jacobian are not used to rank candidates. The target outcome is revealed only after selection as the exact target mean under the declared block-Gaussian likelihood.

## Search / evaluation separation

Search uses three contexts and a frozen subset of depth-1-to-3 words. Evaluation uses two disjoint contexts and disjoint depth-3/4 word families. Build validation records both context and word-family disjointness as passed.

## Policies

- `FULL`: adaptive complete grammar;
- `DEPTH1`: adaptive one-step-only grammar;
- `FINAL_STATE_ONLY`: all depths but only the final-state observation bundle;
- `FIXED`: development-frozen non-adaptive set;
- `RANDOM_MEDIAN`: median of 32 frozen random policies per family/seed.

Development seeds are `1000–1007`. Sealed Final seeds are `2000–2007`; build validation records that the Final seeds were absent during construction.

## Final decision object

The primary structural readout is the first selected physical program in each family, complemented by held-program uncertainty comparisons under exact one-sided sign tests. The final audit requires all registered structural and baseline gates to pass before the formal decision is issued.
