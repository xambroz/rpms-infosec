# rizin

The rizin package

## How to update

### Rawhide
* request side tag with `fedpkg request-side-tag`
* build updated package with `fedpkg build --target=fZZ-build-side-XXXXX` from the `main` branch
* build cutter-re and other dependent packages with the same command from the `main` branch
* when all builds are done, create a bodhi update with `bodhi updates new --from-tag --notes "mynotes" --user YYYYY fZZ-build-side-XXXXX`

### Stable
* build update package with `fedpkg build` from the `fXX` branch
* create buildroot override with `bodhi overrides save <rizin-nvr>`
* build cutter-re and other dependent packages with `fedpkg build` from the `fXX` branch
* when all builds are done, create a bodhi update with `bodhi updates new --type enhancement --bugs xxxxxxxx --close-bugs --notes "mynotes" <rizin-nvr>,<cutter-re-nvr>,...`
