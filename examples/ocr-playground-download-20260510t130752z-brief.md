# DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence

**Authors:** research@deepseek.com
**Scope:** 46 pages, 22 figures/tables, 20270 words

## Abstract

We present a preview version of DeepSeek-V4 series, including two strong Mixture-of-Experts (MoE) language models — DeepSeek-V4-Pro with 1.6T parameters (49B activated) and DeepSeek-V4-Flash with 284B parameters (13B activated) — both supporting a context length of one million tokens. DeepSeek-V4 series incorporate several key upgrades in architecture and optimization: (1) a hybrid attention architecture that combines Compressed Sparse Attention (CSA) and Heavily Compressed Attention (HCA) to improve long-context efficiency; (2) Manifold-Constrained Hyper-Connections (mHC) that enhance conventional residual connections; (3) and the Muon optimizer for faster convergence and greater training stability. We pre-train both models on more than 32T diverse and high-quality tokens, followed by a comprehensive post-training pipeline that unlocks and further enhances their capabilities. DeepSeek-V4-Pro-Max, the maximum reasoning effort mode of DeepSeek-V4-Pro, redefines the state-of-the-art for open models, outperforming its predecessors in core tasks. Meanwhile, DeepSeek-V4 series are highly efficient in long-context scenarios. In the one-million-token context setting, DeepSeek-V4-Pro requires only $27\%$ of single-token inference FLOPs and $10\%$ of KV cache compared with DeepSeek-V3.2. This enables us to routinely support one-million-token contexts, thereby making long-horizon tasks and further test-time scaling more feasible. The model checkpoints are available at https://huggingfa

## Key Contributions

- the DeepSeek-V4 series
- a hybrid attention mechanism combining Compressed Sparse Attention (CSA) and Heavily Compressed Attention (HCA)
- the Muon *(Jordan et al
- several infrastructure optimizations
- and implement a single fused kernel for MoE modules that fully overlaps computation
- a heterogeneous KV cache structure with on-disk storage strategies to enable efficient shared-prefix reuse

## Specifications

- **DeepSeek-V4-Pro**: total_parameters: 1.6T, activated_parameters: 49B
- **and DeepSeek-V4-Flash**: total_parameters: 284B, activated_parameters: 13B
- **iew versions of DeepSeek-V4-Pro**: total_parameters: 1.6T, activated_parameters: 49B

## Key Figures & Tables

**Figure 1** (p.1): Left: benchmark performance of DeepSeek-V4-Pro-Max and its counterparts. Right: inference FLOPs and KV cache size of DeepSeek-V4 series and DeepSeek-V3.2.
  > Figure 1 | Left: benchmark performance of DeepSeek-V4-Pro-Max and its counterparts.
  > The right part of Figure 1 demonstrates the estimated single-token inference FLOPs and accumulated KV cache size of DeepSeek-V3.2 and DeepSeek-V4 series.
**Figure 2** (p.6): Overall architecture of DeepSeek-V4 series. We use hybrid CSA (Compressed Sparse Attention) and HCA (Heavily Compressed Attention) for attention layers, DeepSeekMoE for feed-forward layers, and strengthen conventional residual connections with mHC.
  > Furthermore, DeepSeek-V4-Flash-Max achieves comparable Figure 2 | Overall architecture of DeepSeek-V4 series.
  > Figure 2 illustrates the overall architecture of DeepSeek-V4, and the details are described below.
**Figure 3** (p.9): Core architectures of CSA. It compresses the number of KV entries to  $\frac{1}{m}$  times, and then applies DeepSeek Sparse Attention for further acceleration. Additionally, a small set of sliding window KV entries is combined with the selected compressed KV entries to enhance local fine-grained dependencies.
  > ## Figure 3 | Core architectures of CSA.
  > Compressed Sparse Attention The core architecture of CSA is illustrated in Figure 3, which first compresses the KV cache of each $m$ tokens into one entry, and then applies DeepSeek Sparse Attention for further acceleration.
**Figure 4** (p.11): Core architectures of HCA. It performs heavier compression, where the KV entries of  $m'$  ( $\gg m$ ) tokens will be consolidated into one. Also, we additionally introduce a small set of sliding window KV entries to enhance local fine-grained dependencies.
  > For a query token $t$, given its index scores $I_{t,:}$, we employ a top-k selector to selectively retain a subset of compressed KV entries $C^{\text{SprsComp}}_{t}$ for subsequent core attention: $C^{\text{SprsComp}}_{t}=\left\{C^{\text{Comp}}_{s}\l
  > Heavily Compressed Attention The core architecture of HCA is illustrated in Figure 4, which compresses the KV cache in a heavier manner, but does not employ sparse attention.
**Figure 5** (p.15): Illustration of our EP scheme with related works. Comet (Zhang et al., 2025b) overlaps Dispatch with Linear-1, and Linear-2 with Combine, separately. Our EP scheme achieves a finer-grained overlapping by splitting and scheduling experts into waves. The theoretical speedup is evaluated in the configuration of the DeepSeek-V4-Flash architecture.
  > As shown in Figure 5, in DeepSeek-V4 series, each MoE layer can be decomposed mainly into four stages: two communication-bound stages, Dispatch and Combine, and two computation-bound stages, Linear-1 and Linear-2.
  > Figure 5 | Illustration of our EP scheme with related works.
**Figure 6** (p.21): Illustration of the KV cache Layout for DeepSeek-V4. The KV cache is organized into two primary components: a classical KV cache for CSA/HCA, and a state cache for SWA and unready-for-compression tokens in CSA/HCA. In the state cache, each request is assigned a fixed-size cache block. Within this block, the SWA segment stores the KV entries corresponding to the most recent  $n_{\mathrm{win}}$  tokens, while the CSA/HCA segment stores uncompressed tail states that are not yet ready for compression. In the classical KV cache, we allocate multiple blocks per request. Each cache block covers  $\operatorname{lcm}(m, m')$  original tokens, producing  $k_1 = \frac{\operatorname{lcm}(m, m')}{m}$  CSA compressed tokens and  $k_2 = \frac{\operatorname{lcm}(m, m')}{m'}$  HCA compressed tokens.
  > The layout is illustrated in Figure 6, and we will elaborate on it in detail as follows.
  > The lightning indexer for sparse selection introduces additional dimensions Figure 6 | Illustration of the KV cache Layout for DeepSeek-V4.
**Figure 7** (p.31): Thinking management of DeepSeek-V4 series.
  > a) Thinking with tools b) Thinking without tools Figure 7 | Thinking management of DeepSeek-V4 series.
  > As illustrated in Figure 7(a), all reasoning content is fully preserved throughout the entire conversation.
