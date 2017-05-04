import json
import os

class Planus(object):
    """ A Flat-file JSON storage mechanism
    Useful when dealing with masses amounts of JSON

    :param databaseLocation: The database directory
    :param databaseName: The keystore we want to use, will be in a file called <name>.pln
    """

    def __init__(self, databaseLocation = "~/.planus", databaseName="db"):
        
        self.databaseLocation = os.path.expanduser(databaseLocation)
        self.dbPath = os.path.join(self.databaseLocation, "{}.pln".format(databaseName))
        
        # Check if the database directory exists
        if not os.path.exists(self.databaseLocation):
            # This will throw an exception if we don't have write access
            os.mkdir(self.databaseLocation)

        # Now check if the keystore exists
        if not os.path.exists(self.dbPath):
            # Try to make it if it doesn't
            self._initialiseDatabase()
            
    def _initialiseDatabase(self):
        """ Create the database file and all that """
        pass

    def add(self, key : str, jsonDoc : dict):
        """ Add a new JSON document to the store

        :param key: The storage key to file the document away under
        :param jsonDoc: The JSON object to store
        :rtype: bool
        pass

    def remove(self, key):
        pass

    def get(self, key):
        pass
