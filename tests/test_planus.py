#!/usr/bin/env python3

from planus import Planus

pln = Planus(databaseLocation = "testDB", databaseName="test")

def test_repr():
    assert("PLANUS-JUSTITIAM@test" == str(pln))

def test_serial():
    pln.documentList = {"key":"value", "anotherkey":"anothervalue"}
    expected = """PLJM
    [DOCLIST]
    key|=|value
    anotherkey|=|anothervalue
    """
    
    srl = pln._serialise()
    for line in expected.split("\n"):
        assert(line.strip() in srl)

def test_deserial():
    toDsrl = """PLJM
    [DOCLIST]
    key|=|value
    anotherkey|=|anothervalue
    """

    dsrl = pln._deserialise(toDsrl)
    assert({"key":"value", "anotherkey":"anothervalue"} == dsrl)

def test_clear():
    pln.clear()

def test_add():
    pln.add("testdoc", {"this":"is", "a":1, "document":5})

def test_get():
    j = pln.get("testdoc")
    assert(j == {"this":"is", "a":1, "document":5})
