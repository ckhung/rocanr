from setuptools import setup

setup(
    name='rocanr',
    packages=['rocanr'],
    include_package_data=True,
    install_requires=[
        'rocanr',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)

