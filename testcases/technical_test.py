# PyAlgoTrade
# 
# Copyright 2011 Gabriel Martin Becedillas Ruiz
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""

import unittest
from pyalgotrade import technical
from pyalgotrade import dataseries

class CacheTest(unittest.TestCase):
	def testCacheSize1(self):
		cache = technical.Cache(1)

		self.assertTrue(not cache.isCached(0))
		self.assertTrue(cache.getValue(0) == None)

		cache.putValue(0, 10)
		self.assertTrue(cache.getValue(0) == 10)

		cache.putValue(1, 20)
		self.assertTrue(cache.getValue(1) == 20)

		# Check that the value was replaced
		self.assertTrue(not cache.isCached(0))
		self.assertTrue(cache.getValue(0) == None)

	def testCacheSize2(self):
		cache = technical.Cache(2)
		cache.putValue(0, 0)
		cache.putValue(1, 1)
		cache.putValue(2, 2)

		self.assertTrue(cache.getValue(1) == 1)
		self.assertTrue(cache.getValue(2) == 2)

		# Check that the value was replaced
		self.assertTrue(cache.getValue(0) == None)

class DataSeriesFilterTest(unittest.TestCase):
	class TestFilter(technical.DataSeriesFilter):
		def __init__(self, dataSeries):
			technical.DataSeriesFilter.__init__(self, dataSeries, 1)

		def calculateValue(self, firstPos, lastPos):
			return self.getDataSeries().getValueAbsolute(lastPos)

	def testInvalidPosNotCached(self):
		values = []
		ds = dataseries.SequenceDataSeries(values)
		for i in range(10):
			values.append(i)
			values.append(None) # Interleave Nones.

		testFilter = DataSeriesFilterTest.TestFilter(ds)
		self.assertTrue(testFilter.getValue() == None)
		self.assertTrue(testFilter.getValue(1) == 9)
		self.assertTrue(testFilter.getValue(3) == 8) # We go 3 instead of 2 because we need to skip the interleaved None values.

		self.assertTrue(testFilter.getValueAbsolute(18) == 9)
		self.assertTrue(testFilter.getValueAbsolute(19) == None)
		# Absolut pos 20 should have the next value once we insert it, but right now it should be None
		self.assertTrue(testFilter.getValueAbsolute(20) == None)
		values.append(10)
		self.assertTrue(testFilter.getValueAbsolute(20) == 10)

def getTestCases():
	ret = []
	ret.append(CacheTest("testCacheSize1"))
	ret.append(CacheTest("testCacheSize2"))
	ret.append(DataSeriesFilterTest("testInvalidPosNotCached"))
	return ret


