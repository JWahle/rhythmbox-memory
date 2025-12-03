# rhythmbox-memory
Rhythmbox plugin to continue the last played track on startup

## Install from GitHub
```shell
git clone https://github.com/JWahle/rhythmbox-memory.git
cd rhythmbox-memory
make install
```

## Uninstall
```shell
make uninstall
```

## Update
From within the rhythmbox-memory directory run:
```shell
make update
```

Note: The `make update` target in the Makefile runs `git pull` and then `make install` for you.

## Debug
To run Rhythmbox and show plugin-specific debug output, run:
```shell
make debug
```