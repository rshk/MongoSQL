import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

version = '0.1'
install_requires = [
    'ply',
    'six',
    'pymongo',
]
tests_require = [
    'pytest',
    'pytest-pep8',
    'pytest-cov',
]

extra = {}
if sys.version_info >= (3,):
    extra['use_2to3'] = True


class PyTest(TestCommand):
    test_package_name = 'mongosql'

    def finalize_options(self):
        TestCommand.finalize_options(self)
        _test_args = [
            '--verbose',
            '--ignore=build',
            #'--cov={0}'.format(self.test_package_name),
            #'--cov-report=term-missing',
            '--pep8',
        ]
        extra_args = os.environ.get('PYTEST_EXTRA_ARGS')
        if extra_args is not None:
            _test_args.extend(extra_args.split())
        self.test_args = _test_args
        self.test_suite = True

    def run_tests(self):
        import pytest
        from pkg_resources import normalize_path, _namespace_packages

        # Purge modules under test from sys.modules. The test loader will
        # re-import them from the build location. Required when 2to3 is used
        # with namespace packages.
        if sys.version_info >= (3,) and \
                getattr(self.distribution, 'use_2to3', False):
            #module = self.test_args[-1].split('.')[0]
            module = self.test_package_name
            if module in _namespace_packages:
                del_modules = []
                if module in sys.modules:
                    del_modules.append(module)
                module += '.'
                for name in sys.modules:
                    if name.startswith(module):
                        del_modules.append(name)
                map(sys.modules.__delitem__, del_modules)

            ## Run on the build directory for 2to3-built code
            ## This will prevent the old 2.x code from being found
            ## by py.test discovery mechanism, that apparently
            ## ignores sys.path..
            ei_cmd = self.get_finalized_command("egg_info")

            ## Replace the module name with normalized path
            #self.test_args[-1] = normalize_path(ei_cmd.egg_base)
            self.test_args.append(normalize_path(ei_cmd.egg_base))

        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='MongoSQL',
    version=version,
    packages=find_packages(),
    url='http://rshk.github.io/mongosql',
    license='BSD License',
    author='Samuele Santi',
    author_email='samuele@samuelesanti.com',
    description='NoSQL means "not only..."',
    long_description='NoSQL means "not only..."',
    install_requires=install_requires,
    test_suite='mongosql.tests',
    tests_require=tests_require,
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        #"Programming Language :: Python :: Implementation :: PyPy",
    ],
    package_data={'': ['README.md', 'LICENSE']},
    cmdclass={'test': PyTest},
    **extra)
