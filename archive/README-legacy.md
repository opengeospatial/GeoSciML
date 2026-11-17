# GeoSciML

GeoSciML (Geoscience Markup Language) is a GML/XML data model for the transfer
of geoscience information, developed by the IUGS Commission for the Management
and Application of Geoscience Information (CGI).

This repository additionally hosts the **OGC 16-008 GeoSciML 4.1** standard
re-encoded in **Metanorma** AsciiDoc (under [`docs/`](docs/)), so that the
official standard can be rebuilt and re-published from source rather than from
the legacy hand-produced HTML.

## Contributing

The best way to contribute is to fork this repository. David Blodgett wrote an
excellent [best-practice document to set up your environment](https://gist.github.com/dblodgett-usgs/5fe48b740392d7ecf9b87d03c6c4db6a).

---

# Building the GeoSciML 4.1 standard (Metanorma)

The Metanorma source of the standard is in [`docs/`](docs/):

| Path | Purpose |
| --- | --- |
| `docs/document.adoc` | Master file: all document metadata + `include`s |
| `docs/sections/` | Clauses 1–11, Annexes A–C, and the front matter |
| `docs/images/` | All 107 figures (PNG) referenced by the clauses |
| `docs/metanorma.yml` | Metanorma site manifest |
| `docs/STATUS.adoc` | Conversion notes and things to check on first build |

The entry point is `docs/document.adoc`. Two output shapes are useful:

* **Single document** – `metanorma compile document.adoc` produces
  `document.html` (plus `.xml`, and `.pdf`/`.doc` when fonts are present). This
  is the quickest way to preview while editing.
* **Full site** – `metanorma site generate ... .` produces a browsable site
  (`public/index.html`) and is what the CI publishes to GitHub Pages.

## Continuous integration

[`.github/workflows/metanorma-docs.yml`](.github/workflows/metanorma-docs.yml)
builds the standard on every push / pull request that touches `docs/`:

* every run attaches the rendered site to the workflow as a downloadable
  artifact (`geosciml-site`), so a branch can be previewed before merge;
* pushes to `main` / `master` additionally publish the site to **GitHub Pages**.

> **One-time setup:** in the repository, open **Settings → Pages** and set
> **Build and deployment → Source** to **GitHub Actions**. The workflow uses the
> official `metanorma/metanorma` Docker image, so no tokens or secrets are
> required.

> **Note:** this workflow replaces the two Cimas-generated placeholders
> (`generate.yml`, `docker.yml`) that shipped with the OGC template. Those ran
> `metanorma site generate` at the repository root, where there is no
> `metanorma.yml`, so they have been removed. The GitLab equivalent is kept at
> `docs/.gitlab-ci.yml` for reference and can be deleted if you are GitHub-only.

## Local build for testing

You can build the standard locally in two ways. Both produce the same output;
pick whichever matches your setup. All commands are run from the **repository
root** unless noted.

### Option A — Metanorma Docker image (recommended, works everywhere)

This needs only [Docker](https://docs.docker.com/get-docker/) — no Ruby, Java,
or fonts to install. It works on Windows, macOS, Linux, and inside WSL. The
official image bundles the entire toolchain.

Pull the image once:

```sh
docker pull metanorma/metanorma
```

**Quick single-document preview** (fastest):

```sh
# Linux / macOS / WSL (bash)
docker run --rm -v "$(pwd)/docs":/metanorma metanorma/metanorma \
  metanorma compile document.adoc
```

```powershell
# Windows PowerShell
docker run --rm -v "${PWD}\docs:/metanorma" metanorma/metanorma `
  metanorma compile document.adoc
```

Open the result at `docs/document.html`.

**Full site build** (identical to what CI publishes):

```sh
docker run --rm -v "$(pwd)/docs":/metanorma metanorma/metanorma \
  metanorma site generate --output-dir public --agree-to-terms .
```

Open the result at `docs/public/index.html`.

> The image mounts your `docs/` folder at `/metanorma` (its default working
> directory), so the build reads `document.adoc` and writes the output back into
> `docs/` on your machine.

### Option B — WSL (Ubuntu) with a native Metanorma install

Use this if you want Metanorma installed directly in WSL without Docker.

1. **Install WSL + Ubuntu** (in an elevated PowerShell on Windows), then reboot
   and finish the Ubuntu first-run user setup:

   ```powershell
   wsl --install -d Ubuntu
   ```

2. **Install the Metanorma toolchain** inside the Ubuntu shell. This installs
   Ruby, Java, fonts, and all Metanorma gems via the official setup scripts:

   ```sh
   sudo apt-get update && sudo apt-get install -y curl
   sudo bash -c "curl -L https://raw.githubusercontent.com/metanorma/metanorma-linux-setup/master/ubuntu.sh | bash"
   curl -L https://raw.githubusercontent.com/metanorma/metanorma-linux-setup/master/install-gems.sh | bash
   ```

   Verify the install:

   ```sh
   metanorma version --all
   ```

3. **Build.** Navigate to the repo (a Windows checkout is under
   `/mnt/c/...`) and build from `docs/`:

   ```sh
   cd /mnt/c/path/to/OGC-GeoSciML-metanorma/docs

   # single document
   metanorma compile document.adoc

   # or the full site
   metanorma site generate --output-dir public --agree-to-terms .
   ```

4. **Open the output** from WSL in your Windows browser:

   ```sh
   explorer.exe document.html      # or: explorer.exe public
   ```

> **Fonts / PlantUML:** the standard ships pre-rendered PNG figures, so PlantUML
> is **not** required. For on-screen HTML the default fonts are fine; the setup
> script installs fontist for higher-fidelity PDF/DOC output. Pass
> `--agree-to-terms` on the first run to accept the font licences
> non-interactively.

A native install on Ubuntu proper is identical from step 2 onward.
