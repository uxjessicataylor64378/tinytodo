# tinytodo

A tiny persistent todo list for the terminal. One file, one JSON store
(`~/.tinytodo.json`), zero dependencies beyond the standard library.

## Usage

```bash
python tinytodo.py add "Finish project report" -p h
python tinytodo.py add "Buy milk"
python tinytodo.py list
python tinytodo.py list --all
python tinytodo.py done 1
python tinytodo.py undo 1
python tinytodo.py rm 2
```

Priorities are `h` / `m` / `l` (default `m`):

```
$ python tinytodo.py list
  [ ] #1   !! Finish project report
  [ ] #2    ! Buy milk

2 task(s) pending.
```

Ids stay stable: removing a task never renumbers the rest, and a store from
an older version is migrated automatically on first load.

## Storage

Tasks live in `~/.tinytodo.json` as plain JSON, so backing up or syncing the
list is just copying one file. Nothing else is written anywhere.

## License

MIT
