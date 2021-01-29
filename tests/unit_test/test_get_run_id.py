#!/usr/bin/env python3
# coding: utf-8
from time import sleep

from flask.testing import FlaskClient
from flask.wrappers import Response
from py._path.local import LocalPath

from sapporo.app import create_app, handle_default_params, parse_args
from sapporo.type import RunLog


def get_run_id(client: FlaskClient, run_id: str) -> Response:  # type: ignore
    res: Response = client.get(f"/runs/{run_id}")

    return res


def test_get_run_id(delete_env_vars: None, tmpdir: LocalPath) -> None:
    args = parse_args(["--run-dir", str(tmpdir)])
    params = handle_default_params(args)
    app = create_app(params)
    app.debug = params["debug"]  # type: ignore
    app.testing = True
    client = app.test_client()

    from .test_post_runs.cwltool.test_remote_workflow import \
        post_runs_remote_workflow_with_flask
    posts_res_data = post_runs_remote_workflow_with_flask(client)
    run_id = posts_res_data["run_id"]
    sleep(3)

    res = get_run_id(client, run_id)
    res_data: RunLog = res.get_json()

    assert res.status_code == 200
    assert "run_id" in res_data
    assert run_id == res_data["run_id"]
    assert "request" in res_data
    assert "workflow_params" in res_data["request"]
    assert "workflow_type" in res_data["request"]
    assert "workflow_type_version" in res_data["request"]
    assert "tags" in res_data["request"]
    assert "workflow_engine_name" in res_data["request"]
    assert "workflow_engine_parameters" in res_data["request"]
    assert "workflow_url" in res_data["request"]
    assert "state" in res_data
    assert "run_log" in res_data
    assert "name" in res_data["run_log"]
    assert "cmd" in res_data["run_log"]
    assert "start_time" in res_data["run_log"]
    assert "end_time" in res_data["run_log"]
    assert "stdout" in res_data["run_log"]
    assert "stderr" in res_data["run_log"]
    assert "exit_code" in res_data["run_log"]
    assert "task_logs" in res_data
    assert "outputs" in res_data
