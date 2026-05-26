#!/usr/bin/env python3
"""PA3 tester for sudoku_solver.py."""

from __future__ import annotations

import argparse
import ast
import importlib.util
import sys
from pathlib import Path


def load_module(path: Path, root: Path):
    sys.path.insert(0, str(root))
    spec = importlib.util.spec_from_file_location('submission_sudoku_solver', path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f'Could not load module from {path}')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fixture_paths(root: Path) -> list[Path]:
    return sorted((root / 'tests' / 'fixtures').glob('*.txt'))


def split_fixture(text: str) -> tuple[list[list[int]], bool]:
    marker = '=== EXPECTED ==='
    if marker not in text:
        raise ValueError('Fixture missing === EXPECTED ===')
    left, right = text.split(marker, 1)
    grid = ast.literal_eval(left.replace('=== INPUT ===', '').strip())
    expected = right.strip().lower()
    if expected not in {'solvable: true', 'solvable: false'}:
        raise ValueError('Expected section must be `solvable: true|false`')
    return grid, expected.endswith('true')


def run_case(module, fixture_path: Path) -> tuple[bool, str, object]:
    grid, want_solvable = split_fixture(fixture_path.read_text(encoding='utf-8'))
    result = module.solve([row[:] for row in grid])
    got_solvable = result is not None

    if got_solvable != want_solvable:
        return False, f'expected solvable={want_solvable}, got solvable={got_solvable}', result

    return True, 'PASS', result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--solution',
        default='sudoku_solver.py',
        help='Path to solution file relative to PA3 root',
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    fixtures = fixture_paths(root)
    total = len(fixtures)
    solution_path = (root / args.solution).resolve()
    if not solution_path.exists():
        print(f'TOTAL: 0/{total}')
        print(f'  - Solution file not found: {solution_path}')
        sys.exit(1)

    try:
        module = load_module(solution_path, root)
    except Exception as exc:
        print(f'TOTAL: 0/{total}')
        print(f'  - Could not import solution: {exc}')
        sys.exit(1)

    earned = 0
    issues = []
    for i, fixture_path in enumerate(fixtures, start=1):
        label = fixture_path.stem.replace('case_', '')
        ok, msg, result = run_case(module, fixture_path)
        if ok:
            earned += 1
            print(f'FIXTURE_{i} ({label}): 1/1 [PASS]')
        else:
            print(f'FIXTURE_{i} ({label}): 0/1 [FAIL]')
            issues.append(f'{label}: {msg}')
        print(f'  RESULT: {result!r}')

    for issue in issues:
        print(f'  - {issue}')
    print(f'TOTAL: {earned}/{total}')

    if earned < total:
        sys.exit(1)


if __name__ == '__main__':
    main()