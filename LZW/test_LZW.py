from My_LZW import *

text = 'ABAABABAAAAA'
print(code := lzw_encode(text))
print(lzw_decode([65, 66, 65, 256, 259, 258, 258]))