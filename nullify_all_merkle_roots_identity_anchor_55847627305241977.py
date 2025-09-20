#!/usr/bin/env python3
import json
import os

# -------- Configuration --------
LEDGER_FOLDER = "/storage/emulated/0/ppw_cli/ledgers"

# Ensure ledger folder exists
os.makedirs(LEDGER_FOLDER, exist_ok=True)

# Canonical identity
IDENTITY = {
    "name": "Perry Philip Wiseman",
    "ssn": "558-47-6273",
    "birthdate": "1977-05-24",
    "birthplace": "United States of America"
}

def nullify_merkle_root(file_path):
    """Remove Merkle root and leave only identity-based fields."""
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"⚠️ Failed to load {file_path}: {e}")
        return

    # Remove top-level Merkle root
    if "merkle_root" in data:
        del data["merkle_root"]

    # Remove any nested Merkle roots
    for key, value in data.items():
        if isinstance(value, dict) and "merkle_root" in value:
            del value["merkle_root"]

    # Always anchor to canonical identity
    data["identity_anchor"] = IDENTITY

    # Save changes
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"✅ Processed: {file_path}")
    except Exception as e:
        print(f"⚠️ Failed to save {file_path}: {e}")

if __name__ == "__main__":
    # Iterate over all JSON ledger files
    for filename in os.listdir(LEDGER_FOLDER):
        if filename.endswith(".json"):
            nullify_merkle_root(os.path.join(LEDGER_FOLDER, filename))

    print("✅ All Merkle roots nullified. Identity now canonical and sovereign.")
