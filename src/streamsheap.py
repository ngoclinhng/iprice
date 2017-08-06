
class streamsheapfreq:
    def __init__(self, streams=None):
        # Number of notes in the heaps
        self.size_ = 0

        # Data structure of the heap: (stream_id,word,frequency) list
        # Note: the first item of this list is unused and it is 1-based index
        # This provides the ease of finding a note's parent, left child, right child
        self.swf_ = [None]
        
        # Initializes the heap from a list of file streams
        if streams:
            for i in range(len(streams)):
                line = streams[i].readline()
                if line:
                    self.insert(i, line)

    def isempty(self):
        return self.size_ == 0
    
    # Returns the minimum word and its total frequency in the form a string
    # 'word frequency'
    def min(self):
        if self.isempty():
            return None
        else:
            # Accumulate frequency if any
            word, freq =  self.__accumulate_freq(1)
            return word + ' ' + str(freq)

    # Takes a stream id i and a string line genrerated from this stream in which
    # line must be of the form 'word freq' and inserts them to the heap.
    # Firstly, line is splitted into (word, freq) which is in turn together with i
    # appended to the end of the __swf array.
    # The last step invokes __swim to maintain the heap invariants. 
    def insert(self, i, line):
        word, freq = line.split()
        freq = int(freq)
        self.swf_.append((i,word,freq))
        self.size_ += 1
        self.__swim(self.size_)

    # Removes and returns a list of streams that contain the minimum word from
    # the heap.
    def delmin(self):

        if self.isempty():
            return None

        _, word, _ = self.swf_[1]
        ret_streams = []

        # As long as the heap is not empty and the word at the top node
        # is equal to word we remove the top node by:
        # 1. Swap this node with the last node in the heap.
        # 2. Delete the last item from the _swf array and decrement its
        # size by 1.
        # 3. The heap invariant was probably violated by step 2, we 
        # invoke __sink to fix it.
        while self.size_ > 0 and self.swf_[1][1] == word:
            id, _, _ = self.swf_[1]
            ret_streams.append(id)
            
            self.__swap(1, self.size_)
            del self.swf_[self.size_]
            self.size_ -= 1
            self.__sink(1)

        return ret_streams
        
    
    # Assume that the heap invariant is violated at the node k because
    # k's word becomes smaller than its parent's word. We fix this by
    # moving up the heap, exchanging the node with its parent until we 
    # reach a note with smaller (or equal) parent or root.
    def __swim(self, k):
        while k > 1 and self.__less(k, k/2):
            self.__swap(k,k/2)
            k = k/2

    # Assume that the heap invariant is violated at the node k because
    # k's word becomes larger than one or both of its children's words.
    # We fix this by moving down the heap, swapping the node with the smaller
    # if its two children until we reach the node with both children larger
    # (or equal), or the bottom.
    def __sink(self, k):
        while 2*k <= self.size_:
            # left child
            j = 2*k

            # right child and smaller?
            if j < self.size_ and self.__less(j+1,j):
                j += 1
            
            # Is j's word less than k's word?
            if not self.__less(j,k):
                break
            self.__swap(k,j)
            k = j

    # Is the i's word less than j's word?
    def __less(self, i, j):
        return self.swf_[i][1] < self.swf_[j][1]
    
    # Given two nodes i, j (actually two indices into the __swf array), swap them
    def __swap(self, i, j):
        self.swf_[i], self.swf_[j] = self.swf_[j], self.swf_[i]

    # Give two nodes i, j. Does they contain the same word?
    def __equal(self, i, j):
        return self.swf_[i][1] == self.swf_[j][1]

    # Given a node that contains the word w and its frequency f, walks down the heap
    # from that node to accumulate w's frequency if any.
    def __accumulate_freq(self, k):

        word, freq = self.swf_[k][1:]

        # leaf node?
        if 2*k > self.size_:
            return word, freq
        
        # left child and equal?
        if self.__equal(k, 2*k):
            _, f = self.__accumulate_freq(2*k)
            freq += f

        # right child and equal?
        if 2*k < self.size_ and self.__equal(k, 2*k+1):
            _, f = self.__accumulate_freq(2*k+1)
            freq += f
        
        return word, freq


class streamsheap:
    ''' Most of the code is the same as StreamHeapFreq except it doesn't 
    take word frequency into account. Dubplicate anyway to avoid multiple condition
    checking.
    '''
    def __init__(self, streams=None):
        # Number of notes in the heaps
        self.size_ = 0

        # Data structure of the heap: (stream_id,word) list
        # Note: the first item of this list is unused and it is 1-based index
        # This provides the ease of finding a note's parent, left child, right child
        self.sw_ = [None]
        
        # Initializes the heap from a list of file streams
        if streams:
            for i in range(len(streams)):
                line = streams[i].readline()
                if line:
                    self.insert(i, line)

    def isempty(self):
        return self.size_ == 0
    
    # Returns the minimum word
    def min(self):
        if self.isempty():
            return None
        else:
            return self.sw_[1][1]



    # Takes a stream id i and a string line genrerated from this stream in which
    # line must be of the form 'word' and inserts them to the heap.
    # Firstly, (i,line) is appended to the end of sw_ array.
    # And then invokes __swim to maintain the heap invariants. 
    def insert(self, i, line):
        word = line.split()[0]
        self.sw_.append((i,word))
        self.size_ += 1
        self.__swim(self.size_)

    # Removes and returns a list of streams that contain the minimum word from
    # the heap.
    def delmin(self):

        if self.isempty():
            return None

        _, word= self.sw_[1]
        ret_streams = []

        # As long as the heap is not empty and the word at the top node
        # is equal to word we remove the top node by:
        # 1. Swap this node with the last node in the heap.
        # 2. Delete the last item from the _sw array and decrement its
        # size by 1.
        # 3. The heap invariant was probably violated by step 2, we 
        # invoke __sink to fix it.
        while self.size_ > 0 and self.sw_[1][1] == word:
            id, _ = self.sw_[1]
            ret_streams.append(id)
            
            self.__swap(1, self.size_)
            del self.sw_[self.size_]
            self.size_ -= 1
            self.__sink(1)

        return ret_streams
        
    
    # Assume that the heap invariant is violated at the node k because
    # k's word becomes smaller than its parent's word. We fix this by
    # moving up the heap, exchanging the node with its parent until we 
    # reach a note with smaller (or equal) parent or root.
    def __swim(self, k):
        while k > 1 and self.__less(k, k/2):
            self.__swap(k,k/2)
            k = k/2

    # Assume that the heap invariant is violated at the node k because
    # k's word becomes larger than one or both of its children's words.
    # We fix this by moving down the heap, swapping the node with the smaller
    # if its two children until we reach the node with both children larger
    # (or equal), or the bottom.
    def __sink(self, k):
        while 2*k <= self.size_:
            # left child
            j = 2*k

            # right child and smaller?
            if j < self.size_ and self.__less(j+1,j):
                j += 1
            
            # Is j's word less than k's word?
            if not self.__less(j,k):
                break
            self.__swap(k,j)
            k = j

    # Is the i's word less than j's word?
    def __less(self, i, j):
        return self.sw_[i][1] < self.sw_[j][1]
    
    # Given two nodes i, j (actually two indices into the __sw array), swap them
    def __swap(self, i, j):
        self.sw_[i], self.sw_[j] = self.sw_[j], self.sw_[i]

    # Give two nodes i, j. Does they contain the same word?
    def __equal(self, i, j):
        return self.sw_[i][1] == self.sw_[j][1]
