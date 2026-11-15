# Consolidated research materials

The seven research branches were reviewed against `main` on 2026-11-15.
Their distinct reference-audit sources and dated reports are collected below.
They are separate from the three reasoning modules and are not loaded by the
Skill router or the behavioral benchmark.

## Materials retained once

| Material | Purpose and status |
|---|---|
| [audit_public.py](public-reference-audit/audit_public.py) | Original public-reference numbering and MMseqs2 audit script; preserved byte for byte. |
| [public_pairwise_followup.py](public-reference-audit/public_pairwise_followup.py) | Original all-pair follow-up script; preserved byte for byte. Its required historical artifact is currently unavailable through the queried run. |
| [Public-reference result](public-reference-audit/PUBLIC_AUDIT_RESULT_zh.md) | Dated source report from 2026-11-07; not a new result of this repository consolidation. |
| [All-pair result](public-reference-audit/PUBLIC_PAIRWISE_ACTUAL_RESULT_20261107_zh.md) | Dated follow-up report from 2026-11-07; not a new result of this repository consolidation. |
| [Source and asset manifest](branch-consolidation.json) | Original branches, commits, blobs, file hashes, per-file decisions and a deduplicated catalog of pinned public assets. |

## Reproduction status

Both scripts are standalone historical experiments. They perform network access
and create output directories when executed or imported. The first script's
original workflow used CPU PyTorch 2.9.1 and ANARCII 2.0.8; the scripts fetch the
specified MMseqs2 release. The follow-up requires the exact source-audit ZIP,
its recorded digest, `GH_TOKEN` and `GITHUB_REPOSITORY`, and uses a fixed artifact
ID. On 2026-11-15, GitHub returned no artifacts for runs `42327052038` and
`42352634152`. The original artifact dependency is therefore unresolved; the
reason for its unavailability was not established. The source and reports are
retained without representing the follow-up as currently runnable.

This consolidation checked Python syntax, source-blob equality and repository
validation. It did not execute these two networked experiments, download model
weights, invoke a provider or repeat the reported scientific calculations.
The checksums in the asset catalog are values recorded in the source workflows,
not new verification of remote model files. Original asset licenses still apply.

## Branch resolution

All seven branch heads are preserved as ancestors of the consolidation commit.
Identical source blobs are integrated once. The 29 one-shot workflow files and
three encrypted transport files remain retrievable from their original commits;
they are not copied into the active source tree. The temporary branch README is
replaced by this index. The two research-only branches' deletions of the main
project are explicitly rejected, preserving the current modules, tests and CI.

The per-file manifest gives a source commit and path for historical retrieval,
for example `git show <source-commit>:<source-path>`. No encrypted payload was
decrypted. No historical workflow was activated by this consolidation.
