# Reproducibility Boundary

## What this public artifact reproduces

The v0.1 checkout deterministically verifies:

- the SHA-256 hashes of the redistributed frozen source artifacts;
- repository manifest integrity;
- the formal Final decision label;
- all frozen Final gate booleans;
- the exact initial-alias ceiling reported by the independent audit;
- the 8/8 first-program structure pattern in all three controlled families;
- the registered held-program baseline comparison counts and exact one-sided sign-test p-values used in the public summary;
- the claim ceiling and explicit limitations.

Run:

```bash
python scripts/validate_artifact.py
```

## What this public artifact does not reproduce

This checkout does not redistribute the original sealed MESA-2 runner or the full raw Final output ZIP. Their frozen hashes are recorded in `SOURCE_ARTIFACTS.json`:

- runner-code composite SHA-256: `aa8ca42b1dbae1aee113da984a512a5b7e1c66eaa7adff6d005f264d7ff3ecc7`;
- Development ZIP SHA-256: `dea50eed012a2620ebb74ff55d3e6a8a6b6daf89b6ae44016540d029c9b450a6`;
- Final ZIP SHA-256: `3cfe91830e72ae3dead4edb6ecdbd9d7befdbe779f77082e767628a58e425c25`.

Therefore v0.1 is an **audit-level frozen-result artifact**, not a clean-room one-command regeneration of every synthetic trajectory and adaptive selection step.

## Why the boundary is explicit

A reproducibility claim should not silently exceed the redistributed material. The original independent Final audit reports return code 0, a passing ZIP CRC, all ten Final-manifest entries passing, a completed execution marker, and the frozen runner/development hashes. Those facts are preserved here without pretending the sealed execution package is present in Git history.
