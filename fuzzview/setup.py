from setuptools import setup, find_packages

setup(
    name='fuzzview',
    version='0.1',
    description='Viewer for program fuzzing',
    url='https://github.com/vasilyrud/fuzzview',
    author='Vasily Rudchenko',
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Security',
        'Topic :: Software Development :: Testing',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=['pytest', 'Pillow', 'palettable'],
)
