# radare2

radare2: the reverse engineering framework


## How to update

### Rawhide
* do changes primarily in the rawhide branch
* request side tag with `fedpkg request-side-tag`
* build updated package with `fedpkg build --target=fZZ-build-side-XXXXX` from the `main` branch
* build cutter-re and other dependent packages with the same command from the `main` branch
* when all builds are done, create a bodhi update with `bodhi updates new --from-tag --notes "mynotes" --user YYYYY fZZ-build-side-XXXXX`

### Stable
* wherever possible us fast-forward merge from rawhide to stable branches
```
cd fXX
fedpkg pull && git merge origin/rawhide && fedpkg push && fedpkg build
```
* create buildroot override with `fedpkg override create`
* possibly update and re-build iaito and other dependent packages with `fedpkg build` from the `fXX` branch
* when all builds are done, create a bodhi update with `bodhi updates new --type enhancement --bugs xxxxxxxx --close-bugs --notes "mynotes" radare2-nvr,iaito-nvr,...`

