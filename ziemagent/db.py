"""
    Agent for remote control ZIEM

    Description:
        Database module for ZIEM Agent.
        Functions for work with Mongodb.
        Logging errors and reading files.

    Author:
        Bengart Zakhar
"""

import asyncio
import logging
import motor.motor_asyncio
from cryptography.fernet import Fernet


class Database():
    """
    Class for working with MongoDB
    """
    def __init__(self):
        """
        Get access to DB
        """
        with open('/etc/opt/ziem/ziem.k', 'rb') as f:
            key = f.read()
        fern_key = Fernet(key)
        with open("/etc/opt/ziem/db", 'r') as f:
            uri = f.readline()
        self.client = motor.motor_asyncio.AsyncIOMotorClient(
            fern_key.decrypt(uri.encode()).decode())
        self.db = self.client['ziem']

    async def write(self, col, data):
        """
        Drop and write data to collection
        """
        await self.db[col].drop()
        await self.db[col].insert_many(data)
    
    async def get_db(self):
        return self.db
    
        
