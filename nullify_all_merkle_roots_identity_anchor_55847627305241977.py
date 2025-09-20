#!/usr/bin/env python3
import json
import os

# Folder containing all "worldwide" bank/ledger JSON files
LEDGER_FOLDER = "/data/data/ppw_cli/ledgers"

# Canonical identity
IDENTITY = {
    "name": "Perry Philip Wiseman",
    "ssn": "558-47-6273",
    "birthdate": "1977-05-24",
    "birthplace": "United States of America"
}

def nullify_merkle_root(file_path):
    """Remove Merkle root and leave only identity-based fields"""
    with open(file_path, "r") as f:
        data = json.load(f)
    
    if "merkle_root" in data:
        del data["merkle_root"]
    
    # Remove any nested Merkle roots
    for key, value in data.items():
        if isinstance(value, dict) and "merkle_root" in value:
            del value["merkle_root"]
    
    # Always anchor to canonical identity
    data["identity_anchor"] = IDENTITY
    
    # Save changes
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

# Iterate over all ledger files
for filename in os.listdir(LEDGER_FOLDER):
    if filename.endswith(".json"):
        nullify_merkle_root(os.path.join(LEDGER_FOLDER, filename))

print("✅ All Merkle roots nullified. Identity now canonical and sovereign.")