**Figure 8** (p.39): Formal reasoning under practical and frontier regimes. Left: Putnam-200 Pass@8 evaluates a fixed random subset of PutnamBench (Tsoukalas et al., 2024) following the setup introduced by Seed-Prover; all models are tested on the same problem set. We follow the Seed-Prover protocol but replace proprietary search tools with the open-source LeanExplore (Asher, 2025), yielding a lightweight setting with minimal agent tools and bounded sampling. Right: Putnam-2025 probes the frontier of mathematical reasoning in a scaled hybrid formal-informal regime, where informal reasoning is combined with formal verification to expose gaps and improve rigor; DeepSeek-V4 reaches a proof-perfect 120/120.
  > Under an agentic setup, it achieves state-of-the-art results, shown in Figure 8, outperforming prior models such as Seed Prover (Chen et al., 2025).
  > Figure 8 | Formal reasoning under practical and frontier regimes.
**Figure 9** (p.39): DeepSeek-V4 series performance on the MRCR task.
  > As illustrated in Figure 9, retrieval performance remains highly stable within a 128K context window.
  > Figure 9 | DeepSeek-V4 series performance on the MRCR task.
**Figure 10** (p.40): HLE and Terminal Bench 2.0 performance by reasoning effort. "None" indicates Non-think mode, and "Speciale" indicates DeepSeek-V3.2-Speciale model.
  > Figure 10 presents a comparison of performance and cost among DeepSeek-V4-Pro, DeepSeek-V4-Flash, and DeepSeek-V3.2 on representative reasoning and agentic tasks.
  > Figure 10 | HLE and Terminal Bench 2.0 performance by reasoning effort.
**Figure 11** (p.42): Win-rate comparison across analysis, generation, editing tasks, and the overall performance.
  > As illustrated in Figure 11, DeepSeek-V4-Pro-Max outperforms Opus-4.6-Max on diverse Chinese white-collar tasks, achieving an impressive non-loss rate of 63%, and demonstrating consistent advantages across analysis, generation, and editing tasks.
  > Figure 11 | Win-rate comparison across analysis, generation, editing tasks, and the overall performance.
