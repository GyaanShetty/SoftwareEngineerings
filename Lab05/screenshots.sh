#!/usr/bin/env bash
# Walks every Lab 5 commit: runs the script + pylint/bandit/flake8 on that version.
# Screenshot the terminal at each pause. Does not change your working tree.
cd "$(git rev-parse --show-toplevel)" || exit 1
F=Lab05/restaurant_order_system.py
TMP=$(mktemp -d)
for c in $(git log --reverse --format=%h -- "$F"); do
  clear
  echo "=== $(git log -1 --format='%h  %s' "$c") ==="
  git show "$c":"$F" > "$TMP/restaurant_order_system.py"
  (cd "$TMP" && echo "--- python3 run ---" && python3 restaurant_order_system.py
   echo; echo "--- pylint ---"; pylint restaurant_order_system.py | tail -3
   echo "--- bandit ---"; bandit -q restaurant_order_system.py | grep -E 'Issue' || echo "No issues identified."
   echo "--- flake8 ---"; flake8 restaurant_order_system.py && echo "flake8 clean")
  read -rp $'\n[screenshot now, then press Enter] '
done
rm -rf "$TMP"
