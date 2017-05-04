# Planus Justitiam

[![Build Status](https://travis-ci.org/FloatingGhost/Planus-Justitiam.svg?branch=master)](https://travis-ci.org/FloatingGhost/Planus-Justitiam)

A compressed flat-file store for when you just have too much json for your own good

Uses LZMA compression to save you some space, ya don't want gigabytes of JSON clogging up your system now, do you?

If you do I can turn it off for you.

What a weird request to make.

## Installation

```bash
git clone https://github.com/FloatingGhost/Planus-Justitiam.git planus
cd planus
sudo python3 setup.py install
```

## Usage

```python
from planus import Planus

pln = Planus(
        databaseLocation = "~/.pln",
        databaseName = "testDB")

# Store a JSON document
pln.add("document_key", {"some":"dict", "json":"y'know"})

# Retrieve a json document
pln.get("document_key")

# Update a document
pln.update("document_key", {"new":"json"})

# Remove a document
pln.remove("document_key")

# Clear the store
pln.clear()

# Close the store
pln.close()
```
