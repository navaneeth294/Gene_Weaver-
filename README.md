# GeneWeaver

**GPU-accelerated, mismatch-tolerant sequence search for CRISPR guide screening**, written in Python with Numba CUDA.

When you design a CRISPR guide RNA, you need to find every place in a genome where the guide could bind, including near-matches with a few mismatches (potential off-target sites). A naive scan compares the guide against every genomic position, which gets slow on large genomes. GeneWeaver moves that scan onto the GPU, using one CUDA thread per genomic position.

> Personal project. It currently benchmarks on synthetic genomes; see [Limitations](#limitations).

---

## Results

Benchmarked on an NVIDIA GTX 1650 (4 GB VRAM), with guide `GTTTG`, at most 1 mismatch, on a uniformly random synthetic genome.

| Genome size | Matches | CPU time | GPU time | Speedup |
|---|---|---|---|---|
| 31 Mbp | 483,553 | 12.57 s | 0.265 s | **~47x** |
| 1 Gbp | 15,625,614 | 431.9 s | 1.11 s | **~390x** |

- **Correctness.** At 31 Mbp, the GPU and CPU outputs were compared position by position and found to have zero discrepancies, not just equal totals. At 1 Gbp the match counts are identical.
- **Memory.** The 1 Gbp genome ran without any `CUDA_OUT_OF_MEMORY` errors on a 4 GB card.
- **Sanity check.** The 1 Gbp match rate (~1.56%) agrees with the expected rate for a 5-nt guide with ≤1 mismatch on random sequence: 16/4⁵ = 1/64.

## How it works

```
FASTA ──► BioPython reader ──► uint8 encoding (A=0, C=1, G=2, T=3)
                                        │
                     ┌──────────────────┴──────────────────┐
                     ▼                                     ▼
          CPU baseline (Python)                 GPU kernel (Numba CUDA)
          sliding-window Hamming scan           1 thread per genome position
                     │                                     │
                     └──────────► compare results ◄────────┘
```

1. **Encoding.** Each sequence is converted to a `uint8` array. For large genomes, `encoding_for_bigdata.py` uses a vectorised NumPy lookup table instead of a per-character Python loop.
2. **CPU baseline** (`geneweaver.py`, `run_baseline.py`). A straightforward sliding window counts the mismatches at each position. It is the reference that the GPU output is checked against.
3. **GPU kernel** (`alignment_kernel.py`). Each thread computes the Hamming distance between the guide and one genome window and writes it to an output array. Data moves explicitly with `cuda.to_device()` and `copy_to_host()`.
4. **Verification** (`full_diagnostic.py`, `bug_check.py`). These compare the GPU and CPU results position by position.
5. **TUI** (`tui.py`). A [Textual](https://textual.textualize.io/) app reads the genome in 1 Mbp chunks and shows chunking progress with a progress bar.

## Project structure

| File | Purpose |
|---|---|
| `geneweaver.py` | CPU reference: `count_mismatches`, `find_matches` |
| `alignment_kernel.py` | Numba CUDA alignment kernel |
| `encode_seq.py` | DNA → `uint8` encoding |
| `run_baseline.py` | CPU benchmark on `mock_genome.fasta` |
| `run_gpu.py` | GPU benchmark on `mock_genome.fasta` |
| `full_diagnostic.py`, `bug_check.py` | GPU vs CPU position-by-position verification |
| `1b_genome.py` | Generates a 1-billion-base random genome (`mock_genome_1b.fasta`) |
| `encoding_for_bigdata.py` | Vectorised encoding + GPU run at 1 Gbp |
| `1b_cpu_test.py` | CPU baseline at 1 Gbp |
| `readgenome.py` | BioPython FASTA reading check |
| `tui.py` | Textual chunking progress UI |

## Getting started

**Requirements:** an NVIDIA GPU with a recent CUDA driver, and Python 3.10+ (developed on 3.12).

```bash
git clone https://github.com/navaneeth294/Gene_Weaver-.git
cd Gene_Weaver-
python -m venv venv
venv\Scripts\activate        # Windows  (Linux/macOS: source venv/bin/activate)
pip install -r requirements.txt
```

Run the 31 Mbp benchmark, which uses `mock_genome.fasta`:

```bash
python run_baseline.py       # CPU
python run_gpu.py            # GPU
```

Run the 1 Gbp benchmark (this writes a ~1 GB file, which is git-ignored):

```bash
python 1b_genome.py
python encoding_for_bigdata.py   # GPU
python 1b_cpu_test.py            # CPU (slow: several minutes)
```

Run the TUI:

```bash
python tui.py
```

## Debugging notes

- **Block-count off-by-one.** The grid-size calculation subtracted where it should have added. This under-launched threads and silently inflated the match count. Only the position-by-position comparison against the CPU caught it, which is why that check is part of the workflow.
- **NumPy 2.x vs numba-cuda.** An incompatibility (`row_stack`) was resolved by pinning NumPy below 2.

## Limitations

- The benchmarks use a short 5-nt guide on synthetic random sequence. Real CRISPR guides are ~20 nt and need a PAM check (e.g. `NGG` for SpCas9).
- Only the forward strand is scanned so far.
- The scoring is plain Hamming distance. It doesn't weight mismatches by position in the guide (as CFD/MIT scores do), and it doesn't handle bulges or indels.

## Roadmap

- [ ] Support realistic 20-nt guides with PAM filtering, and scan both strands
- [ ] Benchmark on a real reference assembly
- [ ] Stream genomes larger than GPU memory in chunks (Dask)
- [ ] Connect the TUI to live GPU alignment progress
- [ ] Package the scripts into a single CLI

## Tech stack

Python · Numba (CUDA) · NumPy · BioPython · Textual
