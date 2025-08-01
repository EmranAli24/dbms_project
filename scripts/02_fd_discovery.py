import argparse
import os
import pandas as pd
import json
from itertools import combinations, chain
from collections import defaultdict


def is_fd(df, lhs, rhs):
    """Check if lhs -> rhs holds in the DataFrame (no data loss)."""
    # For each group of LHS values, check if RHS is always the same
    grouped = df.groupby(list(lhs))[rhs].nunique(dropna=False)
    return (grouped <= 1).all()


def powerset(iterable, max_size=None):
    "powerset([A,B,C], max_size=2) --> (A,) (B,) (C,) (A,B) (A,C) (B,C)"
    s = list(iterable)
    for r in range(1, (max_size or len(s))+1):
        for combo in combinations(s, r):
            yield combo


def find_minimal_fds(df, max_lhs_size=2, sample_size=None, verbose=False):
    """
    Find minimal (non-redundant, nontrivial) FDs up to max_lhs_size.
    Returns a list of (lhs_tuple, rhs_col).
    """
    if sample_size is not None and sample_size < len(df):
        df = df.sample(sample_size, random_state=42)
    columns = list(df.columns)
    all_fds = []
    already_found = defaultdict(set)  # rhs -> set of minimal LHSs

    for rhs in columns:
        candidates = [c for c in columns if c != rhs]
        minimal_lhs = []
        for sz in range(1, max_lhs_size+1):
            for lhs in combinations(candidates, sz):
                # Skip if a subset of lhs already determines rhs
                skip = False
                for k in range(1, len(lhs)):
                    for sub in combinations(lhs, k):
                        if sub in already_found[rhs]:
                            skip = True
                            break
                    if skip:
                        break
                if skip:
                    continue
                if is_fd(df, lhs, rhs):
                    # Only add if no subset already found
                    all_fds.append((lhs, rhs))
                    already_found[rhs].add(lhs)
                    if verbose:
                        print(f"Found FD: {lhs} -> {rhs}")
    # Remove trivial FDs (A → A)
    all_fds = [fd for fd in all_fds if fd[1] not in fd[0]]
    return all_fds


def group_fds(fds):
    groups = defaultdict(list)
    for lhs, rhs in fds:
        groups[lhs].append(rhs)
    return groups


def main():
    parser = argparse.ArgumentParser(
        description=" FD discovery  (canonical cover, minimal and nontrivial).")
    parser.add_argument('--input_file', required=True,
                        help='Path to cleaned 1NF CSV')
    parser.add_argument('--output_file', required=True,
                        help='Path to output JSON of discovered FDs')
    parser.add_argument('--max_lhs_size', type=int, default=2,
                        help='Maximum size of LHS to search for FDs')
    parser.add_argument('--sample_size', type=int, default=None,
                        help='Rows to sample for FD discovery (None=all)')
    parser.add_argument('--verbose', action='store_true',
                        help='Print each FD as found')
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output_file), exist_ok=True)
    df = pd.read_csv(args.input_file, dtype=str, keep_default_na=False)
    print(
        f"Loaded: {args.input_file} ({df.shape[0]} rows, {df.shape[1]} columns)")

    print(f"Discovering minimal FDs (max LHS size={args.max_lhs_size})...")
    fds = find_minimal_fds(df, max_lhs_size=args.max_lhs_size,
                           sample_size=args.sample_size, verbose=args.verbose)
    print(f"Found {len(fds)} minimal, nontrivial FDs.")

    grouped = group_fds(fds)
    serializable = {",".join(lhs): rhs_list for lhs,
                    rhs_list in grouped.items()}
    with open(args.output_file, 'w') as f:
        json.dump(serializable, f, indent=2)
    print(f"FDs (canonical cover) saved to {args.output_file}.")

    # Print summary
    print("\nSample minimal FD groups:")
    for i, (lhs, rhs_list) in enumerate(serializable.items()):
        print(f"  {lhs} -> {', '.join(rhs_list)}")
        if i >= 4:
            break


if __name__ == "__main__":
    main()