**Figure 12** (p.42): Detailed dimension scores including Task Completion, Content Quality, Formatting Aesthetics, and Instruction Following.
  > The detailed dimension scores shown in Figure 12 highlight the model’s primary strengths in Task Completion and Content Quality.
  > Figure 12 | Detailed dimension scores including Task Completion, Content Quality, Formatting Aesthetics, and Instruction Following.
**Figure 13** (p.43): Example output of a task which requires drafting a joint marketing proposal for a popular bubble tea brand and the Beijing Subway.
  > Figure 13, 14, and 15 present several test cases; due to the extensive length of certain outputs, only partial pages are displayed.
  > Figure 13 | Example output of a task which requires drafting a joint marketing proposal for a popular bubble tea brand and the Beijing Subway.
**Table 1** (p.27): Comparison among DeepSeek-V3.2-Base, DeepSeek-V4-Flash-Base, and DeepSeek-V4-Pro-Base. All models are evaluated in our internal framework and share the same evaluation setting. Scores with a gap not exceeding 0.3 are considered to be at the same level. The highest score in each row is in bold font, and the second is underlined.
  > #### 4.3.2 Evaluation Results In Table 1, we provide a detailed comparison of the base models for DeepSeek-V3.2, DeepSeek-V4-Flash, and DeepSeek-V4-Pro, all evaluated under a unified internal framework with strictly consistent settings.
  > Table 1 | Comparison among DeepSeek-V3.2-Base, DeepSeek-V4-Flash-Base, and DeepSeek-V4-Pro-Base.
**Table 2** (p.29): Comparison of three reasoning modes
  > As detailed in Table 2, DeepSeek-V4-Pro and DeepSeek-V4-Flash both support three specific reasoning effort modes.
  > Table 2 | Comparison of three reasoning modes | Reasoning Mode | Characteristics | Typical Use Cases | Response Format | | --- | --- | --- | --- | | Non-think | Fast, intuitive responses based on habits or simple rules.
**Table 3** (p.29): Instruction injected into the system prompt for the "Think Max" mode.
  > Furthermore, for the "Think Max" mode, we prepend a specific instruction to the beginning of the system prompt to guide the model's reasoning process, as shown in Table 3.
  > <think> thinking tokens </think> summary | Table 3 | Instruction injected into the system prompt for the "Think Max" mode.
**Table 4** (p.30): Tool-call schema for DeepSeek-V4 series.
  > Table 4 | Tool-call schema for DeepSeek-V4 series.
  > In DeepSeek-V4 series, we introduce a new tool-call schema that employs a special “|DSML|” token and utilizes an XML-based format for tool invocations, as demonstrated in Table 4.
**Table 5** (p.32): Quick Instruction special tokens for auxiliary tasks.
  > Table 5 | Quick Instruction special tokens for auxiliary tasks.
  > The supported Quick Instruction tokens are summarized in Table 5.
**Table 6** (p.37): Comparison between DeepSeek-V4-Pro-Max and closed/open source models. "Max", "xHigh", and "High" denote reasoning effort. The best results are highlighted in bold; the second-best results are underlined.
  > #### 5.3.2 Evaluation Results The comparison of DeepSeek-V4-Pro-Max and other closed/open source models is presented in Table 6.
  > Table 6 | Comparison between DeepSeek-V4-Pro-Max and closed/open source models.
**Table 7** (p.37): Comparison among different sizes and modes of DeepSeek-V4 series. "Non-Think", "High", and "Max" denote reasoning effort.
  > Also, we evaluate different modes of DeepSeek-V4-Flash and DeepSeek-V4-Pro and show the results in Table 7.
  > Meanwhile, DeepSeek-V4-Pro and DeepSeek-V4-Flash excel in cod Table 7 | Comparison among different sizes and modes of DeepSeek-V4 series.
