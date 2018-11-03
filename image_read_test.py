#encoding char codes :'iso2022_jp'
 
import struct
from PIL import Image
 
filename = 'data/ETL9B/ETL9B_1'
skip = 1
record_size = 576
with open(filename, 'rb') as f:
    f.seek(skip * record_size)
    s = f.read(record_size)
    r = struct.unpack('>2H4s504s64x', s)
    print(r[0:3], hex(r[1]))
    i1 = Image.frombytes('1', (64, 63), r[3], 'raw')
    fn = 'ETL9B_{xx}_{yy}.png'.format(xx = (r[0]-1)%20+1,yy = hex(r[1])[-4:])
    i1.save(fn, 'PNG')