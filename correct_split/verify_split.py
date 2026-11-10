#!/usr/bin/env python3
"""
M1.5: Dataset Split & Zero-Leakage Verification Script
Mathematically verifies the 70/20/10 partition ratio and ensures zero image overlap
or cryptographic hash collisions (SHA-256) between Train, Valid, and Test splits.

Author: Mithra Ravi
Milestone: M1 Detect
"""

import sys
import hashlib
from pathlib import Path

def get_image_hashes(directory: Path):
    hash_map = {}
    for p in sorted(directory.glob("*.jpg")):
        with open(p, "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest()
            hash_map[h] = p.name
    return hash_map

def verify_dataset_split(base_dir: str = "data"):
    root = Path(base_dir).resolve()
    train_dir = root / "train" / "images"
    valid_dir = root / "valid" / "images"
    test_dir = root / "test" / "images"

    for d in [train_dir, valid_dir, test_dir]:
        if not d.exists():
            raise FileNotFoundError(f"Split directory missing: {d}")

    train_hashes = get_image_hashes(train_dir)
    valid_hashes = get_image_hashes(valid_dir)
    test_hashes = get_image_hashes(test_dir)

    n_train = len(train_hashes)
    n_valid = len(valid_hashes)
    n_test = len(test_hashes)
    n_total = n_train + n_valid + n_test

    p_train = (n_train / n_total) * 100.0
    p_valid = (n_valid / n_total) * 100.0
    p_test = (n_test / n_total) * 100.0

    print("=" * 65)
    print(" DATASET SPLIT & LEAKAGE VERIFICATION REPORT ")
    print("=" * 65)
    print(f"Total Images in Dataset: {n_total}")
    print(f"  - Training Set:   {n_train:2d} images ({p_train:5.1f}%) [Target: 70%]")
    print(f"  - Validation Set: {n_valid:2d} images ({p_valid:5.1f}%) [Target: 20%]")
    print(f"  - Test Set:       {n_test:2d} images ({p_test:5.1f}%) [Target: 10%]")
    print("=" * 65)

    # 1. Filename Overlap Check
    train_names = set(train_hashes.values())
    valid_names = set(valid_hashes.values())
    test_names = set(test_hashes.values())

    overlap_tv = train_names & valid_names
    overlap_tt = train_names & test_names
    overlap_vt = valid_names & test_names

    # 2. Cryptographic Hash Collision Check (Near-Duplicate / Cloned Images)
    h_tv = set(train_hashes.keys()) & set(valid_hashes.keys())
    h_tt = set(train_hashes.keys()) & set(test_hashes.keys())
    h_vt = set(valid_hashes.keys()) & set(test_hashes.keys())

    print("VERIFICATION CHECKS:")
    print(f"  1. Filename Overlap (Train vs Valid): {len(overlap_tv)} images")
    print(f"  2. Filename Overlap (Train vs Test):  {len(overlap_tt)} images")
    print(f"  3. Filename Overlap (Valid vs Test):  {len(overlap_vt)} images")
    print(f"  4. Hash Collisions  (Train vs Valid): {len(h_tv)} collisions")
    print(f"  5. Hash Collisions  (Train vs Test):  {len(h_tt)} collisions")
    print(f"  6. Hash Collisions  (Valid vs Test):  {len(h_vt)} collisions")
    print("=" * 65)

    is_exact_split = (round(p_train) == 70 and round(p_valid) == 20 and round(p_test) == 10)
    has_zero_leakage = (len(overlap_tv) == 0 and len(overlap_tt) == 0 and len(overlap_vt) == 0 and
                        len(h_tv) == 0 and len(h_tt) == 0 and len(h_vt) == 0)

    if is_exact_split and has_zero_leakage:
        print("[SUCCESS] Dataset strictly conforms to 70/20/10 ratio with ZERO data leakage.")
        return True
    else:
        print("[FAILURE] Dataset split anomaly or leakage detected.")
        return False

if __name__ == "__main__":
    verify_dataset_split()
