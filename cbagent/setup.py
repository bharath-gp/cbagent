from setuptools import setup

version = '0.1'

setup(
    name='cbagent',
    version=version,
    url="https://github.com/couchbase/cbmonitor",
    classifiers=[
        "Intended Audience :: Developers",
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        "Operating System :: POSIX",
        "License :: OSI Approved :: Apache Software License",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Terminals'
    ],
    author="Couchbase",
    author_email="admin@couchbase.com",
    license="Apache Software License",
    packages=["collectors", "stores"],
    py_modules=["metadata_client", "ns_collector"],
    entry_points={
        'console_scripts': ['ns_collector = ns_collector:main']
    },
    include_package_data=True,
    install_requires=[
        'requests',
        'seriesly',
    ],
)