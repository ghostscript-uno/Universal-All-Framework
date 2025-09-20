#!/usr/bin/env python3
import json
import hashlib

# Personal identity info (without UID)
identity_info = {
    "name": "Perry Philip Wiseman",
    "birthdate": "1977-05-24",
    "ssn": "558-47-6273",
    "country": "United States of America"
}

# Load Universal Ownership JSON
json_file = "universal_ownership_cross_anchored_55847627305241977_2025-09-20T00-00-00Z.json"
with open(json_file) as f:
    data = json.load(f)

# Remove Merkle root for hashing
data_for_hash = data.copy()
data_for_hash.pop("merkle_root", None)

# Include identity info in the hash
data_for_hash["identity_info"] = identity_info

# Compute SHA3-512 hash
computed_hash = hashlib.sha3_512(json.dumps(data_for_hash, sort_keys=True).encode()).hexdigest()

print("Computed SHA3-512 hash:", computed_hash)
print("Stored Merkle root:", data["merkle_root"])

if computed_hash == data["merkle_root"]:
    print("✅ Ownership integrity verified with identity only")
else:
    print("❌ Hash mismatch — file may be altered or Merkle root not updated with identity only")
