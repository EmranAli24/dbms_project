import argparse
import os
import re
import pandas as pd
from collections import defaultdict


def snake_case(s):
    # Lowercase, replace spaces and special chars with underscores, remove double underscores
    s = s.strip().lower()
    s = re.sub(r'[\s\-\/\.]+', '_', s)
    s = re.sub(r'[^a-z0-9_]', '', s)
    return re.sub(r'_+', '_', s).strip('_')


def deduplicate_columns(columns):
    """Ensures unique column names by appending .1, .2, etc where needed (like pandas does)"""
    seen = defaultdict(int)
    new_cols = []
    for col in columns:
        base = col
        while col in new_cols:
            seen[base] += 1
            col = f"{base}.{seen[base]}"
        new_cols.append(col)
    return new_cols


def load_and_clean(input_file):
    df = pd.read_csv(input_file, dtype=str, keep_default_na=False)
    # Standardize column names
    cleaned_cols = [snake_case(col) for col in df.columns]
    cleaned_cols = deduplicate_columns(cleaned_cols)
    df.columns = cleaned_cols

    # Remove fully empty rows (all blank)
    df = df.dropna(how='all')
    # Forward-fill context columns (for continuation rows) 
    context_cols = []
    # Heuristic: columns that are not repeating groups (appear only once)
    col_counts = defaultdict(int)
    for c in cleaned_cols:
        base = c.split('.')[0]
        col_counts[base] += 1
    for c in cleaned_cols:
        base = c.split('.')[0]
        if col_counts[base] == 1:
            context_cols.append(c)
    # Forward fill only context columns
    if context_cols:
        df[context_cols] = df[context_cols].replace('', pd.NA).ffill()
    # Strip whitespace from all cells
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    return df


def main():
    parser = argparse.ArgumentParser(
        description="Domain-agnostic data cleaning and 1NF transformer.")
    parser.add_argument('--input_file', required=True,
                        help='Path to raw noisy CSV input file')
    parser.add_argument('--output_file', required=True,
                        help='Path to write cleaned 1NF CSV')
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output_file), exist_ok=True)
    print(f"Loading: {args.input_file}")
    df = load_and_clean(args.input_file)
    print(f"Cleaned shape: {df.shape}")
    df.to_csv(args.output_file, index=False)
    print(f"Saved cleaned file: {args.output_file}")


if __name__ == "__main__":
    main()
