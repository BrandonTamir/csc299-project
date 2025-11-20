# SpeckIt Constitution

Purpose
-------
This document establishes a concise, practical set of rules and expectations for the "SpeckIt" prompt/spec system used in this repository. It exists to make prompt behavior predictable, reviewable, and easy to maintain.

Scope
-----
Applies to: prompt templates, prompt authoring guidelines, prompt review process, and small automation that uses these prompts.

Principles
----------
- Clarity: Prompts must be short, explicit about the goal, and include required constraints.
- Reproducibility: Prompts should produce consistent outputs for the same input when possible.
- Testability: Each prompt should include at least one example (input → expected output) when feasible.
- Minimal side-effects: Prompts must not request secrets or unsafe actions.

Structure for an approved prompt/spec
-----------------------------------
1. Title — short, descriptive.
2. Intent — one-line goal description.
3. Input format — required fields and types.
4. Output expectations — shape, tone, and constraints.
5. Examples — 1–3 representative examples (input → expected output).
6. Safety notes — any limitations or required guardrails.

Contribution & Review
---------------------
- Create or edit files under `.github/prompts/` following the structure above.
- Add or update examples in the same file; keep examples realistic and concise.
- Open a pull request for changes; include rationale and at least one example output.
- At least one reviewer must approve for a prompt/spec to be considered canonical.

Versioning & Changes
--------------------
- Small editorial changes (typos, formatting) can be merged after one reviewer approval.
- Behavioral changes (changing intent, examples, or constraints) should bump a `version:` field in the prompt file and require a brief changelog entry in the PR description.

Usage guidance for automation
----------------------------
- Automation using these prompts should pin the prompt file path and prompt version to avoid surprising updates.
- Tests (unit or snapshot) should validate key examples in CI.

Fallback when prompt file is empty
---------------------------------
If a referenced prompt file is empty or contains only a placeholder, follow these steps:
1. Do not run automation that depends on the prompt until a non-empty prompt/spec is provided.
2. Create a minimal prompt/spec following the structure above and include one example.
3. Open a PR and request review.

Contact
-------
For questions about SpeckIt prompts, add an issue in the repo or ping the maintainer(s) listed in the CODEOWNERS file.

---
Generated: a default SpeckIt constitution because the referenced prompt files were placeholders.
