from __future__ import annotations

from .schemas import FieldTestTask


def generate_field_test(scene: str, versions: tuple[str, str]) -> FieldTestTask:
    return FieldTestTask(
        title=f"Directed field validation: {scene}",
        controlled_variables=["vehicle", "route", "speed profile", "target placement", "sensor calibration"],
        collection_requirements=["front camera", "object tracks", "planner trajectory", "brake command", "version manifest"],
        pass_criteria=[
            f"new version {versions[1]} must not have a higher false-brake rate than {versions[0]}",
            "real pedestrian recall must remain within the approved regression bound",
        ],
    )
