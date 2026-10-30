# slugkit

A small library that turns text into URL slugs. A throwaway repository for trying the Curie Software Factory. Safe to delete.

```python
from slugkit import load_aliases, slugify

slugify("Hello, World!")                 # 'hello-world'
slugify("Posted by user@example.com")    # 'posted-by-user-example-com'
slugify("C++ & Rust", aliases={"c++": "cpp", "&": "and"})    # 'cpp-and-rust'
slugify("C++ & Rust", aliases=load_aliases("aliases.txt"))   # 'cpp-and-rust'
```

Run the tests with:

```bash
python -m unittest discover -s tests -v
```

Standard library only; Python 3.13.
