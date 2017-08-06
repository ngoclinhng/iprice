import os

def reduce(fname1, fname2, dstfile):
    files_stream = open(fname1, 'r')
    book_stream = open(fname2, 'r')
    outstream = open(dstfile, 'w')

    i = files_stream.readline()
    j = book_stream.readline()

    if not i or not j:
        # close all streams
        files_stream.close()
        book_stream.close()
        outstream.close()
        return
    
    # reduce steps
    wi = i.split()[0]
    wj, _ = j.split()

    while True:  
        if wi == wj:
            # write to disk
            outstream.write(j)
            
            # advance file pointers
            i = files_stream.readline()
            j = book_stream.readline()
            if not i or not j:
                break
            wi = i.split()[0]
            wj, _ = j.split()

        elif wi < wj:
            while wi < wj: # advance i until wi == wj or null
                # advance i
                i = files_stream.readline()
                if not i: # done!
                    # close all streams
                    files_stream.close()
                    book_stream.close()
                    outstream.close()
                    return dstfile
                wi = i.split()[0]

        else: # wi > wj
            while wi > wj: # advance j until wj == wi or null
                j = book_stream.readline()
                if not j: # done!
                    # close all streams
                    files_stream.close()
                    book_stream.close()
                    outstream.close()
                    return dstfile
                wj, _ = j.split()
                    
    # if we reach this far, close all file streams, and done!
    files_stream.close()
    book_stream.close()
    outstream.close()
    return dstfile
