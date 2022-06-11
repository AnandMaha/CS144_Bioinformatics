## Skew Algorithm -- Linear time Suffix Array construction
## Suffix Array -- sorted array of indices of all suffixes in a string ($ terminated) 

import random # produce x length string with random characters
import string
import time # measure runtime
import matplotlib.pyplot as plt # plot Runtime(s) v. Length of String

def naive_suffixArray(t): 
    """
    Suffix Array sorting all suffixes, sorted() uses timsort O(n log n)
    Total Runtime: T(n) = n^2 + n^2 log n + n^2 = O(n^2*log n)
    (n = length of t)
    """
    arr = []
    # add all suffixes to arr -- O(n^2)
    for i in range(len(t)):
        arr.append(t[i:])
    # keep arr for index matching -- O(n^2 log n) (timsort * string comparison)
    arr2 = sorted(arr)
    # index matching -- O(n^2)
    for i in range(len(t)):
        arr2[i] = arr.index(arr2[i])
    return arr2 # returns int array of positions of ordered suffixes

###### SOURCE START: https://www.geeksforgeeks.org/suffix-array-set-2-a-nlognlogn-algorithm/
###### Runtime: O(n * (log n)^2)
class suffix:
    def __init__(self):
        self.index = 0
        self.rank = [0, 0]
def geeks(txt, n):
    suffixes = [suffix() for _ in range(n)]
    for i in range(n):
        suffixes[i].index = i
        suffixes[i].rank[0] = (ord(txt[i]) -
                               ord("a"))
        suffixes[i].rank[1] = (ord(txt[i + 1]) -
                        ord("a")) if ((i + 1) < n) else -1
    suffixes = sorted(
        suffixes, key = lambda x: (
            x.rank[0], x.rank[1]))
    ind = [0] * n 
    k = 4
    while (k < 2 * n):
        rank = 0
        prev_rank = suffixes[0].rank[0]
        suffixes[0].rank[0] = rank
        ind[suffixes[0].index] = 0
        for i in range(1, n):
            if (suffixes[i].rank[0] == prev_rank and
                suffixes[i].rank[1] == suffixes[i - 1].rank[1]):
                prev_rank = suffixes[i].rank[0]
                suffixes[i].rank[0] = rank     
            else: 
                prev_rank = suffixes[i].rank[0]
                rank += 1
                suffixes[i].rank[0] = rank
            ind[suffixes[i].index] = i
        for i in range(n):
            nextindex = suffixes[i].index + k // 2
            suffixes[i].rank[1] = suffixes[ind[nextindex]].rank[0] \
                if (nextindex < n) else -1
        suffixes = sorted(
            suffixes, key = lambda x: (
                x.rank[0], x.rank[1]))
        k *= 2
    suffixArr = [0] * n
    for i in range(n):
        suffixArr[i] = suffixes[i].index
    return suffixArr
###### SOURCE END: https://www.geeksforgeeks.org/suffix-array-set-2-a-nlognlogn-algorithm/

def skew(text):
    """
    inspiration/guide: 
    https://gist.github.com/markormesher/59b990fba09972b4737e7ed66912e044
    Suffix Array construction in Linear Time -- Skew Algorithm
    Strategy: Sort 2/3 Suffixes Recursively, then merge last third of suffixes.
    Total Runtime: T(n) = T(2n/3) + O(n) = O(n) [through master theorem]
    (n = length of text)
    """
    # Convert the string into a list of ints
    # Assume the alphabet size of text is max 128 (ascii 0-127)
    return skewRecur([ord(letter) for letter in text], 128)

def skewRecur(text_arr, alpha_size):
    S12 = [i for i in range(len(text_arr)) if i % 3 != 0] # indices of 2nd and 3rd group
    
    S12 = radixSort(text_arr, alpha_size, S12) # sort the 3-prefixes from S12
    triplets = get_triplets(text_arr, S12) # to check duplicate 3-prefixes
    if len(S12) > len(triplets): # if there is at least 1 duplicate len 3 prefix in S12, recurse
        text_slice = [*(triplets[gen_triplet(text_arr, i)] for i in range(1, len(text_arr), 3)), -1,*(triplets[gen_triplet(text_arr, i)] for i in range(2, len(text_arr), 3))]
        text_slice_SufArr = skewRecur(text_slice, len(triplets) + 2) # two sentinels
        mid_sen_pos = int(len(text_slice_SufArr) / 2) # middle sentinel position
        # get proper full suffix indices from text_slice_SufArr
        S12 = [text_slice_idx(idx, mid_sen_pos) for idx in text_slice_SufArr if idx != mid_sen_pos]
    # S0 indices to merge
    # first half of S0 construction is due to how S0 indices are added 
    # when a S0 element is the last element, it won't be added to S0 with this method of construction
    S0 = ([len(text_arr) - 1] if len(text_arr) % 3 == 1 else []) + [i - 1 for i in S12 if i % 3 == 1]
    S0 = bucketSort(text_arr, alpha_size, S0, 0)
    return merge(text_arr, S0, S12)

def radixSort(text_arr, alpha_size, indices):
    # Sort 3-prefixes from 3rd letter, 2nd, then 1st in linear time
    indices = bucketSort(text_arr, alpha_size, indices, 2)
    indices = bucketSort(text_arr, alpha_size, indices, 1)
    return bucketSort(text_arr, alpha_size, indices, 0)

