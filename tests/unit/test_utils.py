""" This module contains unit tests for utils-module. """
import numpy as np
import numpy.ma as ma
from numpy.testing import assert_array_almost_equal
import pytest
from cloudnetpy import utils


@pytest.mark.parametrize("input, output", [
    ([1, 2, 3], [0.5, 1.5, 2.5, 3.5]),
    ([0.1, 0.3, 0.5], [0.0, 0.2, 0.4, 0.6]),
    ([0.02, 0.04, 0.06], [0.01, 0.03, 0.05, 0.07]),
])
def test_binvec(input, output):
    assert_array_almost_equal(utils.binvec(input), output)


@pytest.mark.parametrize("number, nth_bit, result", [
    (0, 0, False),
    (1, 0, True),
    (2, 0, False),
    (2, 1, True),
    (3, 0, True),
])
def test_isbit(number, nth_bit, result):
    assert utils.isbit(number, nth_bit) is result


@pytest.mark.parametrize("n, k, res", [
    (0, 0, 1),
    (3, 0, 3),
    (4, 0, 5),
    (4, 1, 6),
])
def test_setbit(n, k, res):
    assert utils.setbit(n, k) == res


@pytest.mark.parametrize("input, output", [
    ([24*60*60], 24),
    ([12*60*60], 12),
])
def test_seconds2hours(input, output):
    assert utils.seconds2hours(input) == output


@pytest.mark.parametrize("input, output", [
    (np.array([1, 2, 3]), 1),
    (ma.array([1, 2, 3, 4, 5, 6], mask=[0, 1, 0, 1, 0, 0]), 1),
    (np.array([1, 2, 10, 11, 12, 13, 14, 16]), 1)
])
def test_mdiff(input, output):
    assert utils.mdiff(input) == output


@pytest.mark.parametrize("a, b, result", [
    (np.array([2, 3]), np.array([3, 4]), np.sqrt([13, 25])),
    (np.array([2, 3]), ma.array([3, 4], mask=True), [2, 3]),
    (np.array([2, 3]), ma.array([3, 4], mask=[0, 1]), [np.sqrt(13), 3]),
])
def test_l2_norm(a, b, result):
    assert_array_almost_equal(utils.l2norm(a, b), result)


class TestRebin2D:
    x = np.array([1, 2, 2.99, 4, 4.99, 6, 7])
    xnew = np.array([2, 4, 6])
    data = np.array([range(1, 8), range(1, 8)]).T

    def test_rebin_2d(self):
        data_i = utils.rebin_2d(self.x, self.data, self.xnew)
        result = np.array([[2, 4.5, 6.5], [2, 4.5, 6.5]]).T
        assert_array_almost_equal(data_i, result)

    def test_rebin_2d_std(self):
        data_i = utils.rebin_2d(self.x, self.data, self.xnew, 'std')
        result = np.array([np.std([1, 2, 3]), np.std([4, 5]), np.std([6, 7])])
        result = np.array([result, result]).T
        assert_array_almost_equal(data_i, result)


def test_filter_isolated_pixels():
    x = np.array([[0, 0, 1, 1, 1],
                  [0, 0, 0, 0, 0],
                  [1, 0, 1, 0, 0],
                  [0, 0, 0, 0, 1]])
    x2 = np.array([[0, 0, 1, 1, 1],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0]])
    assert_array_almost_equal(utils.filter_isolated_pixels(x), x2)


@pytest.mark.parametrize("input, result", [
    ([[0, 1, 1, 1, 1],
      [0, 0, 0, 1, 0],
      [1, 1, 1, 0, 0],
      [0, 1, 0, 1, 1]],
     [[0, 0, 0, 1, 0],
      [0, 0, 0, 1, 0],
      [0, 1, 0, 0, 0],
      [0, 1, 0, 0, 0]]),
])
def test_filter_x_pixels(input, result):
    assert_array_almost_equal(utils.filter_x_pixels(input), result)


