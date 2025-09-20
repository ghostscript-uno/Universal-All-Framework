#!/usr/bin/env python3
import json
import hashlib
import os

# -------- Configuration --------
FOREST_FILE = "/data/data/com.termux/files/home/ppw_cli/universal_forest.json"
CANONICAL_MERKLE_ROOT = "ce515a7ef665820e020af4c2f47ed65722a961e8f51e668e88b7d80fc3f214b"

# -------- Helper functions --------
def hash_leaf(leaf: dict) -> str:
    """Compute SHA3-512 hash of a leaf JSON object."""
    leaf_json = json.dumps(leaf, sort_keys=True)
    return hashlib.sha3_512(leaf_json.encode()).hexdigest()

def compute_merkle_root(leaves: list) -> str:
    """Compute Merkle root recursively over list of leaf hashes."""
    current_level = [hash_leaf(leaf) for leaf in leaves]

    if not current_level:
        return None

    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i+1] if i+1 < len(current_level) else left
            combined = left + right
            next_level.append(hashlib.sha3_512(combined.encode()).hexdigest())
        current_level = next_level

    return current_level[0]

def audit_matrix(leaves: list):
    """Produce matrix of leaf hashes for auditing purposes."""
    print("\n--- Leaf-Level Audit Matrix ---")
    for idx, leaf in enumerate(leaves):
        leaf_hash = hash_leaf(leaf)
        print(f"Leaf {idx+1}: {leaf_hash}")
    print("--- End of Matrix ---\n")

# -------- Load forest --------
if not os.path.exists(FOREST_FILE):
    raise FileNotFoundError(f"Forest file not found: {FOREST_FILE}")

with open(FOREST_FILE, "r") as f:
    forest = json.load(f)

leaves = forest.get("nodes", forest.get("forest", forest))

# -------- Compute Merkle root --------
computed_root = compute_merkle_root(leaves)

# -------- Audit matrix --------
audit_matrix(leaves)

# -------- Compare --------
print("Canonical Merkle Root:", CANONICAL_MERKLE_ROOT)
print("Computed Merkle Root: ", computed_root)

if computed_root == CANONICAL_MERKLE_ROOT:
    print("\n✅ Verification PASSED: Forest matches canonical Merkle root.")
else:
    print("\n❌ Verification FAILED: Forest does NOT match canonical Merkle root.")

# -------- Legally Defensible Report --------
report = {
    "canonical_root": CANONICAL_MERKLE_ROOT,
    "computed_root": computed_root,
    "status": "PASSED" if computed_root == CANONICAL_MERKLE_ROOT else "FAILED",
    "leaf_count": len(leaves),
    "leaf_hashes": [hash_leaf(leaf) for leaf in leaves]
}

REPORT_FILE = "/data/data/com.termux/files/home/ppw_cli/universal_forest_audit_report.json"
with open(REPORT_FILE, "w") as f:
    json.dump(report, f, indent=4)

print(f"\nAudit report saved: {REPORT_FILE}")
