#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fail(msg: str) -> None:
    raise AssertionError(msg)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    required = [
        'README.md','CLAIM_BOUNDARY.md','METHODS.md','LITERATURE_BOUNDARY.md',
        'REPRODUCIBILITY.md','LICENSE_DECISION.md','CITATION.cff','SOURCE_ARTIFACTS.json',
        'MANIFEST.json','figures/overview.svg','results/final_independent_audit.json',
        'results/frozen_summary.json','source/MESA2_PROTOCOL.md','source/MESA2_FINAL_CLAIM_CARD.md',
        'source/MESA2_BUILD_VALIDATION.json','source/MESA2_ENGINEERING_HISTORY.md'
    ]
    for rel in required:
        if not (ROOT/rel).is_file():
            fail(f'missing required file: {rel}')

    audit = json.loads((ROOT/'results/final_independent_audit.json').read_text())
    summary = json.loads((ROOT/'results/frozen_summary.json').read_text())
    sources = json.loads((ROOT/'SOURCE_ARTIFACTS.json').read_text())

    if audit['formal_decision'] != 'PASS_MESA2_GEOMETRY_SELECTS_EXPERIMENT_STRUCTURE':
        fail('formal decision drift')
    if not audit['final_gates']['all_pass'] or not all(audit['final_gates'].values()):
        fail('Final gates are not all PASS')
    if audit['initial_alias_maximum'] > 1e-12:
        fail('initial alias no longer exact at declared tolerance')

    expected = {
        'ONE_STEP_SUFFICIENT': ({'1': 8}, {'final_state': 8}),
        'COMPOSITION_REQUIRED': ({'3': 8}, {'final_state': 8}),
        'READOUT_REQUIRED': ({'1': 8}, {'microshape': 8}),
    }
    for family, (depths, bundles) in expected.items():
        row = audit['first_program_patterns'][family]
        if row['depth_counts'] != depths or row['bundle_counts'] != bundles:
            fail(f'first-program pattern drift: {family}')

    comps = {(x['family'], x['right']): x for x in audit['method_comparisons']}
    key_checks = {
        ('COMPOSITION_REQUIRED','DEPTH1'): (8, 0.00390625),
        ('COMPOSITION_REQUIRED','RANDOM_MEDIAN'): (8, 0.00390625),
        ('READOUT_REQUIRED','FINAL_STATE_ONLY'): (8, 0.00390625),
        ('ONE_STEP_SUFFICIENT','FINAL_STATE_ONLY'): (2, 0.96484375),
    }
    for key, (wins, p) in key_checks.items():
        got = comps[key]
        if got['wins'] != wins or abs(got['exact_one_sided_sign_p'] - p) > 1e-15:
            fail(f'comparison drift: {key}')

    if summary['formal_decision'] != audit['formal_decision']:
        fail('curated summary decision mismatch')
    flags = summary['interpretation_flags']
    if not flags['synthetic_controlled_method_result']:
        fail('synthetic scope flag lost')
    for k in ['global_minimality_established','natural_mechanism_identification_established','universal_grammar_established','literature_novelty_established','external_transfer_run']:
        if flags[k]:
            fail(f'overclaim flag became true: {k}')

    locked = sources['locked_but_not_redistributed']
    if locked['runner_code_composite_sha256'] != 'aa8ca42b1dbae1aee113da984a512a5b7e1c66eaa7adff6d005f264d7ff3ecc7':
        fail('runner hash drift')
    if locked['development_zip_sha256'] != 'dea50eed012a2620ebb74ff55d3e6a8a6b6daf89b6ae44016540d029c9b450a6':
        fail('development hash drift')
    if locked['final_zip_sha256'] != '3cfe91830e72ae3dead4edb6ecdbd9d7befdbe779f77082e767628a58e425c25':
        fail('final hash drift')

    for name, meta in sources['redistributed_frozen_files'].items():
        path = ROOT / ('results' if name == 'final_independent_audit.json' else 'source') / name
        if path.stat().st_size != meta['bytes'] or sha256(path) != meta['sha256']:
            fail(f'frozen source integrity failed: {name}')

    readme = (ROOT/'README.md').read_text()
    forbidden = ['globally minimal physical experiment', 'literature novelty is established']
    # The first phrase is permitted only as a negation in README; require the explicit negation context.
    if 'not a claim that a machine invented a globally minimal physical experiment' not in readme:
        fail('README global-minimality boundary missing')
    if 'literature novelty' not in readme.lower():
        fail('README literature boundary missing')

    manifest = json.loads((ROOT/'MANIFEST.json').read_text())
    for rel, meta in manifest['files'].items():
        path = ROOT/rel
        if not path.is_file():
            fail(f'manifest file missing: {rel}')
        if path.stat().st_size != meta['bytes'] or sha256(path) != meta['sha256']:
            fail(f'manifest integrity failed: {rel}')

    print('PASS: MESA-2 public artifact validation')
    print('decision:', audit['formal_decision'])
    print('initial_alias_maximum:', audit['initial_alias_maximum'])
    print('families:', ', '.join(expected))
    print('manifest_files:', len(manifest['files']))

if __name__ == '__main__':
    main()
