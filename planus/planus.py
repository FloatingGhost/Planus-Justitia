#!/usr/bin/env python3

import json
import os
import pylzma
import hashlib
from .errors import NoDatabase

class Planus(object):
    """ A Flat-file JSON storage mechanism
    Useful when dealing with masses amounts of JSON

    :param databaseLocation: The database directory
    :param databaseName: The keystore we want to use, will be in a file called <name>.pln
    """

    def __init__(self, databaseLocation = "~/.planus", databaseName="db"):
        
        self.databaseLocation = os.path.expanduser(databaseLocation)
        self.dbPath = os.path.join(self.databaseLocation, "{}.pln".format(databaseName))
        self.dbDocLocation = os.path.join(self.databaseLocation, databaseName) 
        self.databaseName = databaseName

        # Check if the database directory exists
        if not os.path.exists(self.databaseLocation):
            # This will throw an exception if we don't have write access
            os.mkdir(self.databaseLocation)

        # Now check if the keystore exists
        if not os.path.exists(self.dbPath):
            # Try to make it if it doesn't
            self._initialiseDatabase()
        
    def __repr__(self):
        return "PLANUS-JUSTITIAM@{}".format(self.databaseName)
    
    def _initialiseDatabase(self):
        """ Create the database file and all that """
        pass 
      
    def _getDBHandle(self):
        try:
            return open(self.dbPath, "r")
        except FileNotFoundError:
            raise NoDatabase("I can't find a DB file there - does it exist?")
    
    def _getFilenameFromJSON(self, jsonDoc : dict):
        return hashlib.sha512(json.dumps(jsonDoc).encode()).hexdigest()

    def _getAbsoluteFileLocation(self, jsonDoc : dict):
        return os.path.join(self.dbDocLocation, self._getFilenameFromJSON(jsonDoc))

    def _writeJSON(self, jsonDoc : dict):
        """ Write the document to the database """
        fname = self._getAbsoluteFileLocation(jsonDoc)
        
                
    def add(self, key : str, jsonDoc : dict):
        """ Add a new JSON document to the store

        :param key: The storage key to file the document away under
        :param jsonDoc: The JSON object to store
        :rtype: bool
        """
        pass

    def remove(self, key):
        pass

    def get(self, key):
        pass

    def update(self, key):
        pass
