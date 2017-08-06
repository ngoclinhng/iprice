# iprice technical test

Problem: Given a large number of text files with random text (doc1, doc2, …, docM), and a big text file. Find the number of times each word from the consolidated text files occurs in the book with respect to the constrain:files are big, so they probably cannot be stored in the memory.

# solution:
run ```python prog.p text-files-directory book-file```, where ```text-files-directory``` is the directory that contains all text files and ```book-file``` is a single text file representing the book. The output of the above will be save at the current directory with name `result`

if your files are too small or too big you might want to adjust ```MAX_CHUNK_SIZE``` and ```MAX_STREAMS``` in the ```src/prog.py``` file. You can also change ```word``` definition by change the ```WORD_PATTERN``` there.

```run python prog.py``` for more information

Python 2.7.10

Machine: Mac-OSX

Dependencies: None

# for performance test
book: [plot.list.gz](http://ftp.sunet.se/mirror/archive/ftp.sunet.se/pub/tv+movies/imdb/)

texts: [gzipped tar archive](http://www.daviddlewis.com/resources/testcollections/reuters21578/)

Use [this program](https://github.com/manishkanadje/reuters-21578/blob/master/ExtractReuters.java) to extract texts

After extraction:

- book: plot.list (365M, one file)

- texts: 90M, 21,579 files


