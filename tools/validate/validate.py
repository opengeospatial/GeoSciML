#!/usr/bin/env python3
"""
Validate GeoSciML JSON examples against their schemas.

Directory → schema mapping:
  examples/json/4.1/basic/                     → geoscimlBasic.json
  examples/json/4.1/lite/                      → geoscimlLite.json
  examples/json/4.1/featurecollections/basic/  → geosciml_basic_featurecollection.json
  examples/json/4.1/featurecollections/lite/   → geosciml_lite_featurecollection.json

For individual features the validator is narrowed to the $anchor matching the
instance's "featureType" property (e.g. #GeologicUnit within geoscimlBasic.json).
Feature-collection schemas have a top-level $ref so they are validated as-is.

Remote schemas (json-fg, sweCommon, …) are fetched once and cached under
.schema_cache/ in the project root.
"""

import json
import sys
import urllib.request
import urllib.error
from pathlib import Path

from jsonschema import Draft202012Validator
import referencing
from referencing import Registry
from referencing.jsonschema import DRAFT202012

# ── paths ─────────────────────────────────────────────────────────────────────

ROOT = Path(__file__).parent
SCHEMA_DIR = ROOT / "schemas" / "json" / "4.1"
EXAMPLES_DIR = ROOT / "examples" / "json" / "4.1"
CACHE_DIR = ROOT / ".schema_cache"

# ── directory → schema $id ────────────────────────────────────────────────────

_BASE = "https://ext.iide.dev/schemas/geosciml/json/4.1"

DIR_SCHEMA: dict[Path, str] = {
    EXAMPLES_DIR / "basic":                                         f"{_BASE}/geoscimlBasic.json",
    EXAMPLES_DIR / "lite":                                          f"{_BASE}/geoscimlLite.json",
    EXAMPLES_DIR / "borehole":                                      f"{_BASE}/borehole.json",
    EXAMPLES_DIR / "geologicTime":                                  f"{_BASE}/geologicTime.json",
    EXAMPLES_DIR / "geoscimlExtension":                             f"{_BASE}/geoscimlExtension.json",
    EXAMPLES_DIR / "laboratoryAnalysisSpecimen":                    f"{_BASE}/laboratoryAnalysisSpecimen.json",
    EXAMPLES_DIR / "featurecollections/basic":                      f"{_BASE}/geosciml_basic_featurecollection.json",
    EXAMPLES_DIR / "featurecollections/lite":                       f"{_BASE}/geosciml_lite_featurecollection.json",
    EXAMPLES_DIR / "featurecollections/geologicTime":               f"{_BASE}/geosciml_geologictime_featurecollection.json",
    EXAMPLES_DIR / "featurecollections/geoscimlExtension":          f"{_BASE}/geosciml_extension_featurecollection.json",
    EXAMPLES_DIR / "featurecollections/laboratoryAnalysisSpecimen": f"{_BASE}/geosciml_laboratoryanalysisspecimen_featurecollection.json",
}

# ── ANSI colours ──────────────────────────────────────────────────────────────

_USE_COLOUR = sys.stdout.isatty()

def _green(s: str) -> str:  return f"\033[32m{s}\033[0m" if _USE_COLOUR else s
def _red(s: str) -> str:    return f"\033[31m{s}\033[0m" if _USE_COLOUR else s
def _yellow(s: str) -> str: return f"\033[33m{s}\033[0m" if _USE_COLOUR else s
def _bold(s: str) -> str:   return f"\033[1m{s}\033[0m"  if _USE_COLOUR else s

# ── schema registry ───────────────────────────────────────────────────────────

def _load_local_schemas() -> list[tuple[str, referencing.Resource]]:
    resources = []
    for path in SCHEMA_DIR.glob("*.json"):
        schema = json.loads(path.read_text(encoding="utf-8"))
        sid = schema.get("$id")
        if sid:
            resources.append((sid, DRAFT202012.create_resource(schema)))
    return resources


_remote_cache: dict[str, referencing.Resource] = {}


def _retrieve(uri: str) -> referencing.Resource:
    """Fetch a remote schema, using a local file cache."""
    if uri in _remote_cache:
        return _remote_cache[uri]

    # file-based cache
    safe_name = uri.replace("://", "_").replace("/", "_").replace("?", "_")
    cache_file = CACHE_DIR / safe_name
    if cache_file.exists():
        contents = json.loads(cache_file.read_text(encoding="utf-8"))
    else:
        try:
            with urllib.request.urlopen(uri, timeout=15) as resp:
                contents = json.loads(resp.read())
            CACHE_DIR.mkdir(exist_ok=True)
            cache_file.write_text(json.dumps(contents))
        except urllib.error.URLError as exc:
            raise referencing.exceptions.NoSuchResource(ref=uri) from exc

    resource = referencing.Resource.from_contents(contents)
    _remote_cache[uri] = resource
    return resource


def build_registry() -> Registry:
    return Registry(retrieve=_retrieve).with_resources(_load_local_schemas())


# ── validation ────────────────────────────────────────────────────────────────

def _validator_schema(instance: dict, schema_id: str, is_collection: bool) -> dict:
    """
    Return the JSON Schema object to validate *instance* against.

    For feature collections the schema already has a top-level $ref so we
    just point at the schema URI.  For individual features we narrow to the
    $anchor that matches the instance's featureType.
    """
    if is_collection:
        return {"$ref": schema_id}

    feature_type = instance.get("featureType")
    if feature_type:
        return {"$ref": f"{schema_id}#{feature_type}"}
    return {"$ref": schema_id}


def validate_file(
    path: Path,
    schema_id: str,
    is_collection: bool,
    registry: Registry,
) -> list[str]:
    """Return validation error messages; empty list means valid."""
    try:
        instance = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"JSON parse error: {exc}"]

    vs = _validator_schema(instance, schema_id, is_collection)
    validator = Draft202012Validator(vs, registry=registry)
    errors = sorted(validator.iter_errors(instance), key=lambda e: str(e.absolute_path))
    return [
        ("{} → {}".format("/".join(str(p) for p in e.absolute_path), e.message)
         if e.absolute_path else e.message)
        for e in errors
    ]


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    registry = build_registry()

    passed = failed = skipped = 0

    for example_dir, schema_id in sorted(DIR_SCHEMA.items(), key=lambda kv: str(kv[0])):
        if not example_dir.exists():
            print(_yellow(f"  skip  {example_dir.relative_to(ROOT)}  (directory not found)"))
            continue

        is_collection = "featurecollections" in str(example_dir)
        files = sorted(example_dir.glob("*.json"))
        if not files:
            continue

        schema_label = schema_id.split("/")[-1]
        print(_bold(f"\n{example_dir.relative_to(EXAMPLES_DIR)}  →  {schema_label}"))

        for path in files:
            label = path.relative_to(ROOT)
            try:
                errors = validate_file(path, schema_id, is_collection, registry)
            except referencing.exceptions.NoSuchResource as exc:
                print(f"  {_yellow('SKIP')}  {label}  (unresolvable ref: {exc})")
                skipped += 1
                continue

            if errors:
                print(f"  {_red('FAIL')}  {label}")
                for msg in errors:
                    print(f"         {msg}")
                failed += 1
            else:
                print(f"  {_green('OK')}    {label}")
                passed += 1

    total = passed + failed + skipped
    print(
        f"\n{_bold('Results:')}  "
        f"{_green(str(passed))} passed, "
        f"{_red(str(failed))} failed, "
        f"{_yellow(str(skipped))} skipped  "
        f"({total} total)"
    )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
