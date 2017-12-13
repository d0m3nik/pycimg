if __name__ == '__main__':
    with open('./src/pycimg_template.pyx') as f:
        code = f.read()
        dtypes = ['int8', 'int16', 'int32',
                  'uint8', 'uint16', 'uint32',
                  'float32', 'float64'
                ]
        for dtype in dtypes:
            out = code.format(T = dtype)
            #print(out)
            outname = './src/pycimg_{}.pyx'.format(dtype)
            with open(outname, 'w') as fout:
                fout.write(out)       

