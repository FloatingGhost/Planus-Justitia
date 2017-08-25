#!/usr/bin/env python3

import json
import os
import pylzma
import hashlib
import warnings
import logging
from .errors import NoDatabase, InvalidDatabase, DBClosed, NoDocument

class Planus(object):
    """ A Flat-file JSON storage mechanism
    Useful when dealing with masses amounts of JSON

    :param databaseLocation: The database directory
    :param databaseName: The keystore we want to use, will be in a file called <name>.pln
    """

    def __init__(self, databaseLocation = "~/.planus", databaseName="db", verbose=False):
        self.log = logging.getLogger(__name__)
        self.log.info("Initilising Planus for DB %s", databaseName)

        self.databaseLocation = os.path.expanduser(databaseLocation)
        self.dbPath = os.path.join(self.databaseLocation, "{}.pln".format(databaseName))
        self.dbDocLocation = os.path.join(self.databaseLocation, databaseName) 
        self.databaseName = databaseName
        self.documentList = {}

        # Check if the database directory exists
        if not os.path.exists(self.databaseLocation):
            # This will throw an exception if we don't have write access
            self.log.debug("DB Directory doesn't exist. Creating at %s", self.databaseLocation)
            os.mkdir(self.databaseLocation)

        # Now check if the keystore exists
        if not os.path.exists(self.dbPath):
            # Try to make it if it doesn't
            self.log.debug("DB not initilised. Creating at %s...", self.dbPath)
            self._initialiseDatabase()
        else:
            # DB exists, load it up
            self.log.debug("DB Exists, loading...")
            with self._getDBHandle() as f:
                self.documentList = self._deserialise(f)
                self.log.debug("Loaded doclist %s", self.documentList)
        self.CLOSED = False

    def _serialise(self):
        """ Generate the DB index file from our doclist """

        serial = "PLJM\n"
        serial += "[DOCLIST]\n"
        for key,value in self.documentList.items():
            serial += "{}|=|{}\n".format(key, value)
        return serial

    def _deserialise(self, handle):
        if isinstance(handle, str):
            data = handle.strip()
        else:
            data = handle.read().strip()
        docs = {}
        if not data.startswith("PLJM"):
            raise InvalidDatabase("This doesn't look like a Planus file!")
        header,_,doclist = data.partition("[DOCLIST]")
        for line in filter(lambda x:x!="", doclist.split("\n")):
            key,_,value = line.partition("|=|")   
            docs[key.strip()] = value.strip()
        self.log.debug("DSRL ::  %s", docs)
        return docs

    def __repr__(self):
        return "PLANUS-JUSTITIAM@{}".format(self.databaseName)
    
    def _initialiseDatabase(self):
        """ Create the database file and all that """
        with open(self.dbPath, "w") as f:
            f.write(self._serialise())
        os.mkdir(self.dbDocLocation)
 
    def _getDBHandle(self, mode="r"):
        try:
            return open(self.dbPath, mode)
        except FileNotFoundError:
            raise NoDatabase("I can't find a DB file there - does it exist?")
    
    def _getFilenameFromJSON(self, jsonDoc : dict):
        return hashlib.sha512(json.dumps(jsonDoc).encode()).hexdigest()

    def _getAbsoluteFileLocation(self, jsonDoc : dict):
        return os.path.join(self.dbDocLocation, self._getFilenameFromJSON(jsonDoc))

    def _compressJSON(self, jsonDoc):
        return pylzma.compress(json.dumps(jsonDoc).encode())

    def _decompressJSON(self, binary):
        return json.loads(pylzma.decompress(binary).decode())

    def _writeJSON(self, jsonDoc : dict):
        """ Write the document to the database """
        fname = self._getAbsoluteFileLocation(jsonDoc)
        self.log.debug("Writing JSON at %s", fname)
        with open(fname, "wb") as f:
            f.write(self._compressJSON(jsonDoc))

    def _writeIndex(self):
        with self._getDBHandle("w") as f:
            self.log.debug("Writing DB Index %s", f)
            f.write(self._serialise())

    def clear(self):
        self.log.debug("Clearing database")
        for key in self.documentList.keys():
            self.remove(key)
        self.documentList = {}
        self._writeIndex()

    def add(self, key : str, jsonDoc : dict):
        """ Add a new JSON document to the store

        :param key: The storage key to file the document away under
        :param jsonDoc: The JSON object to store
        :rtype: bool
        """
        self.log.debug("Adding JSON doc %s", key)

        if self.CLOSED:
            raise DBClosed("Database is closed!")

        # Check if we already know the key
        if key in self.documentList:
            warnings.warn("Document key already exists. Try using update().")
            self.update(key, jsonDoc)

        # Save it to the file
        self._writeJSON(jsonDoc)

        # If that succeeded, we can add it to the document list
        fname = self._getFilenameFromJSON(jsonDoc)
        self.log.debug("Writing JSON to %s", fname)
        self.documentList[key] = fname
    
        self._writeIndex()

    def remove(self, key):
        """ Remove a document from the store

        :param key: The key to remove
        """
        self.log.debug("Removing JSON doc %s", key)

        if self.CLOSED:
            raise DBClosed("Database is closed!")

        docHash = self.documentList.get(key)
        self.log.debug("Removing hash %s", docHash)

        if not docHash:
            raise NoDocument("{} doesn't exist!".format(key))
    
        try:
            os.unlink(os.path.join(self.dbDocLocation, docHash))
        except FileNotFoundError:
            pass

    def has(self, key):
        self.log.debug("Checking if we have key %s", key)

        if self.CLOSED:               
            raise DBClosed("Database is closed!")

        docHash = self.documentList.get(key)
        if not docHash:
            return False
        return True
 
    def get(self, key):
        self.log.debug("Getting JSON doc %s", key)
        
        if self.CLOSED:
            raise DBClosed("Database is closed!")

        docHash = self.documentList.get(key)
        self.log.debug("Getting hash %s", docHash)

        if not docHash:
            self.log.info("Not found from %s", self.documentList)
            raise NoDocument("{} doesn't exist!".format(key))

        with open(os.path.join(self.dbDocLocation, docHash), "rb") as f:
            return self._decompressJSON(f.read())

    def update(self, key : str, jsonDoc : dict):
        self.log.debug("Updating JSON doc %s", key)

        if self.CLOSED:
            raise DBClosed("Database is closed!")

        docHash = self.documentList.get(key)

        if not docHash:
            self.log.debug("Couldn't find document, adding %s", key)
            self.add(key, jsonDoc)

        with open(os.path.join(self.dbDocLocation, docHash), "wb") as f:
            self.log.debug("Writing to %s", f)
            f.write(self._compressJSON(jsonDoc))

    def close(self):
        self._writeIndex()
        self.CLOSED = True
        self.log.info("Closing database.")
        self.log.info("Remember, Flat is Justice!")
        self.documentList = {}
