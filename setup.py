from setuptools import setup

setup(
    name = "pwnbox",
    version = "0.4",
    packages = ["pwnbox"],
    test_suite = "nose.collector",
    tests_require = ["nose", "pycrypto"],
    author = "Hyeonseop Lee",
    author_email = "hyeonseop@ls-al.me",
    url = "http://github.com/protos37/pwnbox"
)