def bucketSort(text_arr, alpha_size, indices, offset):
    toSort = [idx_wrap(text_arr, idx + offset) for idx in indices]
    num_per_char = count_char(toSort, alpha_size)
    counts = count_total(num_per_char)
    res = [0] * len(indices)
    for idx in indices:
        letter = idx_wrap(text_arr, idx + offset)
        res[counts[letter]] = idx
        counts[letter] += 1
    return res

def idx_wrap(text_arr, i):
    return text_arr[i] if i < len(text_arr) else 0 # access text_arr in valid manner

def count_char(text_arr, alpha_size):
    # num occurrences per character
    num_per_char = [0] * alpha_size
    for letter in text_arr:
        num_per_char[letter] += 1
    return num_per_char

def count_total(num_per_char):
    # cummulative sum of all characters
    cum_sum, run_sum = [0] * len(num_per_char), 0
    for idx, num in enumerate(num_per_char):
        cum_sum[idx] = run_sum
        run_sum += num
    return cum_sum

def get_triplets(text_arr, indices):
    triplets = {}
    for idx in indices:
        triplet = gen_triplet(text_arr, idx)
        if triplet not in triplets:
            triplets[triplet] = len(triplets) + 2 # +2 to reserve sentinels ('$' and '-1')
    return triplets

def gen_triplet(text_arr, i):
    # (text_arr[i],text_arr[i+1],text_arr[i+2])
    return (idx_wrap(text_arr, i), idx_wrap(text_arr, i + 1), idx_wrap(text_arr, i + 2))

def text_slice_idx(idx, mid_sen_pos):
    # to place S1 and S2 indices back in full suffix array
    if idx < mid_sen_pos: # S1
        return 3 * idx + 1
    else: # S2
        return 3 * (idx - mid_sen_pos - 1) + 2 

def merge(text_arr, S0, S12):
    sufArr = []
    i, j = 0, 0
    while i < len(S0) and j < len(S12):
        # append the smaller letter to the suffix array
        if choose_small_suffix(text_arr, S0[i], S12[j]):
            sufArr.append(S0[i])
            i += 1
        else:
            sufArr.append(S12[j])
            j += 1
    sufArr.extend(S0[i:])
    sufArr.extend(S12[j:])
    return sufArr

def choose_small_suffix(text_arr, i, j):
    text_i, text_j = idx_wrap(text_arr, i), idx_wrap(text_arr, j)
    if text_i < text_j: 
        return True
    if text_i > text_j: 
        return False
    # if equal next character will break the tie
    return choose_small_suffix(text_arr, i+1, j+1)

alphabet = ["A","C","T","G"] 
# alt. alphabet = string.ascii_letters
lenList = [1000,2000,5000,10000,15000,20000,30000,40000,50000,80000,100000,160000,320000,640000]
max_naive_num = 40000
naive_times = []
skew_times = []
geeks_times = []
for num in lenList:
    # num random characters 
    text = ''.join((random.choice(alphabet) for i in range(num))).strip()
    text += "$" # to break suffix ties
    ## Naive -- O(n^2 * log n)
    naive_SufArr = []
    if num <= max_naive_num: # above this takes too much time
        start = time.time()
        naive_SufArr = naive_suffixArray(text)  # slow suffix array (from hw 3)                
        tot_time = time.time() - start
        naive_times.append(tot_time) # add time for plotting
        print(num,":","Naive:",tot_time)

    # Geeks -- O(n * (log n)^2)
    start = time.time()
    geeks_SufArr = geeks(text, len(text))
    tot_time = time.time() - start
    geeks_times.append(tot_time) # add time for plotting
    print(num,":","Geeks:",tot_time)
    
    ## Skew -- O(n)
    start = time.time()
    skew_SufArr = skew(text)
    tot_time = time.time() - start
    skew_times.append(tot_time) # add time for plotting
    print(num,":","Skew:",tot_time)

    # Confirm that output arrays match
    if num <= max_naive_num:
        msg = "Good job, all arrays match! ⍩" if naive_SufArr == skew_SufArr and naive_SufArr == geeks_SufArr else "Bad Job! The arrays don't match. ☹"
        print(num,":",msg,"\n")
    else:
        msg = "Good job, all arrays match! ⍩" if skew_SufArr == geeks_SufArr else "Bad Job! The arrays don't match. ☹"
        print(num,":",msg,"\n")

        
# Display Time (seconds) v. Input Size for each algorithm

# Naive
plt.scatter(lenList[:lenList.index(max_naive_num)+1], naive_times, marker="*",color="black")
plt.xlabel('Input Size of String')
plt.ylabel('Display Time (seconds)')
plt.title('Naive Algorithm O(n^2*log n)')
plt.show()

# Geeks
plt.scatter(lenList, geeks_times, marker="*",color="black")
plt.xlabel('Input Size of String')
plt.ylabel('Display Time (seconds)')
plt.title('Geeks Algorithm O(n*(log n)^2)')
plt.show()

# Skew
plt.scatter(lenList, skew_times, marker="*",color="black")
plt.xlabel('Input Size of String')
plt.ylabel('Display Time (seconds)')
plt.title('Skew Algorithm O(n)')
plt.show()    