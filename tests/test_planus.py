#!/usr/bin/env python3

from planus import Planus

pln = Planus(databaseLocation = "testDB", databaseName="test")

def test_repr():
    assert("PLANUS-JUSTITIAM@test" == str(pln))

def test_write():
    pass
