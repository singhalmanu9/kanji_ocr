#encoding char codes :'iso2022_jp'
from collections import Counter
import struct
from PIL import Image, ImageEnhance
 
filename = 'data/ETL1/ETL1C_01'

def make_images_9(filename):
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

def make_images_1(filename):
	record_size = 2052;
	c = Counter();
	with open(filename, 'rb') as f:
		for skip in range(0, 11288):
		    f.seek(skip * record_size)
		    s = f.read(record_size)
		    print(skip)
		    r = struct.unpack('>H2sH6BI4H4B4x2016s4x', s)
		    iF = Image.frombytes('F', (64, 63), r[18], 'bit', 4)
		    iP = iF.convert('L')
		    fn = 'img/ETL1_{xx}_{yy}_{zz}.png'.format(xx = (r[2]-1)%20+1,yy = hex(r[3])[-4:], zz = c[hex(r[3])]);
	    # iP.save(fn, 'PNG', bits=4)
		    enhancer = ImageEnhance.Brightness(iP)
		    iE = enhancer.enhance(16)
		    iE.save(fn, 'PNG')

def make_images_8(filename):
	with open(filename, 'rb') as f:
		for skip in range(0, 51201):
			f.seek((skip) * 512)
			print(skip)
			s = f.read(512)
			r = struct.unpack('>2H4s504s',s)
			i1 = Image.frombytes('1', (64, 63), r[3], 'raw')
			fn = 'ETL8B2_{:d}_{:s}.png'.format((r[0]-1)%20+1, hex(r[1])[-4:])
			i1.save("img/" + fn, 'PNG')

files = ['data/ETL8B/ETL8B2C' + str(i) for i in range(1,4)]
for file in files:
	make_images_8(file)
