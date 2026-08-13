import json
from pathlib import Path

import yaml

from adgl.engine import Engine
from adgl.pipeline import PipelineEngine

ROOT = Path(__file__).resolve().parents[1]


def test_reference_cases():
    checked = 0
    for d in sorted((ROOT / "examples").iterdir()):
        if not d.is_dir():
            continue
        policy = d / "policy.yaml"
        inp = d / "input.json"
        exp = d / "expected.json"
        if not (policy.exists() and inp.exists() and exp.exists()):
            continue

        pol = yaml.safe_load(policy.read_text())
        expected = json.loads(exp.read_text())
        payload = json.loads(inp.read_text())

        if "knowledge_policy" in pol:
            result = PipelineEngine(pol).run(payload)
            if "decision_state" in expected:
                assert result["knowledge"]["decision_state"] == expected["decision_state"], d.name
            if "analysis_state" in expected:
                assert result["analysis"]["state"] == expected["analysis_state"], d.name
            if "consequence" in expected:
                assert result["consequence"]["disposition"] == expected["consequence"], d.name
            if "consequence_status" in expected:
                assert result["consequence"]["status"] == expected["consequence_status"], d.name
            if "path" in expected:
                assert result["consequence"].get("disposition_path") == expected["path"], d.name
            if "reason_code" in expected:
                assert result["consequence"].get("reason_code") == expected["reason_code"], d.name
        else:
            result = Engine(policy).run(payload)
            assert result["decision_state"] == expected["decision_state"], d.name
            if "admitted_ids" in expected:
                assert sorted(str(o["id"]) for o in result["admissible_objects"]) == sorted(expected["admitted_ids"]), d.name
            if "selected_model" in expected:
                assert (result["selected_model"] or {}).get("id") == expected["selected_model"], d.name
            for oid, state in expected.get("dispositions", {}).items():
                assert result["audit"]["object_dispositions"][oid] == state, (d.name, oid)

        checked += 1

    assert checked == 8
