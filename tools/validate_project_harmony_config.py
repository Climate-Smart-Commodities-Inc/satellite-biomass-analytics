#!/usr/bin/env python3
"""Validate public Project Harmony planning configuration files.

This validator checks internal consistency and repository safety. It does not
validate engineering feasibility, regulatory status, grant eligibility, or
commercial commitments.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config" / "project_harmony"
FORBIDDEN_KEY_FRAGMENTS = ("api_key", "secret", "password", "token", "private_key")
ALLOWED_CREDENTIAL_KEYS = {"credential_source", "environment_variable_name", "rotation_policy"}


def load_json(filename: str) -> dict[str, Any]:
    path = CONFIG_DIR / filename
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def assert_no_embedded_credentials(value: Any, path: str = "root") -> None:
    if isinstance(value, dict):
        for key, nested_value in value.items():
            normalized = key.lower()
            if (
                any(fragment in normalized for fragment in FORBIDDEN_KEY_FRAGMENTS)
                and key not in ALLOWED_CREDENTIAL_KEYS
            ):
                raise ValueError(f"Credential-like field is prohibited at {path}.{key}")
            assert_no_embedded_credentials(nested_value, f"{path}.{key}")
    elif isinstance(value, list):
        for index, nested_value in enumerate(value):
            assert_no_embedded_credentials(nested_value, f"{path}[{index}]")


def validate_micro_pilot(config: dict[str, Any]) -> None:
    if config["planning_status"] != "assumption_only":
        raise ValueError("Micro-pilot configuration must remain marked as assumption_only")
    if config["site_location"]["visibility"] != "restricted":
        raise ValueError("Public configuration must keep the exact site location restricted")

    baseline = config["baseline_model"]
    factor = config["pilot_scale_factor"]
    metrics = config["metrics"]
    expected_footprint = baseline["reference_footprint_sq_ft"] * factor
    expected_tph = baseline["reference_processing_tons_per_hour"] * factor
    expected_shift = expected_tph * 8
    expected_annual = expected_shift * 5 * 50

    if metrics["facility_footprint_sq_ft"] != expected_footprint:
        raise ValueError("Facility footprint is inconsistent with the scale factor")
    if metrics["processing_tons_per_hour"] != expected_tph:
        raise ValueError("Processing rate is inconsistent with the scale factor")
    if metrics["processing_tons_per_8hr_shift"] != expected_shift:
        raise ValueError("Shift throughput is inconsistent with the hourly rate")
    if metrics["annual_capacity_tons_50wks"] != expected_annual:
        raise ValueError("Annual capacity is inconsistent with the stated schedule")

    acreage = config["supply_chain_requirements"]["required_contracted_acreage"]
    if not acreage["minimum"] <= acreage["target"] <= acreage["maximum"]:
        raise ValueError("Target acreage must fall within the stated range")
    if not 0 <= config["capital_stack"]["farmer_payout_guarantee_percentage"] <= 100:
        raise ValueError("Farmer payout percentage must be between 0 and 100")


def validate_copilot_design(config: dict[str, Any]) -> None:
    if config["status"] != "design_only":
        raise ValueError("Copilot integration must remain marked as design_only")
    reference = config["external_reference"]
    if reference["relationship_status"] != "public design reference only; no partnership, endorsement, access, code reuse, or affiliation is implied":
        raise ValueError("External reference must retain the non-affiliation statement")
    approval = config["approval_workflow"]
    if approval["human_in_the_loop_role"] != "Systems Administrator":
        raise ValueError("Systems Administrator must remain the HITL role")
    if "public publication" not in approval["reserved_approvals"]:
        raise ValueError("Public publication must remain a reserved approval")
    if config["credential_policy"]["repository_storage"] != "prohibited":
        raise ValueError("Repository credential storage must remain prohibited")


def main() -> int:
    micro_pilot = load_json("decortication_micro_pilot.json")
    copilot_design = load_json("copilot_creator_integration.json")
    assert_no_embedded_credentials(micro_pilot)
    assert_no_embedded_credentials(copilot_design)
    validate_micro_pilot(micro_pilot)
    validate_copilot_design(copilot_design)
    print("Project Harmony planning configuration is internally consistent and credential-free.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"Configuration validation failed: {error}", file=sys.stderr)
        raise SystemExit(1)
