# tinytodo

A tiny persistent todo list for the terminal. One file, one JSON store
(`~/.tinytodo.json`), zero dependencies beyond the standard library.

## Usage

```bash
python tinytodo.py add "Finish project report" -p h
python tinytodo.py add "Buy milk"
python tinytodo.py list
python tinytodo.py done 1
python tinytodo.py rm 2
```
