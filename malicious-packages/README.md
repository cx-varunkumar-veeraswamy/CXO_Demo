# Malicious package manifests (SCA malicious-package detection demo)

**DO NOT INSTALL, BUILD OR RUN ANYTHING IN THIS FOLDER.**

These manifests list open-source packages/versions that were publicly reported as malicious, compromised or
protestware, so Checkmarx One SCA can flag them. They exist for static scanning only.

- No source file in this repository imports, requires or references these packages.
- No Dockerfile, compose file or CI step copies this folder or installs from it.
- `.npmrc` sets `ignore-scripts=true` as a second line of defence; never run `npm install`, `pip install` or `bundle install` here.
- Whether a given name/version is flagged depends on Checkmarx's malicious-package database at scan time.
