# GitHub publication guide — Paper Semantic Bibliometric Toolkit v1.0

## Recommended repository

Name:

```text
paper-semantic-bibliometric-toolkit
```

Description:

```text
Reusable and auditable bibliometric toolkit for Scopus corpus validation, scientific knowledge extraction, trend analysis, Related Work selection, VOSviewer preparation, and state-of-the-art reporting.
```

## Files that should be versioned

```text
README.md
CHANGELOG.md
requirements.txt
config.example.json
config/
docs/
notebooks/
src/
tools/
thesaurus/
data/README.md
```

## Files that should remain local

```text
config.json
data/*.csv
data/*.ris
outputs/
figures/
reports/
validation/executed_notebooks/
Python environments and caches
```

## Preparation

1. Rename `README_START_HERE.md` to `README.md`.
2. Copy this `.gitignore` into the root directory.
3. Copy `config.example.json` into the root directory.
4. Keep the working `config.json` only on the local computer.
5. Copy `data/README.md` into the project data directory.
6. Add Notebook 10 to `notebooks/`.
7. Copy the official reuse manual into `docs/`.

## Initialize Git

Open PowerShell in the toolkit root:

```powershell
git init
git branch -M main
git status
```

Verify that the raw corpus is ignored:

```powershell
git check-ignore -v data/scopus_272.csv
git check-ignore -v data/scopus_export.ris
```

Create the first commit:

```powershell
git add .
git status
git commit -m "Release v1.0.0: initial stable bibliometric toolkit"
```

Before committing, confirm that no Scopus CSV/RIS file appears under “Changes to be committed”.

## Publish using GitHub Desktop

1. Open GitHub Desktop.
2. Select `File > Add local repository`.
3. Select the toolkit root folder.
4. Click `Publish repository`.
5. Use the repository name `paper-semantic-bibliometric-toolkit`.
6. Keep the repository private for the first review.
7. Publish it.

## Create the official version tag

After publishing:

```powershell
git tag -a v1.0.0 -m "Stable release v1.0.0"
git push origin v1.0.0
```

## Future updates

```powershell
git add .
git commit -m "Describe the change"
git push
```

For daily work, these same operations can be performed from GitHub Desktop using:

```text
Commit to main
Push origin
```
