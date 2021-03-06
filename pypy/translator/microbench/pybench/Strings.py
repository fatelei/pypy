# -*- coding: utf-8 -*-
from pybench import Test
from string import join

class ConcatStrings(Test):

    version = 0.1
    operations = 10 * 5
    rounds = 60000

    def test(self):

        # Make sure the strings are *not* interned
        s = join(map(str,range(100)))
        t = join(map(str,range(1,101)))

        for i in xrange(self.rounds):
            t + s
            t + s
            t + s
            t + s
            t + s

            t + s
            t + s
            t + s
            t + s
            t + s

            t + s
            t + s
            t + s
            t + s
            t + s

            t + s
            t + s
            t + s
            t + s
            t + s

            t + s
            t + s
            t + s
            t + s
            t + s

            t + s
            t + s
            t + s
            t + s
            t + s

            t + s
            t + s
            t + s
            t + s
            t + s

            t + s
            t + s
            t + s
            t + s
            t + s

            t + s
            t + s
            t + s
            t + s
            t + s

            t + s
            t + s
            t + s
            t + s
            t + s

    def calibrate(self):

        s = join(map(str,range(100)))
        t = join(map(str,range(1,101)))

        for i in xrange(self.rounds):
            pass
            

class CompareStrings(Test):

    version = 0.2
    operations = 10 * 5
    rounds = 200000

    def test(self):

        # Make sure the strings are *not* interned
        s = join(map(str,range(10)))
        t = join(map(str,range(10))) + "abc"

        for i in xrange(self.rounds):
            t < s
            t > s
            t == s
            t > s
            t < s

            t < s
            t > s
            t == s
            t > s
            t < s

            t < s
            t > s
            t == s
            t > s
            t < s

            t < s
            t > s
            t == s
            t > s
            t < s

            t < s
            t > s
            t == s
            t > s
            t < s

            t < s
            t > s
            t == s
            t > s
            t < s

            t < s
            t > s
            t == s
            t > s
            t < s

            t < s
            t > s
            t == s
            t > s
            t < s

            t < s
            t > s
            t == s
            t > s
            t < s

            t < s
            t > s
            t == s
            t > s
            t < s

    def calibrate(self):

        s = join(map(str,range(10)))
        t = join(map(str,range(10))) + "abc"

        for i in xrange(self.rounds):
            pass
            

class CompareInternedStrings(Test):

    version = 0.1
    operations = 10 * 5
    rounds = 200000

    def test(self):

        # Make sure the strings *are* interned
        s = intern(join(map(str,range(10))))
        t = s

        for i in xrange(self.rounds):
            t == s
            t == s
            t >= s
            t > s
            t < s

            t == s
            t == s
            t >= s
            t > s
            t < s

            t == s
            t == s
            t >= s
            t > s
            t < s

            t == s
            t == s
            t >= s
            t > s
            t < s

            t == s
            t == s
            t >= s
            t > s
            t < s

            t == s
            t == s
            t >= s
            t > s
            t < s

            t == s
            t == s
            t >= s
            t > s
            t < s

            t == s
            t == s
            t >= s
            t > s
            t < s

            t == s
            t == s
            t >= s
            t > s
            t < s

            t == s
            t == s
            t >= s
            t > s
            t < s

    def calibrate(self):

        s = intern(join(map(str,range(10))))
        t = s

        for i in xrange(self.rounds):
            pass
            

class CreateStringsWithConcat(Test):

    version = 0.1
    operations = 10 * 5
    rounds = 80000

    def test(self):

        for i in xrange(self.rounds):
            s = 'om'
            s = s + 'xbx'
            s = s + 'xcx'
            s = s + 'xdx'
            s = s + 'xex'

            s = s + 'xax'
            s = s + 'xbx'
            s = s + 'xcx'
            s = s + 'xdx'
            s = s + 'xex'

            s = s + 'xax'
            s = s + 'xbx'
            s = s + 'xcx'
            s = s + 'xdx'
            s = s + 'xex'

            s = s + 'xax'
            s = s + 'xbx'
            s = s + 'xcx'
            s = s + 'xdx'
            s = s + 'xex'

            s = s + 'xax'
            s = s + 'xbx'
            s = s + 'xcx'
            s = s + 'xdx'
            s = s + 'xex'

            s = s + 'xax'
            s = s + 'xbx'
            s = s + 'xcx'
            s = s + 'xdx'
            s = s + 'xex'

            s = s + 'xax'
            s = s + 'xbx'
            s = s + 'xcx'
            s = s + 'xdx'
            s = s + 'xex'

            s = s + 'xax'
            s = s + 'xbx'
            s = s + 'xcx'
            s = s + 'xdx'
            s = s + 'xex'

            s = s + 'xax'
            s = s + 'xbx'
            s = s + 'xcx'
            s = s + 'xdx'
            s = s + 'xex'

            s = s + 'xax'
            s = s + 'xbx'
            s = s + 'xcx'
            s = s + 'xdx'
            s = s + 'xex'

    def calibrate(self):

        for i in xrange(self.rounds):
            pass
            

