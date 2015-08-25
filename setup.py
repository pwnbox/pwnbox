from setuptools import setup

setup(
    name = "pwnbox",
    version = "0.2.1",
    packages = ["pwnbox"],
    test_suite = "nose.collector",
    tests_require=['nose'],
    author = "protos37",
    author_email = "protos37@gmail.com",
    url = "http://github.com/protos37/pwnbox"
)
