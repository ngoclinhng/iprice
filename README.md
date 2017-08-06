# iprice technical test

Problem: Given a large number of text files with random text (doc1, doc2, …, docM), and a big text file. Find the number of times each word from the consolidated text files occurs in the book with respect to the constrain:files are big, so they probably cannot be stored in the memory.

# solution:
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


