# Evidence register — 4680 Cell Manufacturing Controls Testbed

Revision A · 2026-09-05 · Independent educational engineering project

| Artifact | Evidence class | Status |
|---|---|---|
| Python model and automated tests | Executable software | Run locally; see results/verification.txt |
| CSV traces and metrics | Synthetic model output | Reproducible with python demo.py |
| Architecture and engineering schedules | Concept design | Review draft |
| Vendor IDE compilation / physical I/O | Integration | Not performed |
| Oscilloscope, drive traces, real network timing | Hardware measurement | Not collected |
| Functional safety and code compliance | Independent validation | Not established |

No customer affiliation, factory deployment, vendor endorsement, certification,
or historical commissioning is asserted. Documentation and source were prepared
with AI assistance and require owner review. Do not backdate this project to 2025.
Vendor names identify intended integration targets only.

## Release boundary
These models cannot enforce a machine safety function. Their Boolean fault inputs
model supervisory behavior, not PROFIsafe/FSoE telegrams or certified safety logic.
Physical implementation needs a risk assessment, selected hardware manuals,
validated safety application, electrical review and supervised commissioning.