class StringSlicing(Test):

    version = 0.1
    operations = 5 * 7
    rounds = 100000

    def test(self):

        s = join(map(str,range(100)))

        for i in xrange(self.rounds):

                s[50:]
                s[:25]
                s[50:55]
                s[-1:]
                s[:1]
                s[2:]
                s[11:-11]

                s[50:]
                s[:25]
                s[50:55]
                s[-1:]
                s[:1]
                s[2:]
                s[11:-11]

                s[50:]
                s[:25]
                s[50:55]
                s[-1:]
                s[:1]
                s[2:]
                s[11:-11]

                s[50:]
                s[:25]
                s[50:55]
                s[-1:]
                s[:1]
                s[2:]
                s[11:-11]

                s[50:]
                s[:25]
                s[50:55]
                s[-1:]
                s[:1]
                s[2:]
                s[11:-11]

    def calibrate(self):

        s = join(map(str,range(100)))

        for i in xrange(self.rounds):
            pass

### String methods

if hasattr('', 'lower'):

    class StringMappings(Test):

        version = 0.1
        operations = 3 * (5 + 4 + 2 + 1)
        rounds = 70000

        def test(self):

            s = join(map(chr,range(20)),'')
            t = join(map(chr,range(50)),'')
            u = join(map(chr,range(100)),'')
            v = join(map(chr,range(256)),'')

            for i in xrange(self.rounds):

                s.lower()
                s.lower()
                s.lower()
                s.lower()
                s.lower()

                s.upper()
                s.upper()
                s.upper()
                s.upper()
                s.upper()

                s.title()
                s.title()
                s.title()
                s.title()
                s.title()

                t.lower()
                t.lower()
                t.lower()
                t.lower()

                t.upper()
                t.upper()
                t.upper()
                t.upper()

                t.title()
                t.title()
                t.title()
                t.title()

                u.lower()
                u.lower()

                u.upper()
                u.upper()

                u.title()
                u.title()

                v.lower()

                v.upper()

                v.title()

        def calibrate(self):

            s = join(map(chr,range(20)),'')
            t = join(map(chr,range(50)),'')
            u = join(map(chr,range(100)),'')
            v = join(map(chr,range(256)),'')

            for i in xrange(self.rounds):
                pass

    class StringPredicates(Test):

        version = 0.1
        operations = 10 * 7
        rounds = 80000

        def test(self):

            data = ('abc', '123', '   ', 'äöü', 'ß'*10)
            len_data = len(data)

            for i in xrange(self.rounds):
                s = data[i % len_data]

                s.isalnum()
                s.isalpha()
                s.isdigit()
                s.islower()
                s.isspace()
                s.istitle()
                s.isupper()

                s.isalnum()
                s.isalpha()
                s.isdigit()
                s.islower()
                s.isspace()
                s.istitle()
                s.isupper()

                s.isalnum()
                s.isalpha()
                s.isdigit()
                s.islower()
                s.isspace()
                s.istitle()
                s.isupper()

                s.isalnum()
                s.isalpha()
                s.isdigit()
                s.islower()
                s.isspace()
                s.istitle()
                s.isupper()

                s.isalnum()
                s.isalpha()
                s.isdigit()
                s.islower()
                s.isspace()
                s.istitle()
                s.isupper()

                s.isalnum()
                s.isalpha()
                s.isdigit()
                s.islower()
                s.isspace()
                s.istitle()
                s.isupper()

                s.isalnum()
                s.isalpha()
                s.isdigit()
                s.islower()
                s.isspace()
                s.istitle()
                s.isupper()

                s.isalnum()
                s.isalpha()
                s.isdigit()
                s.islower()
                s.isspace()
                s.istitle()
                s.isupper()

                s.isalnum()
                s.isalpha()
                s.isdigit()
                s.islower()
                s.isspace()
                s.istitle()
                s.isupper()

                s.isalnum()
                s.isalpha()
                s.isdigit()
                s.islower()
                s.isspace()
                s.istitle()
                s.isupper()

        def calibrate(self):

            data = ('abc', '123', '   ', '\u1234\u2345\u3456', '\uFFFF'*10)
            data = ('abc', '123', '   ', 'äöü', 'ß'*10)
            len_data = len(data)

            for i in xrange(self.rounds):
                s = data[i % len_data]


