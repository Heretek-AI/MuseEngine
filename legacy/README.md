# Legacy upload

These are the original files, kept unchanged for reference (apart from removing a byte-identical duplicate of the eval harness). They are not imported by the `museengine` package.

The rewrite in v0.2 addressed the following problems:

- **No model in the loop.** `llm_callable` was stored and never called. Every "phase" was keyword counting plus f-string templates, so "How do I bake sourdough?" got a slime-mold network design.
- **Fake actions.** In `Autonomic Cognitive Os.py`, "build" and "falsify" only adjusted floats and logged sentences such as "verified conservation law". The "compiled skills" pointed to a function that doesn't exist. Goals rotated through 4 hard-coded strings. Only 4 of the advertised 5 agents ever bid.
- **Rigged evaluation.** In `Muse Eval Harness.py`:
  - The scorer rewarded the same jargon the templates emit.
  - The baselines were hand-written strawmen.
  - The DMN "lift" added a literal `+ 38.5`.
  - The ablation didn't ablate, because `seed_traces=[]` fell back to the default traces.
  - The simulations gave the engine a hard-coded capacity advantage.
- **Not runnable as uploaded.** Filenames contain spaces while the modules import snake_case names, and the code prepends a path from the original authoring sandbox.
- **Persistence.** It rewrote the whole SQLite file on every tick with no temp file and no rename, while its docs called this "atomic".
