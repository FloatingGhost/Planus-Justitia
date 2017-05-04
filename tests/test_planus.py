#!/usr/bin/env python3

from planus import Planus
from planus.errors import NoDocument, NoDatabase, DBClosed

from nose.tools import raises

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

@raises(NoDocument)
def test_get_nonexist():
    pln.get("nopes")

def test_update():
    pln.update("testdoc", {"updated":"document"})
    q = pln.get("testdoc")
    assert(q == {"updated":"document"})

def test_close():
    pln.close()

@raises(DBClosed)
def test_get_closed():
    pln.get("testdoc")


def test_get_reopen():
    # re-open
    pl = Planus(databaseLocation="testDB", databaseName="test")
    j = pl.get("testdoc")
    assert(j == {"updated":"document"})

