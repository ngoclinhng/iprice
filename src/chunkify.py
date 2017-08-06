import os, re
from collections import Counter

from config import WORD_PATTERN

def filechunkspool(fname, size):
    fi = open(fname)
    while 1:
        start = fi.tell()
        fi.seek(size, 1)
        line = fi.readline()
        yield fname, start, fi.tell() - start
        if not line:
            break

def dirchunkspool(dirname, size):
    files = [os.path.join(dirname, fname) for fname in os.listdir(dirname)
             if not fname.startswith('.')]
    for fname in files:
        if os.path.getsize(fname) <= size:
            yield fname, 0, os.path.getsize(fname)
        else:
            fi = open(fname)
            while 1:
                start = fi.tell()
                fi.seek(size, 1)
                line = fi.readline()
                yield fname, start, fi.tell() - start
                if not line:
                    break
        

def processchunks(dstdir, chunkslist, id, count_freq):
    data = ''
    for chunk in chunkslist:
        fi = open(chunk[0])
        fi.seek(chunk[1])
        data += fi.read(chunk[2])
        fi.close()
    words = re.findall(re.compile(WORD_PATTERN), data.lower())
    count = Counter(words).most_common()
    dstfile = os.path.join(dstdir, 'chunk_{0}'.format(id))
    fo = open(dstfile, 'w')
    for word, freq in sorted(count):
        if count_freq:
            line = '{0} {1}\n'.format(word, freq)
        else:
            line = word + '\n'
        fo.write(line)
    fo.close()

def chunkifyfile(fname, dstdir, size, count_freq):
    chunkspool = filechunkspool(fname, size)
    id = 0
    chunkslist = []
    totalsize = 0
    for chunk in chunkspool:
        chunkslist.append(chunk)
        totalsize += chunk[2]
        if totalsize >= size:
            id += 1
            processchunks(dstdir, chunkslist, id, count_freq)
            chunkslist = []
            totalsize = 0
    if totalsize > 0:
        processchunks(dstdir, chunkslist, id + 1, count_freq)
        del chunkslist
    return dstdir

def chunkifydir(dirname, dstdir, size, count_freq):
    chunkspool = dirchunkspool(dirname, size)
    id = 0
    chunkslist = []
    totalsize = 0
    for chunk in chunkspool:
        chunkslist.append(chunk)
        totalsize += chunk[2]
        if totalsize >= size:
            id += 1
            processchunks(dstdir, chunkslist, id, count_freq)
            chunkslist = []
            totalsize = 0
    if totalsize > 0:
        processchunks(dstdir, chunkslist, id + 1, count_freq)
    return dstdir
