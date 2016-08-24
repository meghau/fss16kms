import utest, math

@utest.ok
def test_pi():
	""" Function to check the value of pi"""
	assert math.pi == 3.14, "pi goes to infinity and beyond"
