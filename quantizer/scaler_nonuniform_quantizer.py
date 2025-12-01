import numpy as np

def make_nonuniform_table(bit_size, data, full_scale=128):#need fix
    data = np.array(data).flatten()
    data = np.clip(data, 0, full_scale - 1)

    sorted_data = np.sort(data)
    num_steps = 2 ** bit_size

    groups = np.array_split(sorted_data, num_steps)

    table = {}

    for i, group in enumerate(groups):
        low = int(group.min()) if i > 0 else 0
        high = int(group.max()) if i < num_steps-1 else full_scale - 1
        centroid = int(group.mean())
        table[(low, high)] = (i, centroid)

    return table



def nonuniform_quantizer_encode(data, bit_size, full_scale=256):
    data = np.array(data)
    encoded = np.zeros_like(data)
    table = make_nonuniform_table(bit_size,data,full_scale)

    for (low, high), (index, centroid) in table.items():
        mask = (data >= low) & (data < high)
        encoded[mask] = index

    return encoded

def nonuniform_quantizer_decode(encoded, bit_size, data, full_scale=256):
    decoded = np.zeros_like(encoded)
    table = make_nonuniform_table(bit_size,data,full_scale)

    index_to_centroid = {v[0]: v[1] for v in table.values()}

    for idx, centroid in index_to_centroid.items():
        decoded[encoded == idx] = centroid

    return decoded
if __name__ == '__main__':
    bit_size = 2

    pixels = [6, 15, 17, 60, 100, 90, 66, 59, 18, 3, 5, 16, 14, 67, 63, 2, 98, 92]

    encoded = nonuniform_quantizer_encode(pixels, bit_size, 128)
    decoded = nonuniform_quantizer_decode(encoded, bit_size,pixels ,128)

    print("Encoded:", encoded)
    print("Decoded:", decoded)
