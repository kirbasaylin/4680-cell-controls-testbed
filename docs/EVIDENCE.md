# Test status

The Python sequence and fault tests run locally and in GitHub Actions. The SCL source
has not been compiled in TIA Portal. No drive or physical I/O measurements are included.

## Reproduce the results

Run `python -m unittest discover -s tests -v`, then `python demo.py` from the repository
root. The saved local log is [verification.txt](../results/verification.txt).
[GitHub Actions](https://github.com/kirbasaylin/4680-cell-controls-testbed/actions) runs the same commands.

CSV/JSON outputs are model results. The PNG figure summarizes those outputs.
The [design notes](DESIGN.md) record assumptions; the [commissioning plan](COMMISSIONING.md)
lists the hardware work still needed.

No physical commissioning or safety certification has been completed for this project.
