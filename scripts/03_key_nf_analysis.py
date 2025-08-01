
import argparse
import os
import json
import pandas as pd
from itertools import combinations


def load_known_keys(path):
    """Optional: Load known/likely keys (one per line, comma-separated attributes)."""
    if not path or not os.path.exists(path):
        return []
    with open(path) as f:
        return [tuple(line.strip().split(',')) for line in f if line.strip()]


def attribute_closure(attrs, fds, memo=None):
    """Compute closure of a set of attributes under given FDs (with memoization)."""
    attrs = frozenset(attrs)
    if memo is not None and attrs in memo:
        return memo[attrs]
    closure = set(attrs)
    changed = True
    while changed:
        changed = False
        for lhs, rhses in fds.items():
            lhs_set = set(lhs.split(','))
            if lhs_set.issubset(closure):
                for rhs in rhses:
                    if rhs not in closure:
                        closure.add(rhs)
                        changed = True
    if memo is not None:
        memo[attrs] = closure
    return closure


def find_candidate_keys(attributes, fds, max_key_size=3, known_keys=None):
    """Find minimal candidate keys up to max_key_size, using closure and early pruning."""
    all_attrs = set(attributes)
    keys = []
    memo = {}
    # Step 1: Check known keys first
    if known_keys:
        for key in known_keys:
            closure = attribute_closure(key, fds, memo)
            if closure == all_attrs and not any(set(k).issubset(key) for k in keys):
                keys.append(tuple(key))
    # Step 2: Brute force small subsets (if no known key or to find others)
    for r in range(1, min(max_key_size, len(attributes)) + 1):
        for subset in combinations(attributes, r):
            subset_set = set(subset)
            # Minimality: skip if superset of existing key
            if any(set(k).issubset(subset_set) for k in keys):
                continue
            closure = attribute_closure(subset_set, fds, memo)
            if closure == all_attrs:
                keys.append(subset)
    return keys


def nf_analysis(attributes, candidate_keys, fds):
    """Strict 2NF and 3NF violation analysis using all candidate keys."""
    # Prime attributes: any attribute that appears in any candidate key
    prime_attributes = set()
    for key in candidate_keys:
        prime_attributes.update(key)

    violations_2nf = []
    violations_3nf = []
    all_keys = [set(k) for k in candidate_keys]

    for lhs_str, rhses in fds.items():
        lhs = set(lhs_str.split(','))
        for rhs in rhses:
            # 2NF: partial dependency (proper subset of any CK → non-prime)
            for ck in all_keys:
                if lhs < ck and rhs not in prime_attributes:
                    violations_2nf.append((lhs_str, rhs))
            # 3NF:
            # - LHS is not a superkey (does not contain any CK)
            # - RHS is not a prime attribute
            if not any(lhs.issuperset(ck) for ck in all_keys) and rhs not in prime_attributes:
                violations_3nf.append((lhs_str, rhs))
    return violations_2nf, violations_3nf


def main():
    parser = argparse.ArgumentParser(
        description="Efficient real-world key discovery and 2NF/3NF analysis.")
    parser.add_argument('--input_file', required=True)
    parser.add_argument('--fd_file', required=True)
    parser.add_argument('--output_file', required=True)
    parser.add_argument('--max_key_size', type=int, default=3,
                        help='Max candidate key size to check (default=3)')
    parser.add_argument('--known_keys', type=str, default=None,
                        help='Optional: path to file with known keys, one per line')
    args = parser.parse_args()

    df = pd.read_csv(args.input_file, dtype=str, keep_default_na=False)
    with open(args.fd_file) as f:
        fds = json.load(f)

    attributes = list(df.columns)
    known_keys = load_known_keys(args.known_keys)
    keys = find_candidate_keys(
        attributes, fds, max_key_size=args.max_key_size, known_keys=known_keys)
    violations_2nf, violations_3nf = nf_analysis(attributes, keys, fds)

    result = {
        "attributes": attributes,
        "candidate_keys": [list(k) for k in keys],
        "violations_2nf": violations_2nf,
        "violations_3nf": violations_3nf,
    }
    os.makedirs(os.path.dirname(args.output_file), exist_ok=True)
    with open(args.output_file, "w") as f:
        json.dump(result, f, indent=2)

    print("Candidate Keys:")
    for k in keys:
        print("  - " + ", ".join(k))
    print(f"2NF Violations: {len(violations_2nf)}")
    print(f"3NF Violations: {len(violations_3nf)}")
    print(f"Saved analysis to {args.output_file}")


if __name__ == "__main__":
    main()
