import os

# paths
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP_DIR = os.path.join(ROOT_DIR, 'tmp')
BOOK_CHUNK_DIR = os.path.join(TMP_DIR, 'book-chunks')
TEXT_CHUNK_DIR = os.path.join(TMP_DIR, 'text-chunks')
BOOK_FINAL = os.path.join(TMP_DIR, 'book_final')
TEXT_FINAL = os.path.join(TMP_DIR, 'text_final')
RESULT_FILE = os.path.join(ROOT_DIR, 'result')

# constants
# max size of each chunk in bytes
MAX_CHUNK_SIZE = 50 * 1024 * 1024 # 20M
# max number of open file stream at a time
MAX_STREAMS = 35
# word pattern
WORD_PATTERN = '[a-zA-Z]+'
