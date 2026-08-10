# Machine Learning / Excel Analysis Workspace

Cursor project for requirement-driven analysis of uploaded Excel and CSV files.

## How we work

1. **Capture the ask** in [`docs/REQUIREMENTS.md`](docs/REQUIREMENTS.md)
2. **Upload source files** into [`data/raw/`](data/raw/)
3. **Document columns** in [`docs/DATA_DICTIONARY.md`](docs/DATA_DICTIONARY.md)
4. **Inspect & analyze** with scripts in [`analysis/`](analysis/) and notebooks in [`notebooks/`](notebooks/)
5. **Deliver results** to [`outputs/`](outputs/)

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt

# After uploading files to data/raw/
python3 -m analysis.inspect_sources
```

## Folder map

| Path | Purpose |
| ---- | ------- |
| `data/raw/` | Original uploads (do not edit) |
| `data/processed/` | Cleaned / joined datasets |
| `docs/` | Requirements + data dictionary |
| `analysis/` | Reusable Python analysis code |
| `notebooks/` | Exploratory notebooks |
| `outputs/` | Charts, tables, findings |

## Next step

Upload your Excel/CSV files to `data/raw/`, fill in `docs/REQUIREMENTS.md`, then ask Cursor to analyze against those requirements.
