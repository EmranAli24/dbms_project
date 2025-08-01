import argparse
import os
import json
import pandas as pd


def load_json(path):
    with open(path) as f:
        return json.load(f)


def make_3nf_relations(fds):
    """For each FD in canonical cover, make a relation (LHS ∪ RHS)."""
    relations = []
    for lhs_str, rhses in fds.items():
        lhs = set(lhs_str.split(','))
        attrs = set(lhs)
        attrs.update(rhses)
        relations.append(attrs)
    return relations


def ensure_key_in_relations(relations, candidate_keys):
    """Add a relation for the first candidate key if no relation contains a key."""
    key_covered = False
    for key in candidate_keys:
        key_set = set(key)
        if any(key_set.issubset(rel) for rel in relations):
            key_covered = True
            break
    if not key_covered and candidate_keys:
        relations.append(set(candidate_keys[0]))
    return relations


def remove_redundant_relations(relations):
    """Remove subset and duplicate relations."""
    # Remove duplicate relations
    unique_relations = []
    for rel in relations:
        if rel not in unique_relations:
            unique_relations.append(rel)
    # Remove subset relations
    output = []
    for i, rel in enumerate(unique_relations):
        is_subset = False
        for j, other in enumerate(unique_relations):
            if i != j and rel < other:
                is_subset = True
                break
        if not is_subset:
            output.append(rel)
    return output


def project_to_relation(df, attrs):
    """Project dataframe to given attributes, dropping duplicate rows."""
    cols = [col for col in df.columns if col in attrs]
    return df[cols].drop_duplicates()


def main():
    parser = argparse.ArgumentParser(
        description="3NF decomposition with strict redundancy removal.")
    parser.add_argument('--input_file', required=True)
    parser.add_argument('--fd_file', required=True)
    parser.add_argument('--keys_file', required=True)
    parser.add_argument('--out_dir', required=True)
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    df = pd.read_csv(args.input_file, dtype=str, keep_default_na=False)
    fds = load_json(args.fd_file)
    keys_nf = load_json(args.keys_file)
    candidate_keys = keys_nf["candidate_keys"]

    # 1. Make relations from canonical FDs
    relations = make_3nf_relations(fds)
    # 2. Ensure every candidate key is in some relation
    relations = ensure_key_in_relations(relations, candidate_keys)
    # 3. Remove redundant relations strictly
    relations = remove_redundant_relations(relations)

    # 4. Output each relation as a CSV
    rel_list = []
    for i, attrs in enumerate(relations):
        rel_name = f"table_{i+1}"
        rel_path = os.path.join(args.out_dir, f"{rel_name}.csv")
        tdf = project_to_relation(df, attrs)
        tdf.to_csv(rel_path, index=False)
        rel_list.append({
            "table": rel_name,
            "attributes": sorted(attrs),
            "num_rows": len(tdf),
            "csv": rel_path
        })
        print(f"Saved {rel_name}: {len(tdf)} rows, {len(attrs)} columns.")

    # 5. Output a summary JSON
    summary = {
        "relations": rel_list,
        "candidate_keys": candidate_keys
    }
    with open(os.path.join(args.out_dir, "3nf_decomposition_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print("3NF decomposition summary saved.")


if __name__ == "__main__":
    main()
