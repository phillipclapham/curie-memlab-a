# slugkit

A small library that turns text into URL slugs. A throwaway repository for trying the Curie Software Factory. Safe to delete.

```python
from slugkit import slugify

slugify("Hello, World!")                 # 'hello-world'
slugify("Posted by user@example.com")    # 'posted-by-user-example-com'
```

Run the tests with:

```bash
python -m unittest discover -s tests -v
```

## Command line

`python -m slugkit` slugs a whole list of titles without writing Python. Give
it a file of titles, one per line, and it prints one slug per line (blank
lines are skipped):

```bash
python -m slugkit titles.txt
```

With no file argument, or with `-`, titles are read from standard input.
`--sep SEP` and `--max-length N` are passed to `slugify`, and `--prefix
PREFIX` is put in front of every printed slug:

```bash
echo "Hello World" | python -m slugkit --prefix /posts/    # /posts/hello-world
```

Standard library only; Python 3.13.
