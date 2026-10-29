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

Standard library only; Python 3.13.