@pytest.mark.parametrize("input, result", [
    (np.array([0, 5, 0, 0, 2, 0]),
     np.array([0, 5, 5, 5, 2, 2])),
    (np.array([[1, 0, 2, 0],
               [0, 5, 0, 0]]),
     np.array([[1, 1, 2, 2],
               [0, 5, 5, 5]])),
])
def test_ffill(input, result):
    assert_array_almost_equal(utils.ffill(input), result)


def test_ffill_2():
    x = np.array([[5, 1, 1, 6],
                  [3, 0, 1, 0]])
    result = np.array([[5, 5, 5, 6],
                       [3, 0, 0, 0]])
    assert_array_almost_equal(utils.ffill(x, value=1), result)


def test_cumsumr_1():
    x = np.array([0, 1, 2, 0, 1, 1])
    res = np.array([0, 1, 3, 0, 1, 2])
    assert_array_almost_equal(utils.cumsumr(x), res)


def test_cumsumr_2():
    x = np.array([[0, 1, 1, 0],
                  [0, 5, 0, 0]])
    res = np.array([[0, 1, 2, 0],
                    [0, 5, 0, 0]])
    assert_array_almost_equal(utils.cumsumr(x, axis=1), res)


def test_cumsumr_3():
    x = np.array([[0, 1, 1, 0],
                  [0, 5, 0, 0]])
    res = np.array([[0, 1, 1, 0],
                    [0, 6, 0, 0]])
    assert_array_almost_equal(utils.cumsumr(x, axis=0), res)


def test_cumsumr_4():
    x = np.array([[0, 1, 1, 0],
                  [0, 5, 0, 0]])
    res = np.array([[0, 1, 1, 0],
                    [0, 6, 0, 0]])
    assert_array_almost_equal(utils.cumsumr(x), res)


@pytest.mark.parametrize("input, output", [
    (np.array([1, 2, 3]), False),
    (ma.array([1, 2, 3]), False),
    (2, True),
    ((2.5,), True),
    ((2.5, 3.5), False),
    ([3], True),
    ([3, 4], False),
    (np.array(5), True),
    (ma.array(5.2), True),
    (ma.array([1, 2, 3], mask=True), False),
    (ma.array([1, 2, 3], mask=False), False),
    ([], False),
])
def test_isscalar(input, output):
    assert output == utils.isscalar(input)


@pytest.mark.parametrize("x, a, result", [
    (np.arange(1, 10), 5, 5),
    (np.arange(1, 10), 5.4, 5),
    (np.arange(1, 10), 5.5, 6),
    (np.arange(1, 10), 5, 5),
    (np.linspace(0, 10, 21), 3.5, 7),
])
def test_n_elements(x, a, result):
    assert utils.n_elements(x, a) == result


@pytest.mark.parametrize("x, a, result", [
    (np.linspace(0, 1, 61), 30, 30),
    (np.linspace(0, 6, (6*60+1)*2), 10, 20),
])
def test_n_elements_2(x, a, result):
    assert utils.n_elements(x, a, 'time') == result


def test_l2_norm_weighted():
    x = (2, 3)
    weights = (1, 2)
    scale = 10
    assert_array_almost_equal(utils.l2norm_weighted(x, scale, weights), 10*np.sqrt([40]))


@pytest.mark.parametrize("x_new, y_new, result", [
    (np.array([1, 2]),
     np.array([5, 5]),
     np.array([[1, 1], [1, 1]])),
    (np.array([1, 2]),
     np.array([5, 10]),
     np.array([[1, 2], [1, 2]])),
    (np.array([1.5, 2.5]),
     np.array([5, 10]),
     np.array([[1, 2], [1, 2]])),
    (np.array([1, 2]),
     np.array([7.5, 12.5]),
     np.array([[1.5, 2.5], [1.5, 2.5]])),
])
def test_interp_2d(x_new, y_new, result):
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([5, 10, 15])
    z = np.array([5*[1], 5*[2], 5*[3]]).T
    assert_array_almost_equal(utils.interpolate_2d(x, y, z, x_new, y_new),
                              result)
