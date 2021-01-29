#!/usr/bin/env python3
# coding: utf-8
import json
import shlex
import subprocess
from time import sleep

from sapporo.type import RunId

from . import SCRIPT_DIR, TEST_HOST, TEST_PORT  # type: ignore


def post_runs_str_input() -> RunId:
    script_path = SCRIPT_DIR.joinpath("str_input/post_runs.sh")
    proc = subprocess.run(shlex.split(f"/bin/bash {str(script_path)}"),
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,

                          encoding="utf-8",
                          env={"SAPPORO_HOST": TEST_HOST,
                               "SAPPORO_PORT": TEST_PORT})
    assert proc.returncode == 0
    res_data: RunId = json.loads(proc.stdout)

    return res_data


def test_str_input(setup_test_server: None) -> None:
    res_data = post_runs_str_input()
    assert "run_id" in res_data
    run_id = res_data["run_id"]

    from .. import get_run_id_status
    count = 0
    while count <= 120:
        get_status_data = get_run_id_status(run_id)
        if str(get_status_data["state"]) == "COMPLETE":
            break
        sleep(1)
        count += 1
    assert str(get_status_data["state"]) == "COMPLETE"

    from .. import get_run_id
    data = get_run_id(run_id)

    assert any(["test_output.txt" in key for key in data["outputs"].keys()])
    assert data["request"]["tags"] == "{}"
    assert any(["str_input.nf" in obj["file_name"]
                for obj in data["request"]["workflow_attachment"]])
    assert data["request"]["workflow_engine_name"] == "nextflow"
    assert data["request"]["workflow_engine_parameters"] == "{}"
    assert data["request"]["workflow_name"] == "str_input.nf"
    assert data["request"]["workflow_params"] == \
        "{\n  \"str\": \"sapporo-nextflow-str-input\"\n}\n"
    assert data["request"]["workflow_type"] == "Nextflow"
    assert data["request"]["workflow_type_version"] == "v1.0"
    assert data["request"]["workflow_url"] == "./str_input.nf"
    assert data["run_id"] == run_id
    assert data["run_log"]["exit_code"] == 0
    assert data["run_log"]["name"] == "str_input.nf"
    assert "[100%] 1 of 1" in data["run_log"]["stdout"]
    assert str(data["state"]) == "COMPLETE"
    assert data["task_logs"] is None
