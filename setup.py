from setuptools import setup, find_packages

setup(
    name = "pwnbox",
    version = "0.5pre1",
    packages = find_packages(),
    setup_requires = ['sphinx'],
    install_requires = ['six'],
    test_suite = "nose.collector",
    tests_require = ["nose", "pycrypto"],
    author = "Hyeonseop Lee",
    author_email = "hyeonseop@ls-al.me",
    url = "http://github.com/protos37/pwnbox"
)
