
""" test proxy internals like code, traceback, frame
"""
from pypy.conftest import gettestobjspace

class AppProxy(object):
    def setup_class(cls):
        cls.space = gettestobjspace(**{"objspace.std.withtproxy": True})

    def setup_method(self, meth):
        self.w_get_proxy = self.space.appexec([], """():
        class Controller(object):
            def __init__(self, obj):
                self.obj = obj
    
            def perform(self, name, *args, **kwargs):
                return getattr(self.obj, name)(*args, **kwargs)
        def get_proxy(f):
            from pypymagic import transparent_proxy as proxy
            return proxy(type(f), Controller(f).perform)
        return get_proxy
        """)

class AppTestProxyInternals(AppProxy):
    def test_traceback_basic(self):
        try:
            1/0
        except:
            import sys
            e = sys.exc_info()
        
        tb = self.get_proxy(e[2])
        assert tb.tb_frame is e[2].tb_frame
    
    def test_traceback_catch(self):
        try:
            try:
                1/0
            except ZeroDivisionError, e:
                ex = self.get_proxy(e)
                raise ex
        except ZeroDivisionError:
            pass
        else:
            raise AssertionError("Did not raise")

    def test_traceback_reraise(self):
        #skip("Not implemented yet")
        try:
            1/0
        except:
            import sys
            e = sys.exc_info()
        
        tb = self.get_proxy(e[2])
        raises(ZeroDivisionError, "raise e[0], e[1], tb")
        raises(ZeroDivisionError, "raise e[0], self.get_proxy(e[1]), tb")
        import traceback
        assert len(traceback.format_tb(tb)) == 1

    def test_simple_frame(self):
        import sys
        frame = sys._getframe(0)
        fp = self.get_proxy(frame)
        assert fp.f_locals == frame.f_locals

class AppTestProxyTracebackController(AppProxy):
    def test_controller(self):
        import types
        import sys
        import traceback
        
        def get_proxy(f):
            from pypymagic import transparent_proxy as proxy
            return proxy(type(f), Controller(f).perform)
        
        class FakeTb(object):
            def __init__(self, tb):
                self.tb_lasti = tb.tb_lasti
                self.tb_lineno = tb.tb_lineno
                if tb.tb_next:
                    self.tb_next = FakeTb(tb.tb_next)
                else:
                    self.tb_next = None
                self.tb_frame = get_proxy(tb.tb_frame)
        
        class Controller(object):
            def __init__(self, tb):
                if isinstance(tb, types.TracebackType):
                    self.obj = FakeTb(tb)
                else:
                    self.obj = tb
            
            def perform(self, name, *args, **kwargs):
                return getattr(self.obj, name)(*args, **kwargs)
        
        def f():
            1/0
        
        def g():
            f()
        
        try:
            g()
        except:
            e = sys.exc_info()
        
        last_tb = e[2]
        tb = get_proxy(e[2])
        try:
            raise e[0], e[1], tb
        except:
            e = sys.exc_info()
        
        assert traceback.format_tb(last_tb) == traceback.format_tb(e[2])
    
    def test_proxy_get(self):
        from pypymagic import transparent_proxy, get_transparent_controller
        l = [1,2,3]
        def f(name, *args, **kwargs):
            return getattr(l, name)(*args, **kwargs)
        lst = transparent_proxy(list, f)
        assert get_transparent_controller(lst) is f

class DONTAppTestProxyType(AppProxy):
    def test_filetype(self):
        f = self.get_proxy(file)
        f("/tmp/sth", "w").write("aaa")
        assert open("/tmp/sth").read() == "aaa"

    def test_fileobject(self):
        f = open("/tmp/sth", "w")
        fp = self.get_proxy(f)
        fp.write("aaa")
        fp.close()
        assert open("/tmp/sth").read() == "aaa"

    def test_isinstance(self):
        class A:
            pass

        a = A()
        Ap = self.get_proxy(A)
        ap = self.get_proxy(a)
        assert isinstance(a, A)
        assert isinstance(a, Ap)
        assert isinstance(ap, A)
        assert isinstance(ap, Ap)
        assert type(a) is type(ap)
