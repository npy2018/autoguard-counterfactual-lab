# Method and data sources

- comma.ai, **comma2k19**: https://github.com/commaai/comma2k19
- Pearl-style intervention semantics are represented here as controlled software interventions, not as a claim of full causal identification from observational logs.
- The project separates parameter/module interventions from lower-confidence environment or pixel interventions to make Sim2Real limits explicit.

# Research and public-data sources

- comma.ai, **comma2k19** — official repository: https://github.com/commaai/comma2k19
- Motional / nuScenes devkit, **CAN bus expansion**: https://github.com/nutonomy/nuscenes-devkit/blob/master/python-sdk/nuscenes/can_bus/README.md

Public telemetry is used only as a real-world signal source. Any OTA fault in the demos is explicitly controlled and injected; the repositories do not claim that the upstream dataset contains a real OTA defect.