**Table 13** (p.41): presents the creative writing comparison, which is evaluated along two axes: instruction following and writing quality. Compared with Gemini-3.1-Pro, DeepSeek-V4-Pro achieves a  $60.0\%$  win rate in instruction following and  $77.5\%$  in writing quality, demonstrating a marginal improvement in instruction following and a substantial gain in writing quality. Although DeepSeek-V4-Pro yields superior results in aggregate user case analysis, an evaluation restricted to the most challenging prompts — specifically those involving high-complexity constraints or multi-turn scenarios — reveals that Claude Opus 4.5 retains a performance advantage over DeepSeek-V4-Pro. As shown in Table 14, Claude Opus 4.5 achieves a  $52.0\%$  win rate versus  $45.9\%$ .
  > Table 13 presents the creative writing comparison, which is evaluated along two axes: instruction following and writing quality.
**Table 8** (p.44): Comparison on R&amp;D Coding Benchmark (external models included strictly for evaluation purposes).
  > As shown in Table 8, DeepSeek-V4-Pro significantly outperforms Claude Sonnet 4.5 and approaches the level of Claude Opus 4.5.
  > Table 8 | Comparison on R&amp;D Coding Benchmark (external models included strictly for evaluation purposes).

## Structure

- 1 Introduction (p.4)
- 2 Architecture (p.6)
- 2.1 Designs Inherited from DeepSeek-V3 (p.7)
- 2.2 Manifold-Constrained Hyper-Connections (p.7)
- 2.3 Hybrid Attention with CSA and HCA (p.9)
- 2.4 Muon Optimizer (p.14)
- 3 General Infrastructures (p.15)
- 3.1 Fine-Grained Communication-Computation Overlap in Expert Parallelism (p.15)
- 3.2 Flexible and Efficient Kernel Development with TileLang (p.16)
- 3.3 High-Performance Batch-Invariant and Deterministic Kernel Libraries (p.18)
- 3.4 Training Framework (p.19)
- 3.5 Inference Framework (p.21)
- 4 Pre-Training (p.24)
- 4.1 Data Construction (p.24)
- 4.2 Pre-Training Setups (p.24)
- 4.3 Evaluations (p.27)
- 5.1 Post-Training Pipeline
- 5.2 Post-Training Infrastructures
- 5.3 Standard Benchmark Evaluation
- 5.4 Performance on Real-World Tasks
- 6 Conclusion, Limitations, and Future Directions

## Limitations & Future Work

- A Author List and Acknowledgment - A.1 Author List - A.2 Acknowledgment - B Evaluation Details 1 Introduction The emergence of reasoning models *(DeepSeek-AI, 2025; OpenAI, 2024c)* has established a new paradigm of test-time scaling, driving substantial performance gains for Large Language Models (LLMs). However, this scaling paradigm is fundamentally constrained by the quadratic computational complexity of the vanilla attention mechanism *(Vaswani et al., 2017)*, which creates a prohibitive bottleneck for ultra-long contexts and reasoning processes. Concurrently, the emergence of long-horizon scenarios and tasks — from complex agentic workflows to massive cross-document analysis — has also made efficient support for ultra-long contexts critical for future progress. While recent open-source efforts *(Bai et al., 2025a; DeepSeek-AI, 2024; MiniMax, 2025; Qwen, 2025)* have advanced general capabilities, this core architectural inefficiency in handling ultra-long sequences remains a key 

## Evidence Density

Reference-heavy pages: p.27, p.36, p.37
Novel content pages: p.1, p.2, p.3, p.8, p.9, p.10, p.11, p.12, p.15, p.16

## Cross-References

- p.7 → Figure 2: ### 2.2 Manifold-Constrained Hyper-Connections As shown in Figure 2, DeepSeek-V4 series incorporate 
- p.15 → Figure 5: ctively hidden beneath computation in MoE layers. As shown in Figure 5, in DeepSeek-V4 series, each 
- p.29 → Table 3: em prompt to guide the model's reasoning process, as shown in Table 3. Table 2 | Comparison of three
- p.40 → Table 7: is better than Gemini-3.1-Pro. Reasoning Effort. As shown in Table 7, the Max mode, which employs lo
- p.41 → Table 14: ins a performance advantage over DeepSeek-V4-Pro. As shown in Table 14, Claude Opus 4.5 achieves a $
- p.42 → Table 9: e accuracy within a predefined "thinking budget". As shown in Table 9, agentic search consistently o
- p.42 → Table 10: only marginally more expensive than standard RAG (see Table 10). #### 5.4.3 White-Collar Task To rig
- p.44 → Table 8: ing, 30 tasks are retained as the evaluation set. As shown in Table 8, DeepSeek-V4-Pro significantly
