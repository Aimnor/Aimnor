This repo is used to both serve as presentation and CV generator.

# Requirements
Is is meant to be used on Linux (debian based) with python 3

# Installation

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# Execution

```bash
python -m venv venv
rendercv render "Marion_FABRE_CV.yaml" --dont-generate-html --dont-generate-png --dont-generate-typst
```


# Dirty fix

Link in highlights are not properly rendered in markdown, in order to fix it, you can use the built-in regexp of vscode to fix it.

find filed:
`#link\("(.*)"\)\[(.*)\]`

replace field:
`[$2]($1)`