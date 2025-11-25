def frequency_character(text:str):
    prob = {}
    for c in text:
        if c in prob:
            prob[c] +=1
        else:
            prob[c] = 1
    return prob

def converter(freq:dict):
    heap = []
    for k,v in freq.items():
        heap.append([v,[k,'']])
    heap = sorted(heap,reverse=True)
    return heap

def encoding(text:str,Adjheap:dict):
    answer = ''
    for c in text:
        answer+=Adjheap[c]
    return answer
def huffman(heap, length):
    count = len(heap)
    ch = ''
    for item in heap:
        value = item[0]
        reminder = length - value
        if count ==1 :
            item[1][1] = ch
            break
        if value <= reminder :
            item[1][1] = ch+'0'
            ch+='1'
        else:
            item[1][1] = ch +'1'
            ch +='0'
        count-=1
        length -= value
    AdjHeap = {}
    for item in heap:
        AdjHeap[item[1][0]] = item[1][1]
    return AdjHeap

def my_huffman_encode(text):
    length = len(text)
    prob = frequency_character(text)
    heap = converter(prob)
    AdjHeap = huffman(heap,length)
    encode = encoding(text,AdjHeap)
    return encode , AdjHeap

def my_huffman_decode(encode:str,tree:dict):
    pass

if __name__ == '__main__':
    text1 =  'BCAADDDCCACACAC'
    length = len(text1)
    text2 = "aabbbbccde"
    prob = frequency_character(text1)
    # print(prob)
    heap = converter(prob)
    # print(heap)
    AdjHeap = huffman(heap,length)
    print(AdjHeap)

