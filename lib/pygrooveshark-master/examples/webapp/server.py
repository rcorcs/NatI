# -*- coding:utf-8 -*-

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os.path
import time
import json
import threading
from wsgiref.util import FileWrapper

from pyweb.core.server import simple_server
from pyweb.core.application import Application
from pyweb.handlers.directory import Directory

from grooveshark import Client
from grooveshark.classes.song import Song

class Cache():
    STATE_READING = 0
    STATE_FINISHED = 1
    STATE_CANCELED = 2
    def __init__(self, fileobj, size, blocksize=2048):
        self._fileobj = fileobj
        self.size = size
        self._blocksize = blocksize
        self.state = self.STATE_READING
        self._memory = []
        self._current = 0
        self._active = True
        self.bytes_read = 0
        self._read_thread = threading.Thread(target=self._read)
        self._read_thread.start()
        
    def _read(self):
        data = self._fileobj.read(self._blocksize)
        while data and self._active:
            self._memory.append(data)
            self.bytes_read += len(data)
            data = self._fileobj.read(self._blocksize)
        if self._active:
            self.state = self.STATE_FINISHED
        self._fileobj.close()
    
    def reset(self):
        self._current = 0
        
    @property
    def offset(self):
        return self._current
    
    @offset.setter
    def offset(self, offset):
        self._current = offset
    
    def cancel(self):
        if self.state == self.STATE_READING:
            self._active = False
            self.state = self.STATE_CANCELED
        
    def read(self, size=None):
        start_block, start_bytes = divmod(self._current, self._blocksize)
        if size:
            if size > self.size - self._current:
                size = self.size - self._current
            while self._current + size > self.bytes_read:
                time.sleep(0.01)
            self._current += size
            end_block, end_bytes = divmod(self._current, self._blocksize)
            result = self._memory[start_block:end_block]
        else:
            while self.size > self.bytes_read:
                time.sleep(0.01)
            self._current = self.size
            result = self._memory[start_block:]
        if size:
            if end_bytes > 0 :
                result.append(self._memory[end_block][:end_bytes])
        if start_bytes > 0 and result:
            result[0] = result[0][start_bytes:]
        return b''.join(result)

class Grooveshark(Application):
    __URLS__ = {'/desktop/.*|/icons/.*' : 'www',
                '/request/popular' : 'popular',
                '/request/search' : 'search',
                '/request/stream' :  'stream'}
    www = Directory(os.path.join(os.path.dirname(__file__), 'www'))
    def __init__(self):
        super().__init__()
        self.client = Client()
        self.client.init()
        self._cache = {}
        self._cache['streams'] = {}     
    
    def _respond_json(self, data, response):
        response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        response.body.append(json.dumps(data).encode('utf-8'))
    
    def _bad_request(self, message, response):
        response.status = 400
        response.message = 'ERROR'
        response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        response.body.append(json.dumps({'status' : 'error', 'result' : message}).encode('utf-8'))
    
    def popular(self, request, response):
        if not 'popular' in self._cache:
            self._cache['popular'] =  (time.time(), [song.export() for song in self.client.popular()])
        if time.time() - self._cache['popular'][0] > 7200:
            self._cache['popular'] =  (time.time(), [song.export() for song in self.client.popular()])
        self._respond_json({'status' : 'success', 'result' : self._cache['popular'][1]}, response)
    
    def search(self, request, response):
        if not 'type' in request.query:
            request.qery['type'] = [SEARCH_TYPE_SONGS]
        if 'query' in request.query:
            if not request.query['type'][0] in (Client.SONGS,
                                                Client.ALBUMS,
                                                Client.ARTISTS):
                self._bad_request('unknown type', response)
            else:
                result = [object.export() for object in self.client.search(request.query['query'][0], request.query['type'][0])]
                self._respond_json({'status' : 'success', 'result' : result}, response)
        else:
            self._bad_request('missing query argument', response)
    
    def stream(self, request, response):
        song = Song.from_export(json.loads(request.query['song'][0]), self.client.connection)
        if song.id in self._cache['streams']:
            stream, cache = self._cache['streams'][song.id]
        else:
            stream = song.stream
            cache = Cache(stream.data, stream.size)
            self._cache['streams'][song.id] = stream, cache
        if 'Range' in request.headers:
            response.status = 206
            start_byte, end_byte = request.headers['Range'].replace('bytes=', '').split('-')
            if start_byte:
                start_byte = int(start_byte)
            else:
                start_byte = 0
            if end_byte:
                end_byte = int(end_byte)
            else:
                end_byte = stream.size
            cache.offset = start_byte
            if 'download' in request.query:
                response.headers['Content-Disposition'] = 'attachment; filename="{} - {} - {}.mp3"'.format(song.name, song.album.name, song.artist.name)
            response.headers['Accept-Ranges'] = 'bytes'
            response.headers['Content-Type'] = stream.data.info()['Content-Type']
            response.headers['Content-Length'] = str(stream.size)
            response.headers['Content-Range'] = 'bytes {}-{}/{}'.format(start_byte, end_byte, stream.size)
            response.body = FileWrapper(cache)
        else:
            cache.reset()
            if 'download' in request.query:
                response.headers['Content-Disposition'] = 'attachment; filename="{} - {} - {}.mp3"'.format(song.name, song.album.name, song.artist.name)
            response.headers['Accept-Ranges'] = 'bytes'
            response.headers['Content-Type'] = stream.data.info()['Content-Type']
            response.headers['Content-Length'] = str(stream.size)
            response.body = FileWrapper(cache)
    
if __name__ == '__main__':
    simple_server(Grooveshark())
    

