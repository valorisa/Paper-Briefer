# Compression Quality Validation Test

**Date:** 2026-05-10
**Paper:** DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence
**Paper size:** 46 pages, 20,270 words, 22 figures/tables
**Brief size:** ~3,900 tokens (4,155 with limitations fix)
**Compression:** ~5x

## Methodology

1. Generated a brief from the paper using `paper-briefer`
2. Gave the brief to a fresh LLM instance with NO access to the original paper
3. Asked 5 substantive technical questions spanning different comprehension dimensions
4. Evaluated: correctness, confidence calibration, hallucination detection

## Questions and Results

### Q1: Architecture (mechanism)
**Question:** How does DeepSeek-V4 achieve its 10x KV cache reduction compared to V3?

**Result:** PASS (Medium confidence)
- Correctly identified CSA + HCA hybrid as the mechanism
- Correctly described compression ratios and sliding window
- Flagged missing: specific m/m' values, layer allocation ratios

### Q2: Quantitative claims
**Question:** How does V4-Pro-Max compare to Claude models on coding tasks?

**Result:** PASS (High confidence)
- All 6 benchmark numbers reproduced exactly
- Correct relative positioning (outperforms Sonnet, approaches Opus)
- Flagged missing: benchmark methodology details

### Q3: Limitations
**Question:** What limitations do the authors acknowledge?

**Result:** FAIL (before fix) / PASS (after fix)
- Brief did not contain limitations section
- LLM correctly said "this information is not in the brief" (no hallucination)
- Fixed by adding `_extract_limitations()` to extraction engine

### Q4: Novelty assessment
**Question:** What's genuinely new in V4 vs V3?

**Result:** PASS (Medium confidence)
- Correctly separated: new (CSA/HCA, mHC, Muon) from inherited (DeepSeekMoE, MTP)
- Flagged missing: MTP status unclear, quantitative ablation data

### Q5: Practical implications
**Question:** What advantages would V4-Flash offer for document analysis deployment?

**Result:** PASS (Medium-High confidence)
- Derived 3.7x faster inference from 27% FLOPs ratio
- Correctly identified 10x memory reduction
- Made actionable deployment recommendations
- Flagged missing: actual latency numbers, cost comparisons

## Key Findings

1. **Zero hallucinations** — when information was missing, the LLM said so
2. **Figures carry the proof** — Q1 and Q5 were answerable because figure captions + anchors preserved the architectural explanation
3. **Exact numbers preserved** — Q2 worked perfectly because table data was extracted verbatim
4. **Limitations are critical** — the only failure was missing limitations, now fixed
5. **Confidence calibration works** — the LLM's self-reported confidence correlated with actual answer quality
