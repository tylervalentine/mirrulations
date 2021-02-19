from setuptools import setup, find_packages

setup(
    name="c21server",
    packages=find_packages('src'),
    package_dir={'': 'src'}
)

setup(
    name="c21client",
    packages=find_packages('src'),
    package_dir={'': 'src'}
)
