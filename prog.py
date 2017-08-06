from __future__ import print_function
import os,sys, shutil, time

from src.config import ROOT_DIR, TMP_DIR, BOOK_CHUNK_DIR, TEXT_CHUNK_DIR
from src.config import BOOK_FINAL, TEXT_FINAL, RESULT_FILE
from src.config import MAX_CHUNK_SIZE, MAX_STREAMS

from src.chunkify import chunkifyfile, chunkifydir
from src.merge import merge
from src.reduce import reduce


def usage():
    print('[usage]: python prog.py texts book\n')
    print('[where]:')
    print('- texts is a directory that contains all text files.')
    print('- book is a single text file.\n')
    print('[output]: number of times each word in texts occurs in book.\n')
    print('[note]: you might want to adjust some parameters from %s to achive better running time and memory usage if your files are too large or too small.\n' 
          % os.path.join(ROOT_DIR, 'src', 'config.py'))
    print('[test]: run python prog.py data data/t8.shakespeare.txt. To check the result on linux/mac-osx machine:')
    print("    1. run: tr 'A-Z' 'a-z' < data/t8.shakespeare.txt | tr -sc 'A-Za-z' '\\n' | sort | uniq -c > foo.")
    print('    2. check your result with foo ;)')
    print('    3. Run the program on your own big data for performance test.')

def main():
    if len(sys.argv) != 3:
        usage()
    else:
        texts = sys.argv[1]
        book = sys.argv[2]
        if not os.path.isdir(texts):
            print('directory not found: %s' % texts)
            sys.exit()
        if not os.path.isfile(book):
            print('file not found: %s' % book)
            sys.exit()
        run(texts, book)
    
        

def run(texts, book):
    # clean the tmp directory
    if os.path.isdir(TMP_DIR):
        shutil.rmtree(TMP_DIR)
    os.mkdir(TMP_DIR)
    os.mkdir(BOOK_CHUNK_DIR)
    os.mkdir(TEXT_CHUNK_DIR)
    
    start = time.time()

    # 1. chunkify the book
    print('chunkifying book: %s' %book)
    book_chunks = chunkifyfile(book, BOOK_CHUNK_DIR, MAX_CHUNK_SIZE, count_freq=True)
    print('done! all book chunks processed and saved to: %s' % book_chunks)

    # 2. merge book chunks
    print('merging book chunks')
    book_final = merge(book_chunks, BOOK_FINAL, MAX_STREAMS, count_freq=True)
    print('done! all book chunks merged and saved to: %s' %book_final)

    # 3. chunkify text files
    print('chunkifying text files: %s' % texts)
    text_chunks = chunkifydir(texts, TEXT_CHUNK_DIR, MAX_CHUNK_SIZE, count_freq=False)
    print('done! all text chunks processed and saved to: %s' % text_chunks)

    # 4. merge texts chunks
    print('merging text chunks')
    text_final = merge(text_chunks, TEXT_FINAL, MAX_STREAMS, count_freq=False)
    print('done! all text chunks merged and saved to: %s' % text_final)

    # 5. combine book_final and text_final
    print('combining')
    result = reduce(text_final, book_final, RESULT_FILE)
    print('all done! output saved to: %s' % result)

    print('Total time elapsed: {0} secs'.format(time.time() - start))

if __name__ == '__main__':
    main()
