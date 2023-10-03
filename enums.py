"""Module containing enumerated types"""
# Author: Daniel Davis
# Group: CSCK451 Group A
# Date: 02/10/2023

from enum import Enum


class Format(Enum):
    """Pickling Format for data dictionary"""
    # Used by Client and Server
    BINARY = 1
    JSON = 2
    XML = 3


class Source(Enum):
    """Data source format"""
    # Used by Client and Server
    Dictionary = 4
    TextFile = 8


class SecurityLevel(Enum):
    # Used by Client and Server
    UnEncrypted = 16
    Encrypted = 32


class ServerDestination(Enum):
    """Server output option"""
    # Used only by Server
    Print = 512
    File = 1024


class ServerClients(Enum):
    """Server connections option"""
    # Used only by Server
    SinglePC = 2048
    MultiPC = 4096
