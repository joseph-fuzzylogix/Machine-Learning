"""First-pass inventory of uploaded Excel / CSV files.

Run after placing files in data/raw/:

    python3 -m analysis.inspect_sources
"""

from __future__ import annotations

from analysis.loaders import (
    OUTPUTS_DIR,
    ROOT,
    inventory_sources,
    list_source_files,
    load_table,
    profile_dataframe,
)


def main() -> None:
    files = list_source_files()
    if not files:
        print("No source files found in data/raw/.")
        print("Upload .xlsx / .xls / .csv files there, then re-run this script.")
        return

    print(f"Found {len(files)} source file(s):")
    for path in files:
        print(f"  - {path.name}")

    inventory = inventory_sources()
    print("\n=== Source inventory ===")
    print(inventory.to_string(index=False))

    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    inventory_path = OUTPUTS_DIR / "source_inventory.csv"
    inventory.to_csv(inventory_path, index=False)
    print(f"\nWrote {inventory_path}")

    for _, row in inventory.iterrows():
        full_path = ROOT / row["file"]
        sheet = row["sheet"]
        df = load_table(full_path, sheet_name=sheet if sheet is not None else 0)
        label = full_path.stem + (f"__{sheet}" if sheet else "")
        profile = profile_dataframe(df)
        profile_path = OUTPUTS_DIR / f"profile_{label}.csv"
        profile.to_csv(profile_path, index=False)
        print(f"Wrote {profile_path}")


if __name__ == "__main__":
    main()
