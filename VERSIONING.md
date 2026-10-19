# Versioning protocol (set by Niko, 2026-10-18)

The hosted artifact has no platform rollback button. This repo is the revert
path: spec, decisions, data builders, and live-state snapshots, kept current
in the same change as the thing they describe.

## Rules

1. Commit after every verified build round. SPEC.md, DECISIONS.md, and the
   RECONSTRUCT.md changelog are updated in the same commit as the round they
   describe; never let the repo lag the shipped app.
2. Tag BEFORE any risky or experimental change:
   `pre-<change>-YYYY-MM-DD` (annotated, message states what "known good"
   means at that tag and what the experiment is).
   Tag AFTER major verified milestones: `good-<feature>-YYYY-MM-DD`.
3. At every tag, snapshot the artifact's live state with its `getstate`
   action into `snapshots/state-<tag>.json` and commit it with the tag.
4. Commit messages say what changed in the game (behavior), not just "update".
5. `hidden_files/` is never committed (throwaway credentials live only there).
6. The weekly workspace backup mirrors this repo to the Google Drive
   "Muse Bot" folder, so tags and snapshots do not live only on this VM.

## Reverting

A revert is a new artifact edit that restores the tagged behavior per SPEC.md
at that tag, plus, if game data is involved, the snapshot values re-saved via
the artifact's save actions. Verify the revert with the same played QA pass
as any other round, then commit and tag the revert itself.
