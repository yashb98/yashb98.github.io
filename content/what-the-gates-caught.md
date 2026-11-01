---
title: "What the Gates Caught"
summary: "Seven ways my own study tried to fool me (a token-soup data loader, an eval-token confound, a misread smoke log, a conflated data ratio) and how each one was caught or disclosed before it became a claim."
date: "2026-07-07"
tags: ["qwen3-0.6b", "methodology", "pre-registration", "reproduce-then-attribute"]
---

Every controlled result in my Qwen3-0.6B study passed through the same gates: a plausibility read of scored verdicts, a fixed held-out evaluation set required before any win call, iso-FLOP confound checks, and a claim-to-file audit that opens every cited artifact. The paper's Section 11 is a catalogue of what those gates caught *in my own work*, and it is the section I most want people to read. Positive results are easy to like. A protocol that demonstrably catches its author's own errors is the strongest warrant I can offer for the claims that survived it.

Here is the catalogue: symptom, detection, root cause, fix.

## The catalogue

### 1. The token-soup data mix

In the first data-mix run, the 50/50 dclm-edu/FineWeb-Edu blend scored roughly 2x *worse* than both pure parents: wikitext-2 BPB 2.77 against roughly 1.52, as recorded in the fix commit. That is physically implausible for a blend, whose loss should sit near the convex hull of its parents, and I caught it because a blend cannot score worse than both parents, before any conclusion was recorded. Root cause: a numpy shuffle applied at the *token* level had interleaved the two sources token by token, destroying all sequence structure. The fix (commit a576baa) concatenates the two coherent halves and mixes at the packed-sequence level, shuffling whole 4096-token windows. A 30-step probe after the fix shows training cross-entropy descending from 11.65 to 8.04, where the token-soup variant had stayed flat near 11. The broken cohort was discarded and rerun; the loader now carries an in-code warning.

### 2. The SFT eval-token confound

In-loop advisory scoring showed response-masked SFT beating its iso-FLOP control by 0.68 perplexity, nominally significant. The protocol forbids a win call from in-loop numbers, and re-scoring on one fixed held-out response-masked set collapsed the gap to +0.009 perplexity (95% CI [+0.0045, +0.0139], 3 seeds, paired), with a full-sequence cross-check giving -0.006 (95% CI [-0.011, -0.001]) in the control's favor, so it fails the one-sided improvement test. The arms had been scored on different token populations: response tokens versus all tokens. Verdict of record: directional. I wrote up the full anatomy in [The Win That Was Not](the-win-that-was-not.html); the standing guard is that in-loop perplexities are permanently labeled advisory.

### 3. The RFT smoke-log misread

An earlier draft of the RLVR verdict stated that the rejection-fine-tuning control collected *zero* verifier-correct completions. The claim-to-file audit for the paper re-read the full training log rather than its opening lines and found the "0 collected" line belongs to a one-step smoke test of 2026-07-02 at the top of the same log. The real 300-step run collected 352 of 38,400 rollouts, about 0.9%, matching the flat ~0.9% GRPO training reward. The verdict file and the repository README were corrected on 2026-07-06, with the correction note embedded in the regenerated artifact. The null verdict is unchanged (352 completions were far too few to separate RFT from the floor), but "zero" was wrong, and now smoke-test output is read as a distinct log segment.

This entry pairs with the study's cleanest pre-registered result: the GRPO null itself. Before the run, the decision rule was fixed: GRPO had to beat both the SFT floor and a random-reward control on non-overlapping confidence intervals, or Phase 3 would not proceed. The verifier-correct reward stayed flat at ~0.9% for all 300 steps (first-50 mean 0.0091, last-50 0.0080) while the random-reward gate arm hovered at ~0.5 by construction. GRPO beat neither gate on either eval set, and the pre-registered decision fired: no Phase 3. Single seed, capped as directional by design: a null I trust precisely because the bar was set before I could see the result.

[See the per-step rewards in the results file](https://github.com/yashb98/BuildFromScratch/blob/fe18745556e4877a0d2e804e15e423999fd40bb2/Qwen3-0.6B/results/grpo_rewards.json).

### 4. The conflated data ratio

Repository documentation paired the 2.14x gap-to-original with "~275,000x less data." The claim-to-file audit caught it: the source file pairs 275,000x with the 131M-token Phase-A probe, whose gap is 3.5x. Numbers from two different runs had merged into one sentence. The correct pairings are 2.14x at ~30,000x less data (the 1.19B-token run) and 3.5x at ~275,000x less data (the 131M-token run); both are descriptive-tier, single-run, in-loop validation-perplexity ratios, corrected 2026-07-06. The two runs and their source files are in [the gap results file](https://github.com/yashb98/BuildFromScratch/blob/fe18745556e4877a0d2e804e15e423999fd40bb2/Qwen3-0.6B/results/gap_to_original.json).

### 5. The build that died at 30%

The exploratory partial-RoPE-0.10 build died at step 5,450 of 18,150 (about 30% of budget) with a last-eval in-loop validation perplexity of 50.71 (single run, not suite-stamped). This one is an honesty entry rather than a gate catch: the temptation with a crashed exploratory arm is to quietly drop it. It is reported as incomplete in the paper instead, because a results table that only contains finished runs is a survivorship filter.

### 6. The stale derived field

The ledger entry for the mid-training anneal carried a sub-field reading "directional" beside a verdict field reading "win." The audit cross-checked every ledger field against the run's verdict artifact and found the cap predated a same-night upgrade that completed the stage's required evaluation battery: the verdict fields were updated, the derived sub-field was not. The authoritative verdict file supports the win. The lesson stands as a standing hazard: derived fields duplicated across artifacts can go stale independently of the record they summarize.

### 7. The citation that pointed at the wrong file

The model README cited verify.json as evidence for the 596,049,920-parameter count, but that file contains no parameter field. The number itself is correct; it is recovered exactly by recomputation from the architecture configuration and asserted in the build's test suite. Only the citation was off. The claim-to-file audit caught it, and the resulting rule became this site's thesis: every number must trace to the file that actually contains it.

## Why this is the argument

None of these was caught by re-reading prose, and I re-read the prose plenty. Item 5 is a disclosure rather than a catch. The other six came from an implausible scored verdict, a fixed held-out set required before any win call, or a claim-to-file audit that opens every cited artifact.

That is the case for gates and pre-registration in one sentence: the author is the least trustworthy reviewer of a result they want. My in-loop SFT "win" had a beautiful confidence interval. The mix-run failure looked like a boring bad arm until the implausible score gave it away. The RFT "zero" read fine for days. What kept each of these out of the record was not vigilance but structure: checks specified in advance, applied identically to results I liked and results I didn't. The same gates validate the positive claims in the paper, which is exactly why the failure catalogue is published next to them.
