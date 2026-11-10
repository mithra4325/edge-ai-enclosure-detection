# M1.5: Dataset Split & Zero Data Leakage Verification

**Status:** **COMPLETE**

---

## 1. Purpose of the Task
The objective of Milestone 1.5 is to rigorously audit the dataset distribution, demonstrate that the training, validation, and testing partitions adhere to the standard **70% / 20% / 10%** ratio, and cryptographically prove that no images or near-duplicates leak across partitions.

## 2. What I Implemented
- Inspected the physical Roboflow dataset export directories (`data/train/`, `data/valid/`, `data/test/`).
- Calculated the exact image counts and percentage distributions across all three partitions.
- Created an automated verification script ([`verify_split.py`](verify_split.py)) that computes SHA-256 cryptographic hashes for every image.
- Tested for filename collisions and binary content duplicates across all pair combinations (Train vs Valid, Train vs Test, Valid vs Test).
- Archived verification execution logs in [`verification_results.txt`](verification_results.txt).

## 3. Hardware Used
- Raspberry Pi 5 Model B Rev 1.1 (ARM Cortex-A76 quad-core @ 2.4 GHz, 4GB RAM).
- Ext4 filesystem storage on high-speed MicroSD.

## 4. Software and Dependencies
- Python 3.13 standard library (`hashlib`, `pathlib`).
- Standard POSIX filesystem utilities.

## 5. How the Implementation Works
1. `get_image_hashes()` traverses each partition directory (`train/images/`, `valid/images/`, `test/images/`) and generates a 256-bit SHA-256 digest of every image's raw binary contents:
   $$\text{Hash} = \text{SHA256}(\text{Image Bytes})$$
2. Set intersection checks ($\cap$) are executed on filename sets to detect any shared image names.
3. Set intersection checks are executed on SHA-256 hash sets to catch any image that was renamed, duplicated, or copy-pasted into another split.
4. Total image counts are summed and percentage ratios are evaluated against the target $70\% / 20\% / 10\%$ criteria.
5. If both filename overlap and hash overlap equal zero, the script issues a verified zero-leakage verdict.

## 6. How to Reproduce or Run It
From the project root on the Raspberry Pi 5:
```bash
# Run verification script
python3 current_split/verify_split.py
```

## 7. Evidence Available in this Folder
- [`verify_split.py`](verify_split.py): Standalone Python verification script.
- [`verification_results.txt`](verification_results.txt): Raw console execution output confirming 0 overlaps and exact 70/20/10 split.

## 8. Actual Results

### Dataset Partition Audit

| Split Name | Image Count | Actual Percentage | Target Percentage | Target Bounding Boxes | Overlap with Other Splits |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Train Set** | **28** | **70.0%** | 70% | 44 | **0 images** |
| **Validation Set** | **8** | **20.0%** | 20% | 11 | **0 images** |
| **Test Set (Held-Out)**| **4** | **10.0%** | 10% | 5 | **0 images** |
| **Total** | **40** | **100.0%** | 100% | **60** | **0 images** |

### Cryptographic Leakage Checks
- **Filename Overlap (Train vs Valid):** **0**
- **Filename Overlap (Train vs Test):** **0**
- **Filename Overlap (Valid vs Test):** **0**
- **SHA-256 Hash Collisions (Train vs Valid):** **0**
- **SHA-256 Hash Collisions (Train vs Test):** **0**
- **SHA-256 Hash Collisions (Valid vs Test):** **0**
- **Verification Verdict:** **SUCCESS — ZERO DATA LEAKAGE CONFIRMED**

## 9. Pending Items and Limitations
- **Pending Items:** None for Milestone 1.5.
- **Reference Link Clarification:** My college assessment document includes an external reference link:
  `https://github.com/theiceman07/edge-computing/tree/1ba9220105a474fa0c36774bed9383ceeea1e229/evidence/M1/05_correct_split`.
  As instructed, that link was used solely as reference for expected evidence standards. All verification here reflects my own independent dataset.
