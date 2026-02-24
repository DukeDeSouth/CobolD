# CobolD

COBOL → Python. Byte-perfect.

Found 6 bugs in [this savings calculator](https://github.com/cchipman21804/Savings). Three were silently eating money — off by hundreds of dollars on long-term deposits. Fixed directly in COBOL.

Also translating COBOL programs to Python so both produce identical output, byte for byte.

## Verify

```bash
# Bug fix — 3 test cases, original vs fixed
cobc -x savings_verify.cob && ./savings_verify

# Translations
cobc -x mortgage.cob && ./mortgage > cobol.txt
python3 mortgage.py > python.txt
diff cobol.txt python.txt   # empty = byte-perfect

cobc -x unstring.cob && ./unstring-example > cobol.txt
python3 unstring.py > python.txt
diff cobol.txt python.txt
```

## Files

| File | Description |
|------|-------------|
| `savings_original.cob` | Original code with bugs |
| `savings_fixed.cob` | Fixed version, 6 bugs documented in header |
| `savings_verify.cob` | Side-by-side verification (3 test cases) |
| `mortgage.cob` / `.py` | 30-year mortgage amortization |
| `unstring.cob` / `.py` | COBOL UNSTRING — 6 examples, full state machine |

## Requirements

- GnuCOBOL 3.x (`brew install gnucobol` / `apt install gnucobol`)
- Python 3.8+
