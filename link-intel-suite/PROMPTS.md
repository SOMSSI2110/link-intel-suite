# PROMPTS.md - my key prompts log

Keep the handful of prompts that actually moved the build. Not every message - the ones that
mattered: the system/sub-agent prompts, the ones you iterated on, the "this finally worked"
moment. Paste them here MANUALLY as you go.

Why manual? Some free Ollama cloud models do not save a local session log, so an auto audit
log may be empty. That is fine and expected (see the brief's Model Fairness section). What
guarantees your process is judged fairly is: the working plugin + reproducible report.json,
incremental git commits, this PROMPTS.md, and a short DECISIONS.md. Keep these up to date.

Format per entry:
- **Prompt** (paste it)
- **For:** what you were trying to do
- **Revised?** did you have to change it, and why

---

## Example (replace with your own)

- **Prompt:** "Extend linkintel/analyzer.py over_optimized_anchors: flag a destination where
  one non-generic anchor is >= 60% of all internal anchors pointing at it AND count >= 10.
  Run python linkintel/analyzer.py and show the counts."
- **For:** completing the over-optimized exact-match anchor rule
- **Revised?** Yes - first version flagged tiny destinations; added the count >= 10 floor.

---

## My prompts
1. **Prompt:**
"Explain the Internal Linking Intelligence architecture, starter bundle structure, report schema and scoring priorities."

**For:**
Understanding project architecture before implementation.

**Revised?**
No.
2. Prompt:
Review only cluster_pages() against rulebook section C. List exactly 3 weaknesses and do not modify code.

For:
Identifying highest-impact scoring weaknesses in topical clustering.

Revised?
No.
3. Prompt:
Design a deterministic clustering algorithm that uses page keywords as the primary clustering signal instead of URL path segments. Explain only, do not modify code.

For:
Finding a rulebook-compliant clustering strategy before implementation.

Revised?
Pending comparison against current URL-path approach.
