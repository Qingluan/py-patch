
from setuptools import setup, find_packages


setup(name='py_patch',
    version='0.0.3',
    description='some',
    url='https://github.com/xxx',
    author='auth',
    author_email='xxx@gmail.com',
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': ['x-patch-py=py_patch_src.cmd:main']
    },

)
