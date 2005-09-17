import autopath


class TestW_SliceObject:

    def test_indices(self):
        from pypy.objspace.std import slicetype
        space = self.space
        w = space.wrap
        w_None = space.w_None
        w_slice = space.newslice(w_None, w_None, w_None)
        assert slicetype.indices3(space, w_slice, 6) == (0, 6, 1)
        w_slice = space.newslice(w(0), w(6), w(1))
        assert slicetype.indices3(space, w_slice, 6) == (0, 6, 1)
        w_slice = space.newslice(w_None, w_None, w(-1))
        assert slicetype.indices3(space, w_slice, 6) == (5, -1, -1)

    def test_indices_fail(self):
        from pypy.objspace.std import slicetype
        space = self.space
        w = space.wrap
        w_None = space.w_None
        w_slice = space.newslice(w_None, w_None, w(0))
        self.space.raises_w(space.w_ValueError,
                            slicetype.indices3, space, w_slice, 10)


class AppTest_SliceObject:
    def test_new(self):
        def cmp_slice(sl1, sl2):
            for attr in "start", "stop", "step":
                if getattr(sl1, attr) != getattr(sl2, attr):
                    return False
            return True
        raises(TypeError, slice)
        raises(TypeError, slice, 1, 2, 3, 4)
        assert cmp_slice(slice(23), slice(None, 23, None))
        assert cmp_slice(slice(23, 45), slice(23, 45, None))

    def test_indices(self):
        assert slice(4,11,2).indices(28) == (4, 11, 2)
        assert slice(4,11,2).indices(8) == (4, 8, 2)
        assert slice(4,11,2).indices(2) == (2, 2, 2)
        assert slice(11,4,-2).indices(28) == (11, 4, -2)
        assert slice(11,4,-2).indices(8) == (7, 4, -2)
        assert slice(11,4,-2).indices(2) == (1, 2, -2)

    def test_repr(self):
        assert repr(slice(1, 2, 3)) == 'slice(1, 2, 3)'
        assert repr(slice(1, 2)) == 'slice(1, 2, None)'
        assert repr(slice('a', 'b')) == "slice('a', 'b', None)"
        
    def test_eq(self):
        slice1 = slice(1, 2, 3)
        slice2 = slice(1, 2, 3)
        assert slice1 == slice2
        slice2 = slice(1, 2)
        assert slice1 != slice2

    def test_lt(self):
        assert slice(0, 2, 3) < slice(1, 0, 0)
        assert slice(0, 1, 3) < slice(0, 2, 0)
        assert slice(0, 1, 2) < slice(0, 1, 3)
        assert not (slice(1, 2, 3) < slice(0, 0, 0))
        assert not (slice(1, 2, 3) < slice(1, 0, 0))
        assert not (slice(1, 2, 3) < slice(1, 2, 0))
        assert not (slice(1, 2, 3) < slice(1, 2, 3))

    def test_long_indices(self):
        assert slice(-2 ** 100, 10, 1).indices(1000) == (0, 10, 1)
        assert slice(-2 ** 200, -2 ** 100, 1).indices(1000) == (0, -1, 1)
        assert slice(2 ** 100, 0, -1).indices(1000) == (999, 0, -1)
        assert slice(2 ** 100, -2 ** 100, -1).indices(1000) == (999, -1, -1)
        start, stop, step = slice(0, 1000, 2 ** 200).indices(1000)
        assert start == 0
        assert stop == 1000
        assert step >= 1000
        raises(OverflowError, "slice(0, 1000, 1).indices(2 ** 100)")
