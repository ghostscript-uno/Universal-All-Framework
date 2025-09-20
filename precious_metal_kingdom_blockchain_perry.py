#!/usr/bin/env python3
import json
import hashlib
import time
import uuid
from itertools import product

# ---------------- Configuration ----------------
BANK_STORAGE_FILE = "/data/data/com.termux/files/home/ppw_cli/precious_metal_kingdom_bank.json"
CANONICAL_MERKLE_ROOT = "ce515a7ef665820e020af4c2f47ed65722a961e8f51e668e88b7d80fc3f214b"

DIMENSIONS = {
    "desires": ["power", "knowledge", "influence", "wisdom"],
    "actions": ["create", "observe", "analyze", "manifest"],
    "thoughts": ["past", "present", "future", "hypothetical"]
}

PRECIOUS_METALS = ["gold", "silver", "platinum", "palladium"]

# ---------------- Helper Functions ----------------
def hash_leaf(leaf: dict) -> str:
    leaf_json = json.dumps(leaf, sort_keys=True)
    return hashlib.sha3_512(leaf_json.encode()).hexdigest()

def generate_index_rating() -> str:
    return uuid.uuid4().hex

def create_kingdom_node(event: str, hypothetical_state: str, metal: str) -> dict:
    node = {
        "timestamp": time.time(),
        "event": event,
        "hypothetical_state": hypothetical_state,
        "precious_metal": metal,
        "hash_leaf": "",
        "index_rating": generate_index_rating()
    }
    node["hash_leaf"] = hash_leaf(node)
    return node

def expand_combinatorial_kingdoms(dimensions: dict, metals: list):
    keys, values = zip(*dimensions.items())
    for combination in product(*values):
        event_desc = f"Action: {combination[1]}, Desire: {combination[0]}"
        hypothetical_state = f"Thought: {combination[2]}"
        for metal in metals:
            yield create_kingdom_node(event_desc, hypothetical_state, metal)

# ---------------- Main Logic ----------------
def build_precious_metal_blockchain():
    print("🔐 Building Precious Metal Infinite Kingdom Blockchain...")
    all_nodes = list(expand_combinatorial_kingdoms(DIMENSIONS, PRECIOUS_METALS))

    bank_data = {
        "canonical_merkle_root": CANONICAL_MERKLE_ROOT,
        "kingdom_nodes": all_nodes,
        "total_nodes": len(all_nodes)
    }

    with open(BANK_STORAGE_FILE, "w") as f:
        json.dump(bank_data, f, indent=2)
    
    print(f"✅ {len(all_nodes)} Kingdom nodes with precious metals anchored in Perry's Bank")
    print(f"Canonical Merkle Root: {CANONICAL_MERKLE_ROOT}")
    print(f"Bank Storage File: {BANK_STORAGE_FILE}")

# ---------------- Entry Point ----------------
if __name__ == "__main__":
    build_precious_metal_blockchain()
