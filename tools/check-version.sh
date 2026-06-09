#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
VERSION_FILE="${ROOT_DIR}/VERSION"
PACKAGE_JSON="${ROOT_DIR}/frontend-angular/package.json"

if [[ ! -f "${VERSION_FILE}" ]]; then
  echo "Missing VERSION file at ${VERSION_FILE}" >&2
  exit 1
fi

VERSION="$(tr -d '[:space:]' < "${VERSION_FILE}")"

if [[ ! "${VERSION}" =~ ^[0-9]+\.[0-9]+\.[0-9]+([-.][0-9A-Za-z.-]+)?$ ]]; then
  echo "VERSION must contain one semantic version, got: ${VERSION}" >&2
  exit 1
fi

failures=0

check_equals() {
  local label="$1"
  local actual="$2"

  if [[ "${actual}" != "${VERSION}" ]]; then
    echo "Version mismatch: ${label} is ${actual}, expected ${VERSION}" >&2
    failures=$((failures + 1))
  fi
}

if [[ ! -f "${PACKAGE_JSON}" ]]; then
  echo "Missing Angular package file at ${PACKAGE_JSON}" >&2
  exit 1
fi

ANGULAR_VERSION="$(
  python3 - "${PACKAGE_JSON}" <<'PY'
import json
import sys

with open(sys.argv[1], "r", encoding="utf-8") as f:
    print(json.load(f)["version"])
PY
)"
check_equals "frontend-angular/package.json version" "${ANGULAR_VERSION}"

if rg -n 'spaghetti-chef-[^[:space:]]+-release|nathabee/spaghetti-chef|spaghetti-chef.git' \
    "${ROOT_DIR}/Jenkinsfile" \
    "${ROOT_DIR}/tools/README.md" \
    "${ROOT_DIR}/tools/win" \
    "${ROOT_DIR}/tools/ops" >/dev/null; then
  echo "Found stale SpaghettiChef release references in BenchChef release tooling." >&2
  failures=$((failures + 1))
fi

if [[ "${failures}" -gt 0 ]]; then
  echo "Version check failed. Update VERSION first, then run tools/sync-version.sh." >&2
  exit 1
fi

echo "Version check passed: ${VERSION}"
