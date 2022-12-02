# SECUREAUTH LABS. Copyright 2018 SecureAuth Corporation. All rights reserved.
#
# This software is provided under under a slightly modified version
# of the Apache Software License. See the accompanying LICENSE file
# for more information.
#
# Author: Alberto Solino (@agsolino)
#
# Description:
#   Transport implementations for the DCE/RPC protocol.
#
from __future__ import division
from __future__ import print_function

import binascii
import os
import re
import socket

try:
    from urllib.parse import urlparse, urlunparse
except ImportError:
    from urlparse import urlparse, urlunparse

from . import ntlm
from .rpcrt import DCERPCException, DCERPC_v5, DCERPC_v4

import asyncio

class DCERPCStringBinding:
    parser = re.compile(r'(?:([a-fA-F0-9-]{8}(?:-[a-fA-F0-9-]{4}){3}-[a-fA-F0-9-]{12})@)?' # UUID (opt.)
                        +'([_a-zA-Z0-9]*):' # Protocol Sequence
                        +'([^\[]*)' # Network Address (opt.)
                        +'(?:\[([^\]]*)\])?') # Endpoint and options (opt.)

    def __init__(self, stringbinding):
        match = DCERPCStringBinding.parser.match(stringbinding)
        self.__uuid = match.group(1)
        self.__ps = match.group(2)
        self.__na = match.group(3)
        options = match.group(4)
        if options:
            options = options.split(',')
            
            self.__endpoint = options[0]
            try:
                self.__endpoint.index('endpoint=')
                self.__endpoint = self.__endpoint[len('endpoint='):]
            except:
                pass

            self.__options = {}
            for option in options[1:]:
                vv = option.split('=', 1)
                self.__options[vv[0]] = vv[1] if len(vv) > 1 else ''
        else:
            self.__endpoint = ''
            self.__options = {}

    def get_uuid(self):
        return self.__uuid

    def get_protocol_sequence(self):
        return self.__ps

    def get_network_address(self):
        return self.__na

    def set_network_address(self, addr):
        self.__na = addr

    def get_endpoint(self):
        return self.__endpoint

    def get_options(self):
        return self.__options

    def get_option(self, option_name):
        return self.__options[option_name]

    def is_option_set(self, option_name):
        return option_name in self.__options

    def unset_option(self, option_name):
        del self.__options[option_name]

    def __str__(self):
        return DCERPCStringBindingCompose(self.__uuid, self.__ps, self.__na, self.__endpoint, self.__options)

def DCERPCStringBindingCompose(uuid=None, protocol_sequence='', network_address='', endpoint='', options={}):
    s = ''
    if uuid:
        s += uuid + '@'
    s += protocol_sequence + ':'
    if network_address:
        s += network_address
    if endpoint or options:
        s += '[' + endpoint
        if options:
            s += ',' + ','.join([key if str(val) == '' else "=".join([key, str(val)]) for key, val in options.items()])
        s += ']'

    return s

def DCERPCTransportFactory(stringbinding):
    sb = DCERPCStringBinding(stringbinding)

    na = sb.get_network_address()
    ps = sb.get_protocol_sequence()
    if 'ncadg_ip_udp' == ps:
        port = sb.get_endpoint()
        if port:
            rpctransport = UDPTransport(na, int(port))
        else:
            rpctransport = UDPTransport(na)
    elif 'ncacn_ip_tcp' == ps:
        port = sb.get_endpoint()
        if port:
            rpctransport = TCPTransport(na, int(port))
        else:
            rpctransport = TCPTransport(na)
    elif 'ncacn_http' == ps:
        port = sb.get_endpoint()
        if port:
            rpctransport = HTTPTransport(na, int(port))
        else:
            rpctransport = HTTPTransport(na)
    elif 'ncacn_np' == ps:
        named_pipe = sb.get_endpoint()
        if named_pipe:
            named_pipe = named_pipe[len(r'\pipe'):]
            rpctransport = SMBTransport(na, filename = named_pipe)
        else:
            rpctransport = SMBTransport(na)
    elif 'ncalocal' == ps:
        named_pipe = sb.get_endpoint()
        rpctransport = LOCALTransport(filename = named_pipe)
    else:
        raise DCERPCException("Unknown protocol sequence.")

    rpctransport.set_stringbinding(sb)
    return rpctransport

