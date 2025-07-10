import unittest
from samples.embeddedCrypto1 import *
from hamcrest import *
from random import *

class test1(unittest.TestCase):

	def __assert_constructor(self, l, e):
		any_N=-1
		any_p=-1
		return Group(l, e, any_N, any_p)

	def __assert_unsuccessful_constructor(self, l, e):
		try:
			self.__assert_constructor(l, e)
		except:
			return True
		
		assert_that(f"Constructor did not fail with l={l}, e={e}", equal_to("Constructor failing"))
		
	def __assert_successful_constructor(self, l, e):
		try:
			self.__assert_constructor(l, e)
		except:
			assert_that(f"Constructor failed with l={l}, e={e}", equal_to("Constructor did not fail"))

	def test_zp_additive_group_is_abelian(self):
		z11 = Group("ZpAdditive", 0, 11, 11)
		assert_that(z11.law(7, 5), equal_to(z11.law(5, 7)))
		assert_that(z11.law(7, z11.law(3, 5)), equal_to(z11.law(z11.law(7, 3), 5)))
		assert_that(z11.law(7, z11.e), equal_to(7))
		
	def test_zp_multiplictive_group_is_abelian(self):
		z11 = Group("ZpMultiplicative", 1, 10, 11)
		assert_that(z11.law(7, 5), equal_to(z11.law(5, 7)))
		assert_that(z11.law(7, z11.law(3, 5)), equal_to(z11.law(z11.law(7, 3), 5)))
		assert_that(z11.law(7, z11.e), equal_to(7))

	def test_exception_unknown(self):
		with self.assertRaises(Exception) as e:
			Group("", 0, 0, 0).checkParameters()
		self.assertEqual(str(e.exception), "l is unknown")

	def test_exception_additive(self):
		with self.assertRaises(Exception) as e:
			Group("ZpAdditive", 3, 3, 3).checkParameters()
		self.assertEqual(str(e.exception), "Problem with parameters")

	def test_exception_multiplicative(self):
		with self.assertRaises(Exception) as e:
			Group("ZpMultiplicative", 3, 2, 3).checkParameters()
		self.assertEqual(str(e.exception), "Problem with parameters")

	def testLab1_part1(self):
		monGroupe = Group("ZpAdditive", 0, 23, 23)
		assert_that(monGroupe.exp(5, 7), equal_to(12))
		assert_that(monGroupe.exp(5, -1), equal_to(18))
		monGroupe = Group("ZpMultiplicative", 1, 22, 23)
		assert_that(monGroupe.exp(5, 7), equal_to(17))
		assert_that(monGroupe.exp(5, -1), equal_to(14))
		subZ809 = SubGroup("ZpAdditive", 0, 809, 809, 3)
		i = int((random() * 10000) % 809)
		assert_that(subZ809.DLbyTrialMultiplication(3, 4), equal_to(12))
		assert_that(subZ809.DLbyTrialMultiplication(300, 400), equal_to(120000 % 809))
		assert_that(subZ809.DLbyBabyStepGiantStep(3, 12), equal_to(4))
		assert_that(subZ809.DLbyBabyStepGiantStep(300, 120000 % 809), equal_to(400))
		assert_that(subZ809.ComputeDL(subZ809.exp(subZ809.g, i), 800), equal_to(i))
		assert_that(subZ809.ComputeDL(subZ809.exp(subZ809.g, i), 1000), equal_to(i))
		assert_that(subZ809.DLinPrimePowerOrderGroup(subZ809.exp(subZ809.g, i), 809, 1), equal_to(i))
		subZ809 = SubGroup("ZpMultiplicative", 1, 808, 809, 3)
		i = int((random() * 1000) % 809)
		assert_that(subZ809.DLbyTrialMultiplication(3, 4), equal_to(81))
		assert_that(subZ809.DLbyTrialMultiplication(300, 4), equal_to(8100000000 % 809))
		assert_that(subZ809.DLbyBabyStepGiantStep(3, 81), equal_to(4))
		assert_that(subZ809.DLbyBabyStepGiantStep(300, 8100000000 % 809), equal_to(4))
		assert_that(subZ809.ComputeDL(subZ809.exp(subZ809.g, i), 800), equal_to(i))
		assert_that(subZ809.ComputeDL(subZ809.exp(subZ809.g, i), 1000), equal_to(i))
		assert_that(subZ809.DLinPrimePowerOrderGroup(subZ809.exp(subZ809.g, i), 809, 1), equal_to(i))
		subZ64 = SubGroup("ZpAdditive", 0, 64, 64, 3)
		i = int((random() * 1000) % 64)
		#assert_that(subZ64.DLinPrimePowerOrderGroup(subZ64.exp(subZ64.g, i), 2, 6), equal_to(i))
		subZ64 = SubGroup("ZpMultiplicative", 1, 63, 64, 3)
		i = int((random() * 1000) % 64)
		#assert_that(subZ64.DLinPrimePowerOrderGroup(subZ64.exp(subZ64.g, i), 2, 4), equal_to(i))
		subZ251 = SubGroup("ZpMultiplicative", 1, 250, 251, 71)
		assert_that(subZ251.DLbyPohligHellman(210), equal_to(197))
		subZ179424673 = SubGroup("ZpMultiplicative", 1, 179424672, 179424673, 15)
		assert_that(subZ179424673.DLbyPohligHellman(153967177), equal_to(123456))

	def testLab1_part2(self):
		subZ23 = SubGroup("ZpAdditive", 0, 23, 23, 5)
		assert(subZ23.testDiffieHellman())
		assert(subZ23.DiffieHellman(5, 6, 2, 7, 12))
		subZ257 = SubGroup("ZpAdditive", 0, 33, 257, 256)
		assert(subZ257.testDiffieHellman())
		(p, g, N) = retrieve()
		subZp = SubGroup("ZpAdditive", 0, N, p, g)
		assert(subZp.testDiffieHellman())
