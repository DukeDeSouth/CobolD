# CobolD

Verified COBOL → Python translation. Byte-perfect output matching.

## Quick start

```bash
brew install gnucobol

cd samples
cobc -x mortgage.cob && ./mortgage > expected.txt
python3 mortgage.py > actual.txt
diff expected.txt actual.txt    # zero diff, 1363 bytes = 1363 bytes
```

## Requirements

- GnuCOBOL 3.2+
- Python 3 (stdlib only)
