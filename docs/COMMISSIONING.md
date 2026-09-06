# Commissioning and validation plan

**Document status: future integration procedure. No hardware steps signed off.**

| Gate | Action | Acceptance evidence | Status |
|---|---|---|---|
| 1 | Review model and assumptions | Tests and code walkthrough | Software only |
| 2 | Select hardware/runtime versions | BOM, firmware and compatibility matrix | Pending |
| 3 | Compile vendor source and adapters | Saved project plus build log | Pending |
| 4 | Review electrical/safety design | Approved drawings and validation plan | Pending |
| 5 | Verify field I/O without motion | Signed point-to-point record | Pending |
| 6 | Validate homing and low-speed motion | Direction, limits, scale and stopping traces | Pending |
| 7 | Exercise interlocks and restart | Timestamped scenario records | Pending |
| 8 | Validate performance under load | Raw drive/network/scope exports | Pending |

Use inert surrogates. Hardware fault injection must follow a reviewed test method;
the software's network-loss and brownout flags are not instructions to interrupt
energized cables or supplies. Record operator, reviewer, date, equipment IDs,
software revision, stimulus, expected response, observed response and raw evidence.

## Software reproducibility
Run `python -m unittest discover -s tests -v`, then `python demo.py` from this repository.
Saved `results/verification.txt` captures the local run. CI is configured but has not
run on GitHub until you publish. No native-PLC test coverage is implied.