class DCERPCTransport:

    DCERPC_class = DCERPC_v5

    def __init__(self, remoteName, dstport):
        self.__remoteName = remoteName
        self.__remoteHost = remoteName
        self.__dstport = dstport
        self._stringbinding = None
        self._max_send_frag = None
        self._max_recv_frag = None
        self._domain = ''
        self._lmhash = ''
        self._nthash = ''
        self.__connect_timeout = None
        self._doKerberos = False
        self._username = ''
        self._password = ''
        self._domain   = ''
        self._aesKey   = None
        self._TGT      = None
        self._TGS      = None
        self._kdcHost  = None
        self.set_credentials('','')
        # Strict host validation - off by default and currently only for
        # SMBTransport
        self._strict_hostname_validation = False
        self._validation_allow_absent = True
        self._accepted_hostname = ''

    async def connect(self):
        raise RuntimeError('virtual function')
    async def send(self,data=0, forceWriteAndx = 0, forceRecv = 0):
        raise RuntimeError('virtual function')
    async def recv(self, forceRecv = 0, count = 0):
        raise RuntimeError('virtual function')
    def disconnect(self):
        raise RuntimeError('virtual function')
    def get_socket(self):
        raise RuntimeError('virtual function')

    def get_connect_timeout(self):
        return self.__connect_timeout
    def set_connect_timeout(self, timeout):
        self.__connect_timeout = timeout

    def getRemoteName(self):
        return self.__remoteName

    def setRemoteName(self, remoteName):
        """This method only makes sense before connection for most protocols."""
        self.__remoteName = remoteName

    def getRemoteHost(self):
        return self.__remoteHost

    def setRemoteHost(self, remoteHost):
        """This method only makes sense before connection for most protocols."""
        self.__remoteHost = remoteHost

    def get_dport(self):
        return self.__dstport
    def set_dport(self, dport):
        """This method only makes sense before connection for most protocols."""
        self.__dstport = dport

    def get_stringbinding(self):
        return self._stringbinding

    def set_stringbinding(self, stringbinding):
        self._stringbinding = stringbinding

    def get_addr(self):
        return self.getRemoteHost(), self.get_dport()
    def set_addr(self, addr):
        """This method only makes sense before connection for most protocols."""
        self.setRemoteHost(addr[0])
        self.set_dport(addr[1])

    def set_kerberos(self, flag, kdcHost = None):
        self._doKerberos = flag
        self._kdcHost = kdcHost

    def get_kerberos(self):
        return self._doKerberos

    def get_kdcHost(self):
        return self._kdcHost

    def set_max_fragment_size(self, send_fragment_size):
        # -1 is default fragment size: 0 (don't fragment)
        #  0 is don't fragment
        #    other values are max fragment size
        if send_fragment_size == -1:
            self.set_default_max_fragment_size()
        else:
            self._max_send_frag = send_fragment_size

    def set_hostname_validation(self, validate, accept_empty, hostname):
        self._strict_hostname_validation = validate
        self._validation_allow_absent = accept_empty
        self._accepted_hostname = hostname

    def set_default_max_fragment_size(self):
        # default is 0: don't fragment.
        # subclasses may override this method
        self._max_send_frag = 0

    def get_credentials(self):
        return (
            self._username,
            self._password,
            self._domain,
            self._lmhash,
            self._nthash,
            self._aesKey,
            self._TGT,
            self._TGS)

    def set_credentials(self, username, password, domain='', lmhash='', nthash='', aesKey='', TGT=None, TGS=None):
        self._username = username
        self._password = password
        self._domain   = domain
        self._aesKey   = aesKey
        self._TGT      = TGT
        self._TGS      = TGS
        if lmhash != '' or nthash != '':
            if len(lmhash) % 2:
                lmhash = '0%s' % lmhash
            if len(nthash) % 2:
                nthash = '0%s' % nthash
            try: # just in case they were converted already
               self._lmhash = binascii.unhexlify(lmhash)
               self._nthash = binascii.unhexlify(nthash)
            except:
               self._lmhash = lmhash
               self._nthash = nthash
               pass

    def doesSupportNTLMv2(self):
        # By default we'll be returning the library's default. Only on SMB Transports we might be able to know it beforehand
        return ntlm.USE_NTLMv2

    def get_dce_rpc(self):
        return DCERPC_v5(self)

class TCPTransport(DCERPCTransport):
    """Implementation of ncacn_ip_tcp protocol sequence"""

    def __init__(self, remoteName, dstport = 135):
        DCERPCTransport.__init__(self, remoteName, dstport)
        self.reader = 0
        self.writer = 0
        self.set_connect_timeout(30)

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(
        self.getRemoteHost(), self.get_dport())
        return 1

    def disconnect(self):
        try:
            self.writer.close()
        except socket.error:
            self.writer = None
            return 0
        return 1

    async def send(self,data, forceWriteAndx = 0, forceRecv = 0):
        if self._max_send_frag:
            offset = 0
            while 1:
                toSend = data[offset:offset+self._max_send_frag]
                if not toSend:
                    break
                self.writer.write(toSend)
                offset += len(toSend)
        else:
            #print('-------------- send')
            self.writer.write(data)
            #await writer.drain()

    async def recv(self, forceRecv = 0, count = 0):
        #print('-------------- recv')
        if count:
            #buffer = b''
            #while len(buffer) < count:
            #   buffer += await self.reader.read(count-len(buffer))
            buffer = await self.reader.read(count)
        else:
            buffer = await self.reader.read(8192)
        return buffer

    async def recv_fast(self):
        buffer = await self.reader.read()
        return buffer

    def get_socket(self):
        return self.writer

class LOCALTransport(DCERPCTransport):
    """
    Implementation of ncalocal protocol sequence, not the same
    as ncalrpc (I'm not doing LPC just opening the local pipe)
    """

    def __init__(self, filename = ''):
        DCERPCTransport.__init__(self, '', 0)
        self.__filename = filename
        self.__handle = 0

    def connect(self):
        if self.__filename.upper().find('PIPE') < 0:
            self.__filename = '\\PIPE\\%s' % self.__filename
        self.__handle = os.open('\\\\.\\%s' % self.__filename, os.O_RDWR|os.O_BINARY)
        return 1

    def disconnect(self):
        os.close(self.__handle)

    def send(self,data, forceWriteAndx = 0, forceRecv = 0):
        os.write(self.__handle, data)

    def recv(self, forceRecv = 0, count = 0 ):
        data = os.read(self.__handle, 65535)
        return data
