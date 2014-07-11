from distutils.core import setup

setup(
    name='pyley',
    version='0.1.0',
    packages=['pyley', 'tests'],
    url='https://github.com/ziyasal/pyley',
    license='LICENSE',
    author='ziyasal',
    author_email='sarikayaziya@gmail.com',
    description='Python client for an open-source graph database Cayley',
    install_requires=['requests'],
    include_package_data=True
)
