import os

if __name__ == '__main__':
    for ndi_type in ['bf', 'df']:
        for support in range(10, 200, 10):
            os.system(
                f'ndi/{ndi_type}/ndi data/retail-train.dat {support} 3 data/{ndi_type}-{support}.dat')
