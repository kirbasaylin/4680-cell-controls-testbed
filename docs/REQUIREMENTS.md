# Next model revision

Proposed parameters supplied for the next iteration. These values are not measurements
and do not describe the current executable model. Current results remain in `results/`.

## Station parameters

| Parameter | Proposed value |
|---|---:|
| Conveyor nominal speed | 0.32 m/s |
| Cell pitch | 82 mm |
| Index move | 246 mm / 3 pitches |
| Normal index time | 0.92 s |
| Settle time | 180 ms |
| Station cycle time | 2.7–3.1 s |
| Index timeout | 1.50 s |
| Sensor debounce | 40 ms |
| Jam detection | 650 ms without an expected transition |
| Restart verification | 500 ms continuously healthy permissives |
| Recipe count | 4 |
| Digital inputs / outputs | 18 / 14 |
| Analog signals | 2 simulated |
| Intended topology | PLC, drive and remote I/O over PROFINET |

The existing model uses different motion and timing parameters. Debounce, stable-state
verification and an expanded I/O map need implementation. Recipe names, permitted
ranges and the full signal list still need definition.

## Throughput accounting

Moving three pitches does not necessarily mean completing three cells. The production
count must identify how many finished cells leave the station per cycle.

| Completed cells per cycle | Ideal rate at 3.1 s | Ideal rate at 2.7 s |
|---|---:|---:|
| 1 | 1,161 cells/h | 1,333 cells/h |
| 3 | 3,484 cells/h | 4,000 cells/h |

The proposed 1,050–1,200 cells/h estimate is consistent with approximately 90% effective
running time for one completed cell per cycle. That interpretation is a planning
assumption, not a measured production rate. If three cells finish each cycle, the lower
estimate requires a different bottleneck or utilization assumption.

## Regression plan

| Group | Planned cases |
|---|---:|
| Nominal production cycles | 12 |
| Recipe validation | 8 |
| Index timeout faults | 6 |
| Sensor disagreement | 5 |
| Jam recovery | 8 |
| Restart interlocks | 7 |
| Motion inhibition | 6 |
| First-fault retention | 9 |
| Power-cycle recovery | 3 |
| Total | 64 |

The proposed campaign also calls for 21 distinct fault scenarios. Individual scenarios,
stimuli and expected outcomes must be specified before that coverage can be counted.
The repository currently has eight test methods, including parameterized subcases.
The 64-case plan is not a PASS report.

## Event-sequence review

The supplied example commands indexing at 14.220 s and raises INDEX_TIMEOUT at 15.540 s.
That interval is 1.320 s. A 1.50 s timer starting at the command would expire at 15.720 s;
starting at the 14.237 s drive-run feedback would give 15.737 s.

The 650 ms jam timer also needs an explicit arming event. If armed at the index command,
it expires at 14.870 s, before either example timeout. If armed later, record that event
and define which alarm wins when both conditions occur.

The reset example clears the jam at 21.493 s, requests reset at 22.017 s and reports
SAFE_TO_RESTART at 22.520 s. Decide whether the 500 ms stable interval runs before reset
acceptance or starts after the reset request; implement and test one policy consistently.
After acceptance, require a separate start command. Generate event timestamps from the
implementation rather than copying the illustrative sequence into a result file.
