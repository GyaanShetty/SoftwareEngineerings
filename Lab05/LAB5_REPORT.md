# Lab 5 – Static Code Analysis

Gyaan Shetty · PES1UG24CS178 · `restaurant_order_system.py`

Scores: Pylint 4.81 → 10.00 · Bandit 5 issues (2 High, 1 Medium, 2 Low) → 0 · Flake8 9 → 0

## Issues found and fixed

| Issue | Tool / Code | Type | Line(s) | Description | Fix |
|---|---|---|---|---|---|
| Shell command execution | Bandit B605 | Security (High) | 58 | `os.system("echo ..." + filename)` allows shell injection via filename | Replaced with `print()`; no shell call |
| Weak hash | Bandit B324 | Security (High) | 47 | MD5 used for ticket hash | Switched to `hashlib.sha256` |
| Use of eval | Bandit B307 / Pylint W0123 | Security (Medium) | 42 | `eval(promo_expr)` runs arbitrary code | Takes a numeric discount %, validated 0–100 |
| Insecure RNG | Bandit B311 | Security (Low) | 51 | `random.randint` for POS PIN | `secrets.randbelow(9000) + 1000` |
| try/except/pass | Bandit B110, Flake8 E722, Pylint W0702 | Bug | 24–27 | Bare except swallowed every error silently | Catch `KeyError` only, return False |
| Hardcoded secret | Manual review | Security | 71, 80 | POS token in source and printed to stdout | Read from `POS_TERMINAL_KEY` env var; print only whether it's set |
| Mutable default arg | Pylint W0102 | Bug | 15 | `order_log=[]` shared across calls | Default `None`, init inside function |
| Unclosed file / no encoding | Pylint R1732, W1514 | Bug | 55 | `open()` without `with` or encoding | `with open(..., encoding="utf-8")` |
| Naming | Pylint C0103 | Convention | 15, 23, 30, 40 | camelCase function names | Renamed to snake_case |
| Missing docstrings | Pylint C0116 | Convention | 15–61 | No function docstrings | Added docstrings |
| `== None` | Flake8 E711, Pylint C0121 | Style | 32 | Singleton compared with `==` | `is None` |
| Unused variables/import | Flake8 F401/F841, Pylint W0611/W0612 | Maintainability | 6, 31, 41, 63 | `math`, `service_tax`, `t` unused | Removed |
| Shadowed global | Pylint W0621 | Bug risk | 61 | Param `orders` shadows module global | Renamed to `order_book` |
| Redundant if/else | Pylint R1703, R1705 | Refactor | 34–37 | if/else returning bools | `return not order["is_settled"]` |
| Long lines | Flake8 E501, Pylint C0301 | Style | 18, 19, 75 | Lines over 79 chars | Wrapped dict, shortened calls |
| Module-level call / no newline | Flake8 W292, Pylint C0304 | Style | 83 | `main()` runs on import, no final newline | `if __name__ == "__main__":` guard + newline |

## Reflection

**1. Which issues were easiest to fix, and which hardest?**
Style stuff was trivial — `is None`, unused imports, line wrapping, docstrings. The `eval()` was the hardest because removing it changes the function's interface: the caller used to pass an expression string, so I had to decide what the function actually should accept (a discount percentage) and add validation, not just delete a line.

**2. Did the tools report any false positives?**
Partly. B324 flags MD5 "for security", but the ticket hash is just an identifier, so `usedforsecurity=False` would also have been acceptable. B311 on the PIN is legit though, since a POS PIN is an access credential. Some Pylint conventions (docstrings on tiny functions) are more preference than defect.

**3. How would you integrate static analysis into a real workflow?**
Pre-commit hooks running Flake8 and Bandit locally, then the same tools plus Pylint with a score threshold (e.g. `--fail-under=9.5`) in CI on every PR, so failing checks block merges. Bandit High findings should be hard failures; style findings can just be warnings.

**4. What improvements did you see after the fixes?**
No arbitrary code execution or shell injection paths, no leaked secret, and the mutable default bug is gone (orders logged in one call no longer leak into another). Code reads more consistently — PEP 8 names, docstrings, simpler boolean logic — and the module can be imported without side effects.
