# Langsnapy - Tool to snapshot your LLMs, NLP Models and Chatbots

_I am looking for better name_

Idea behind this tool, is to maintain snapshots of what your model can answer.

__How it works:__ You define a set of questions. This tool run this questions against your model and save the answers. Then you can run this questions again and compare the answers with the saved ones.

### How to use

```python
```

### How to test

```sh
poetry install -E runtime-deps --with dev
poetry run pytest
```