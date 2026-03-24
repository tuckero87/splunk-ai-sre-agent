from __future__ import annotations

import json
import os
from functools import cache
from pathlib import Path
from string import Template
from typing import Any

import requests
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = REPO_ROOT / "config"
CASES_DIR = REPO_ROOT / "cases"
DEFAULT_TIMEOUT = 60

type JsonValue = str | int | float | bool | None | list["JsonValue"] | dict[str, "JsonValue"]
type JsonDict = dict[str, JsonValue]
type RequestMapping = dict[str, Any]


@cache
def load_yaml_file(path: Path) -> dict[str, Any]:
    """Load a YAML file into a dictionary."""
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected a mapping in {path}")
    return data


def expand_env(value: Any) -> Any:
    """Expand ${ENV_VAR} placeholders inside strings recursively."""
    match value:
        case str():
            return Template(value).safe_substitute(os.environ)
        case list():
            return [expand_env(item) for item in value]
        case dict():
            return {key: expand_env(item) for key, item in value.items()}
        case _:
            return value


@cache
def load_targets() -> dict[str, Any]:
    """Load Splunk target configuration with environment variable expansion."""
    raw = load_yaml_file(CONFIG_DIR / "splunk_targets.yaml")
    return expand_env(raw)


@cache
def load_policy() -> dict[str, Any]:
    """Load the local agent policy file."""
    raw = load_yaml_file(CONFIG_DIR / "agent_policy.yaml")
    return expand_env(raw)


def clear_config_caches() -> None:
    """Clear cached configuration reads."""
    load_yaml_file.cache_clear()
    load_targets.cache_clear()
    load_policy.cache_clear()


def load_target(name: str) -> dict[str, Any]:
    """Return the target configuration for a named Splunk target."""
    targets = load_targets()
    if name not in targets:
        available = ", ".join(sorted(targets))
        raise KeyError(f"Unknown target '{name}'. Available targets: {available}")
    return targets[name]


def coerce_bool(value: Any, default: bool = True) -> bool:
    """Interpret common string forms of booleans."""
    match value:
        case None:
            return default
        case bool():
            return value
        case str():
            return value.strip().lower() in {"1", "true", "yes", "on"}
        case _:
            return bool(value)


def request_json(
    target_name: str,
    method: str,
    path: str,
    *,
    params: RequestMapping | None = None,
    data: RequestMapping | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> JsonDict:
    """Perform a JSON request to the Splunk management API."""
    target = load_target(target_name)
    base_url = str(target["base_url"]).rstrip("/")
    url = f"{base_url}{path}"
    verify_ssl = coerce_bool(target.get("verify_ssl"), default=True)

    headers: dict[str, str] = {"Accept": "application/json"}
    auth_block = target.get("auth", {}) or {}
    auth = None

    token = auth_block.get("token")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    else:
        username = auth_block.get("username")
        password = auth_block.get("password")
        if username and password:
            auth = (username, password)
        else:
            raise ValueError(
                f"Target '{target_name}' does not provide either a bearer token or basic auth credentials."
            )

    response = requests.request(
        method=method.upper(),
        url=url,
        headers=headers,
        params=params,
        data=data,
        auth=auth,
        verify=verify_ssl,
        timeout=timeout,
    )
    response.raise_for_status()
    if not response.content:
        return {}

    payload = response.json()
    if not isinstance(payload, dict):
        raise ValueError(f"Expected a JSON object response from {url}")
    return payload


def dump_json(path: Path, payload: JsonDict) -> None:
    """Write a dictionary to disk as pretty JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=False)
        handle.write("\n")
