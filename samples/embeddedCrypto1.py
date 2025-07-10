from sympy.ntheory import factorint
from sympy.ntheory.modular import crt
from random import *

from pyasn1.type import univ, namedtype
from pyasn1.codec.der.decoder import decode

class Group(object):
	def __init__(self, l, e, N, p):
		self.l = l
		self.e = e
		self.N = N
		self.p = p
		if self.checkParameters() != True:
			raise Exception("Problem with parameters")
	
	def checkParameters(self):
		if self.l == "":
			raise Exception("l is unknown")
		if (self.l == "ZpAdditive" and self.e == 0) or (self.l == "ZpMultiplicative" and self.e == 1):
			return True
		else:
			return False
			
	def law(self, g1, g2):
		if self.l == "ZpAdditive":
			return (g1 + g2) % self.p
		if self.l == "ZpMultiplicative":
			return (g1 * g2) % self.p
			
	def exp(self, g, k) :
		if k == 0:
			return self.e
		elif k == -1:
			return self.exp(g, self.N - 1)
		else:
			h0 = self.e
			h1 = g
			t = k.bit_length() - 1
			for i in range(t, -1, -1):
				if ((k >> i) & 1) == 0:
					h1 = self.law(h0, h1)
					h0 = self.law(h0, h0)
				else:
					h0 = self.law(h0, h1)
					h1 = self.law(h1, h1)
			return h0

class SubGroup(Group):
	def __init__(self, l, e, N, p, g):
		Group.__init__(self, l, e, N, p)
		self.g = g			

	def ComputeDL(self, h, tau = 1000):
		if (self.N <= tau):
			for i in range(self.N):
				if self.DLbyTrialMultiplication(self.g, i) == h:
					return i
		else:
			return self.DLbyBabyStepGiantStep(self.g, h)
	
	def DLbyTrialMultiplication(self, g, k):
		h = self.e
		t = k.bit_length()
		for i in range(t, -1, -1):
			h = self.law(h, h)
			if ((k >> i) & 1) == 1:
				h = self.law(h, g)
			else:
				x = self.law(h, g)
		return h
			
	def DLbyBabyStepGiantStep(self, g, h):
		w = int(pow(self.N, 1 / 2))
		if pow(self.N, 1 / 2) % 2 > 0:
			w += 1
		T = [self.exp(g, i * w) for i in range(w + 1)]
		for j in range (w + 1):
			x = self.law(h, self.exp(g, self.N - j))
			for i in range(len(T)):
				if x == T[i]:
					return (w * i + j) % self.N
					
	def DLinPrimePowerOrderGroup(self, h, pk, ek):
		y = self.exp(self.g, int(pow(pk, ek - 1)))
		i = 0
		subgroup = SubGroup(self.l, self.e, pk, self.p, y)
		for j in range(ek):
			gih = self.law(self.exp(self.g, self.N - i), h)
			power = int(pow(self.p, ek - j - 1))
			H = self.exp(gih, power)
			t = subgroup.ComputeDL(H)
			i = i + t * int(pow(pk, j)) % int(pow(pk, ek))
		return i % int(pow(pk, ek))
		
	def DLbyPohligHellman(self, h):
		I = []
		M = []
		for k in factorint(self.N):
			pk, ek = k, factorint(self.N)[k]
			M += [int(pow(pk, ek))]
			gk = self.exp(self.g, int(self.N / pow(pk, ek)))
			hk = self.exp(h, int(self.N / pow(pk, ek)))
			for ik in range(int(pow(pk, ek))):
				if (self.exp(gk, ik) == hk):
					I += [ik]
					break
		i = crt(M, I)[0]
		return i
		
	def testDiffieHellman(self):
		a = int((random() * 1000) % (self.N + 1))
		b = int((random() * 1000) % (self.N + 1))
		A = self.exp(self.g, a)
		B = self.exp(self.g, b)
		if (self.exp(A, b) == self.exp(B, a)):
			return True
		else:
			return False
	    		
	def DiffieHellman(self, a, b, A, B, K):
		if (A == self.exp(self.g, a) and B == self.exp(self.g, b) and K == self.exp(A, b) and K == self.exp(B, a)):
			return True
		else:
			return False

class DHParameter(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('prime', univ.Integer()),                # p
        namedtype.NamedType('base', univ.Integer()),                 # g
        namedtype.OptionalNamedType('privateValueLength', univ.Integer())  # optional N
    )

def retrieve():
    with open("dhParam.der", 'rb') as f:
        der_data = f.read()

    dh_param, _ = decode(der_data, asn1Spec=DHParameter())

    p = int(dh_param.getComponentByName('prime'))
    g = int(dh_param.getComponentByName('base'))

    try:
        N = int(dh_param.getComponentByName('privateValueLength'))
    except Exception:
        N = p - 1

    return (p, g, N)
