from PIL import Image


def str2bin(text):
	tBin = ""
	for i in text:
		bn = bin(ord(i))[2:]
		bn = '0' * (8 - len(bn)) + bn
		#print(bn)
		tBin += bn 
	return tBin

def bin2str(bn):
	str = chr(bin2dec(bn))
	return str

def bin2dec(bn):
	p = len(bn)-1
	sum = 0
	for i in bn:
		sum += int(i)*(2**p)
		p -= 1
	return sum

def dec2bin(n):
	bn = ""
	while(n >= 1):
		bn = str(n%2) + bn
		n = n//2
	#return bn
	return '0' * (8 - len(bn)) + bn


def editPix(pix, bits):
	#print(pix, bits, end=' ')
	if(len(bits) == 6):
		pix = (bin2dec(dec2bin(pix[0])[:6] + bits[:2]), bin2dec(dec2bin(pix[1])[:6] + bits[2:4]), bin2dec(dec2bin(pix[2])[:6] + bits[4:]), 255)
	if(len(bits) == 4):
		pix = (bin2dec(dec2bin(pix[0])[:6] + bits[:2]), bin2dec(dec2bin(pix[1])[:6] + bits[2:4]), pix[2], 253)
	if(len(bits) == 2):
		pix = (bin2dec(dec2bin(pix[0])[:6] + bits[:2]), pix[1], pix[2], 252)
	if(len(bits) == 0):
		pix = (pix[0], pix[1], pix[2], 254)
	#print(pix)
	return pix
			

def encrypt(image, text):
	#text = "test12345"
	bn = str2bin(text)
	
	if image.mode == "RGB":
	    a_channel = Image.new('L', image.size, 255)
	    image.putalpha(a_channel)
	   
	pix = image.load()

	fits = False
	x, y = image.size
	end = False
	n = 0
	for j in range(y):
		for i in range(x):
			pix[i, j] = editPix(pix[i, j], bn[n:n+6])

			if(pix[i, j][3] != 255):
				fits = True

			n += 6
			if(n > len(bn)):
				end = True
				break
		if(end):
			break

	if(fits == False):
		print("text cant fit in image!")
	else:
		image.save("out.png")


def extractBin(clr):
	alpha = clr[3];

	bn = ''
	if(alpha == 255):
		for i in range(3):
			bn += dec2bin(clr[i])[6:]
		#print(bn, alpha)
		return bn

	if(alpha == 254):
		return bn

	if(alpha == 253):
		for i in range(3):
			bn += dec2bin(clr[i])[6:]
		#print(bn, alpha)
		return bn[:4]

	if(alpha == 252):
		for i in range(3):
			bn += dec2bin(clr[i])[6:]
		#print(bn, alpha)
		return bn[:2]


def decrypt(image):
	pix = image.load()
	x, y = image.size

	end = False
	bn = ""
	for j in range(y):
		for i in range(x):
			bn += extractBin(pix[i, j])

			if(pix[i, j][3] != 255):
				end = True
				break
			
		if(end):
			break
	#print(bn, len(bn))

	text = ""
	for i in range(len(bn)//8):
		text += bin2str(bn[8*i:8*i + 8])

	#print(text)
	return text



#image = Image.open('smol.png')
#text = "yeah two"

img = input("Enter image name: ")
image = Image.open(img)

n = int(input("(1) for encrypt, (2) for decrypt: "))
if n == 1:
	text = input("Enter text: ")
	encrypt(image, text)
elif n == 2:
	text = decrypt(image)
	print(text)

'''
data = "hi"
image = Image.open('tbt.png')

x, y = 0, 0

im = image.load()
im[x, y] = (255, 0, 0, 255)

image.save("test.png")
'''