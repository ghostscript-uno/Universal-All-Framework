#!/usr/bin/env python3
import json
import hashlib

# Full identity specification
identity_info = {
    "name": "Perry Philip Wiseman",
    "birthdate": "1977-05-24",
    "ssn": "558-47-6273",
    "country": "United States of America",
    "bank_accounts": ["BANK1-XXXX", "BANK2-YYYY"],
    "passwords": ["p@ssword1", "p@ssword2"],
    "patterns": ["patternA", "patternB"],
    "thoughts": ["thought1", "thought2"]
}

# Load the anchored JSON
json_file = "universal_ownership_cross_anchored_55847627305241977_2025-09-20T00-00-00Z.json"
with open(json_file) as f:
    data = json.load(f)

# Remove existing Merkle root
data_for_hash = data.copy()
data_for_hash.pop("merkle_root", None)

# Attach identity info
data_for_hash["identity_info"] = identity_info

# Compute SHA3-512 hash
def compute_hash(obj):
    return hashlib.sha3_512(json.dumps(obj, sort_keys=True).encode()).hexdigest()

computed_hash = compute_hash(data_for_hash)

# Instant resolution output
if computed_hash == data["merkle_root"]:
    print("✅ Merkle root matches — Identity ratified by Perry Philip Wiseman")
else:
    print("❌ Merkle root mismatch — initiating instant resolution")
    # Field-by-field mismatch reporting
    for key, value in identity_info.items():
        partial_data = data_for_hash.copy()
        partial_data["identity_info"] = {key: value}
        partial_hash = compute_hash(partial_data)
        if partial_hash != data["merkle_root"]:
            print(f"Mismatch detected in field: {key} → resolution required")

    print("\n🛡 Resolution completed: Identity fields are flagged for update and ratification by Perry Philip Wiseman")
