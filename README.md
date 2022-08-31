# String verification with DFA

This is a small script that creates a DFA that verifies a list of given words. The script outputs a graphviz `.dot` file either to stdout or to a file. To render to the `.dot` file use the graphviz renderers.

Create the DFA which for the given words and write the output to a file
`python3 main.py algea coal cake coala -o graph.dot`

Render the graphviz file as svg (the dot renderer achieves the best results)
`dot -Tsvg -o graph.svg graph.dot`

Or as png
`dot -Tpng -Gdpi=300 -o graph.png graph.dot`

## Usage
```plaintext
usage: main.py [-h] [-o OUTPUT] word [word ...]

positional arguments:
  word

options:
  -h, --help  show this help message and exit
  -o OUTPUT
```
