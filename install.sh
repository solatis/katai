#!/usr/bin/env bash
#
# Installs katai into Claude Code from the clone this script sits in, so that
# Claude Code loads the plugin from the clone itself: an edit in the clone is
# what the next session runs.
#
#   ./install.sh              install
#   ./install.sh --uninstall  remove what install wrote

set -euo pipefail

CLONE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"

# Plans and check files of every repository live here, outside every checkout,
# so that a cleared session and a linked worktree find them.
STATE_ROOT="$HOME/.local/state/katai"

SETTINGS="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/settings.json"

fail() {
    echo "install.sh: $1" >&2
    exit 1
}

require_tools() {
    local missing=()
    local t
    for t in "$@"; do
        command -v "$t" >/dev/null 2>&1 || missing+=("$t")
    done
    [ ${#missing[@]} -eq 0 ] || fail "not on the PATH: ${missing[*]}"
}

# Adds or removes directories in permissions.additionalDirectories of the user
# settings. The stages read plans there, and the Read tool asks before every
# read outside the working directories unless the directory is listed.
edit_working_directories() {
    python3 - "$SETTINGS" "$@" <<'PY'
import json
import pathlib
import sys

settings, action, *directories = sys.argv[1:]
path = pathlib.Path(settings)
data = json.loads(path.read_text()) if path.exists() else {}
permissions = data.setdefault("permissions", {})
listed = permissions.get("additionalDirectories", [])
kept = [d for d in listed if d not in directories]
permissions["additionalDirectories"] = kept + (directories if action == "add" else [])
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(json.dumps(data, indent=2) + "\n")
PY
}

install() {
    require_tools claude git gh python3

    claude plugin install katai --marketplace "$CLONE"
    mkdir -p "$STATE_ROOT"
    edit_working_directories add "$STATE_ROOT" "$CLONE"

    echo
    echo "katai loads from $CLONE"
    echo "plans live under $STATE_ROOT"
    echo "A running session takes it after /reload-plugins."
}

uninstall() {
    require_tools claude python3

    claude plugin uninstall katai@katai
    claude plugin marketplace remove katai
    edit_working_directories remove "$STATE_ROOT" "$CLONE"

    echo
    echo "katai is removed from Claude Code."
    echo "Your plans under $STATE_ROOT and the clone $CLONE are untouched."
}

case "${1:-}" in
"") install ;;
--uninstall) uninstall ;;
*) fail "unknown argument: $1 (use no argument, or --uninstall)" ;;
esac
