# Bibliographic data directory

Place the bibliographic exports for the active research project in this folder.

Expected files:

```text
data/scopus_export.csv
data/scopus_export.ris
```

The exact filenames can be changed in `config.json`.

## Important

Raw Scopus CSV and RIS exports are intentionally excluded from Git through `.gitignore`.

After cloning the repository:

1. Copy `config.example.json` to `config.json`.
2. Add the local CSV and RIS files to this directory.
3. Update the filenames and search metadata in `config.json`.
4. Execute the notebooks or the master dashboard.
