# Design basis · CELL-001 · Rev A

## Scope and assumptions
The station transfers inert 46 mm diameter × 80 mm cylindrical surrogates between
an infeed conveyor, indexing nest and outfeed. The 4680 designation is a form-factor
reference. No electrolyte, welding, formation, battery chemistry, or live-cell process
is modeled. A part-present sensor releases an 80 mm relative index; the station dwells
for 200 ms and checks exit clearance before completing one cycle.

## Control contract
| State | Command | Exit condition | Abnormal path |
|---|---|---|---|
| IDLE | All off | Fresh start edge | Any active fault latches |
| FEED | Conveyor | Part present | 3 s timeout |
| INDEX | Axis move | Target reached | Drive fault / 3 s timeout |
| DWELL | All off | Recipe dwell elapsed | 3 s timeout |
| EJECT | Conveyor while exit blocked | Exit clear | 3 s timeout |
| COMPLETE | All off | Start released | No repeat from held start |
| FAULT | All off | Fault cleared + reset edge with start released | No automatic restart |

Fault priority is safety permissive, network health, drive health, then jam. The first
fault is retained until reset. Jam recovery is a stop, manual clearance, reset and fresh
start; automatic reverse is intentionally outside this design. Position is retained in
the Python model, so the next cycle starts a new relative move from the stopped position.
A real station must re-establish nest registration or home before resuming production.

Recipe defaults: 80 mm pitch, 160 mm/s speed, 0.2 s dwell, 3 s state timeout.
Recipe changes are accepted only in IDLE. The kinematic Python axis has no inertia,
acceleration, load torque, encoder quantization or drive loop. Index motion takes about
0.5 s; that is a model input consequence, not measured throughput or tuning evidence.
Sensors in demo.py are scripted ideal inputs, not an independent material-flow model.

## Intended integration
Concept: S7-1500 standard control with distributed I/O and drive interfaces on PROFINET.
A separately engineered safety system supplies a diagnostic permissive to the standard
PLC. PROFIsafe and drive STO require compatible safety hardware, configured addresses,
watchdogs and validated safety logic; none is implemented by the Python model or SCL.
No IP addresses, telegram selections or catalog numbers are claimed to be commissioned.

## Native source boundary
FB_CellSequence.scl is a vendor-oriented source draft, not a TIA project. It consumes
IndexDone from a future motion adapter, whereas Python calculates a target position.
Build an adapter around the selected technology object and its Busy/Done/Error semantics;
clear stale Done before accepting another command. Add homing, motion abort handling,
recipe validation, retentivity policy and I/O plausibility checks in the vendor project.
The two implementations are not proven equivalent and the SCL has not been compiled.

## Review risks
| Risk | Current handling | Remaining work |
|---|---|---|
| Pinch/crush at indexer | Model stops on lost permissive | Risk assessment and safety validation |
| Part sensor stuck high | Timeout covers missing transitions only partly | Add edge/occupancy plausibility |
| Network loss | Injected Boolean latches alarm | Real device diagnostics and watchdog tests |
| Mid-index jam | Motion request removed | Physical stopping and registration recovery |
| Recipe beyond machine limits | Positive values + travel/timeout validation | Mechanical bounds and access control |
