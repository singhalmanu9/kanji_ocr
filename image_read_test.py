#encoding char codes :'iso2022_jp'
from collections import Counter
import struct
from PIL import Image, ImageEnhance
import bitstring
import codecs
filename = 'data/ETL1/ETL1C_01'

def make_images_9(filename):
	record_size = 576
	c = Counter()
	with open(filename, 'rb') as f:
		for skip in range(0, 121440):
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
	record_size = 2052
	c = Counter();
	with open(filename, 'rb') as f:
		for skip in range(0, 11560):
		    f.seek(skip * record_size)
		    s = f.read(record_size)
		    print(skip)
		    r = struct.unpack('>H2sH6BI4H4B4x2016s4x', s)
		    c[hex(r[3])] += 1
		    iF = Image.frombytes('F', (64, 63), r[18], 'bit', 4)
		    iP = iF.convert('L')
		    fn = 'img/ETL1_{xx}_{yy}_{zz}.png'.format(xx = (r[2]-1)%20+1,yy = hex(r[3])[-4:], zz = c[hex(r[3])]);
	    # iP.save(fn, 'PNG', bits=4)
		    enhancer = ImageEnhance.Brightness(iP)
		    iE = enhancer.enhance(16)
		    iE.save(fn, 'PNG')

def make_images_8(filename):
	c = Counter();
	with open(filename, 'rb') as f:
		for skip in range(0, 51201):
			f.seek((skip) * 512)
			print(skip)
			s = f.read(512)
			r = struct.unpack('>2H4s504s',s)
			c[hex(r[1])] += 1
			i1 = Image.frombytes('1', (64, 63), r[3], 'raw')
			fn = 'ETL8B2_{:d}_{:s}_{zz}.png'.format((r[0]-1)%20+1, hex(r[1])[-4:], zz = c[hex(r[1])])
			i1.save("img/" + fn, 'PNG')

# def make_images_2(filename, skipsize):
# 	record_size = 2745
# 	t56s = '0123456789[#@:>? ABCDEFGHI&.](<  JKLMNOPQR-$*);\'|/STUVWXYZ ,%="!'
# 	def T56(c):
# 	    return t56s[c]
	 
# 	with codecs.open('co59-utf8.txt', 'r', 'utf-8') as co59f:
# 	    co59t = co59f.read()
# 	co59l = co59t.split()
# 	CO59 = {}
# 	for c in co59l:
# 	    ch = c.split(':')
# 	    co = ch[1].split(',')
# 	    CO59[(int(co[0]),int(co[1]))] = ch[0]
	 
# 	for skip in range(skipsize):
# 		f = bitstring.ConstBitStream(filename=filename)
# 		f.pos = skip * 6 * 3660
# 		r = f.readlist('int:36,uint:6,pad:30,6*uint:6,6*uint:6,pad:24,2*uint:6,pad:180,bytes:2700') 
# 		print (r[0], T56(r[1]), "".join(map(T56, r[2:8])), "".join(map(T56, r[8:14])), CO59[tuple(r[14:16])],bytes(CO59[tuple(r[14:16])],'iso2022_jp').decode("iso"))
# 		iF = Image.frombytes('F', (60,60), r[16], 'bit', 6)
# 		iP = iF.convert('L')
# 		fn = '{:s}.png'.format(CO59[tuple(r[14:16])])
# 		#iP.save(fn, 'PNG', bits=6)
# 		enhancer = ImageEnhance.Brightness(iP)
# 		iE = enhancer.enhance(4)
# 		iE.save("img/" + fn, 'PNG')

#files = ['data/ETL2/ETL2_' + str(i) for i in range(1,6)]
# i = 0
# skipsize = [9056,10480,11360,10480,11420]
files = ['data/ETL9B/ETL9B_' + str(i) for i in range(1,6)]

for file in files:
	make_images_9(file)