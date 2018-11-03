#encoding char codes :'iso2022_jp'
from collections import Counter
import struct
from PIL import Image
 
filename = 'data/ETL9B/ETL9B_1'

def make_images(filename):
	record_size = 576
	c = Counter()
	with open(filename, 'rb') as f:
		for skip in range(0, 121441):
		    f.seek(skip * record_size)
		    s = f.read(record_size)
		    r = struct.unpack('>2H4s504s64x', s)
		    c[hex(r[1])] += 1
		    if hex(r[1]) == "0x2422":
		    	print(c[hex(r[1])])
		    i1 = Image.frombytes('1', (64, 63), r[3], 'raw')
		    fn = 'img/ETL9B_{xx}_{yy}_{zz}.png'.format(xx = (r[0]-1)%20+1,yy = hex(r[1])[-4:], zz = c[hex(r[1])])
		    i1.save(fn, 'PNG')
files = [ 'data/ETL9B/ETL9B_1', 'data/ETL9B/ETL9B_2', 'data/ETL9B/ETL9B_3', 'data/ETL9B/ETL9B_4', 'data/ETL9B/ETL9B_5']

for file in files:
	make_images(file)
