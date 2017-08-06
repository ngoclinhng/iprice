import os

from streamsheap import streamsheap, streamsheapfreq

def merge1(streams, merged_file, count_freq):
    if count_freq:
        pq = streamsheapfreq(streams)
    else:
        pq = streamsheap(streams)
    outstream = open(merged_file, 'w')
    while not pq.isempty():
        outstream.write(pq.min() + '\n')
        idx = pq.delmin()
        for i in idx:
            line = streams[i].readline()
            if line:
                pq.insert(i, line)
    outstream.close()
    for stream in streams:
        stream.close()

def merge(dirname, dstfile, n_streams, count_freq):
    files = [os.path.join(dirname, fname) for fname in os.listdir(dirname)
             if not fname.startswith('.')]
    N = len(files)
    k = n_streams
    
    while N > k:
        merged_file = os.path.join(dirname, '{0}_{1}'.format(N, N-k+1))
        streams = map(open, files[-k:])
        merge1(streams, merged_file, count_freq)
        del files[-k:]
        files.append(merged_file)
        N = N - k + 1
    if N == 1:
        return files[0]
    else:
        streams = map(open, files)
        merge1(streams, dstfile, count_freq)
        return dstfile
        
