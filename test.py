import base64
import zlib


value = "eJxjZGBgYIRiViBmR+KjY2R5JiBmxiMPYrORIA8yjxuPPIwPk+cAYk488jAMAEucAL0="


def base64_zlib_to_csv(value):
    # decode
    result = base64.b64decode(value)
    result = zlib.decompress(result)

    # cast byte representation to int
    mem_view = memoryview(result)
    mem_view = mem_view.cast('I')

    return ", ".join(str(index) for index in mem_view)


def f(x, m='a'):
    z = 2
    t = 3

    def g():
        #nonlocal t
        foo = m
        print(locals())

        return x
    return g



h = f(5)
h = f(6)
x = h()
print(h.__dict__)
print(h.__code__.co_freevars)
print(h.__code__.co_varnames)
print(h.__code__.co_argcount)