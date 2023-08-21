from BitHash import BitHash
from BitVector import BitVector

# d is the number of hash functions
# n keys to be inserted
class BloomFilter(object):
    # Return the estimated number of bits needed (N)in a Bloom 
    # Filter that will store numKeys (n) keys, using numHashes 
    # (d) hash functions, and that will have a
    # false positive rate of maxFalsePositive 
    
    def __bitsNeeded(self, numKeys, numHashes, maxFalse):
        
        phi = 1 - (maxFalse ** (1/numHashes))
        
        N = numHashes / (1 - phi ** (1/numKeys))
        
        # return N which is the number of bits needed with all the criteria to keep a false positive rate of maxFalse
        return int(N)
    
    # wrapper method for __bitsNeeded
    def bitsNeeded(self):
        return self.__bitsNeeded(self.__numKeys, self.__numHashes, self.__maxFalsePositive)
    
    def __init__(self, numKeys, numHashes, maxFalsePositive):
        # n - the number of keys
        self.__numKeys = numKeys
        # d - the number of hash functions used
        self.__numHashes = numHashes
        # P -  the max false positive rate
        self.__maxFalsePositive = maxFalsePositive  
        
        # will need to use __bitsNeeded to figure out how big
        # of a BitVector will be needed
        self.__theVector = BitVector(size = self.bitsNeeded())
        
        self.__numKeysSet = 0
        
    
    # insert the specified key into the Bloom Filter.
    # Doesn't return anything, since an insert into 
    # a Bloom Filter always succeeds!
    def insert(self, key):
        
        # for each hash funtion
        for i in range(1, self.__numHashes + 1):
            # store where the key hashes to in temp
            temp = BitHash(key, i) % self.bitsNeeded()
            # if the bit wasn't previoiusly set
            if self.__theVector[temp] == 0:
                # set that bit to 1
                self.__theVector[temp] = 1
                # increment the keys so far 
                self.__numKeysSet += 1
    
    # Returns True if key MAY have been inserted into the Bloom filter. 
    # Returns False if key definitely hasn't been inserted into the BF.
    def find(self, key):
        
        # for each hash function
        for i in range(1, self.__numHashes + 1):
            # if any of those bits are not set to 1, the key has definitely not been inserted into the Bloom filter
            temp = BitHash(key, i) % self.bitsNeeded()
            # if that bit is not 1 (not set)
            if self.__theVector[temp] != 1:
                # the key has definitely not been inserted
                return False
        # otherwise we fall out of the loop and all of them are 1 so key may be in filter
        return True
       
    # Returns the PROJECTED current false positive rate based on the
    # ACTUAL current number of bits actually set in this Bloom Filter. 
    def falsePositiveRate(self):
        
        # actual current proportion of bits in the bit vector that are still 0
        # (total bits - set bits) / total bits
        phi = (self.bitsNeeded() - self.numBitsSet()) / self.bitsNeeded()
        
        # then use equation A to get the projected current false positive rate
        P = (1 - phi) ** self.__numHashes
        return P
       
    # Returns the current number of bits ACTUALLY set in this Bloom Filter
    def numBitsSet(self):
        return self.__numKeysSet
       

def __main():
    numKeys = 100000
    numHashes = 4
    maxFalse = .05
    
    # create the Bloom Filter
    
    b = BloomFilter(numKeys, numHashes, maxFalse)
    
    
    # open the file
    fin = open("wordlist.txt")
    
    # read the first numKeys words from the file and insert them 
    line = fin.readline()
    # variable for the loop
    count = 0
    # while count is less than number of keys being inserted
    while count < numKeys:
        # insert the new word
        b.insert(line)
        # go to the next
        line = fin.readline()
        # increment the count
        count += 1
    
    # close the file
    fin.close()
        
    # Print out what the PROJECTED false positive rate should 
    # THEORETICALLY be based on the number of bits that ACTUALLY ended up being set
    # in the Bloom Filter.
    print("The PROJECTED false positive rate is: " + str(b.falsePositiveRate()))

    # re-open the file, and re-read the same bunch of the first numKeys 
    # words from the file and count how many are missing from the Bloom Filter, 
    # there should be 0 missing
    # printing out how many are missing. This should report that 0 words are 
    # missing from the Bloom Filter. Don't close the input file of words since
    # in the next step we want to read the next numKeys words from the file.
    fin = open("wordlist.txt")
    line = fin.readline()
    # count for the loop
    count2 = 0
    # how many keys are not in the bloom filter
    notIn = 0
    # go through 100000 keys
    while count2 < numKeys:
        # check if the key is in the Bloom Filter
        # if it isn't, in the filter, increment notIn by 1
        if b.find(line) == False: notIn += 1
        # go to the next word
        line = fin.readline()
        # increment the count
        count2 += 1
    print("There are " + str(notIn) + " keys missing from the Bloom Filter! (should be 0)") 
    

    # Now read the next numKeys words from the file, none of which 
    # have been inserted into the Bloom Filter, and count how many of the 
    # words can be (falsely) found in the Bloom Filter.
    # now line should be the 100,00th so now just do another 100,000 and should be the next words that haven't encountered yet
    # count for the loop
    count3 = 0
    # how many keys are falsely found to be in the bloom filter
    falseIn = 0
    # loop through next 100000 words
    while count3 < numKeys:
        if b.find(line) == True: falseIn += 1
        # go to the next word
        line = fin.readline()
        # increment the loop count
        count3 += 1
    
    # close the file
    fin.close()
    
    
        
    # Print out the percentage rate of false positives. This number is close 
    # to the estimated false positive rate above
    print("The ACTUAL false positive rate is: " + str(falseIn/100000))
    
    
    
if __name__ == '__main__':
    
    __main()       

