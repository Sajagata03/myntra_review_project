from setuptools import find_packages, setup

setup(
    name='scrapper',
    version='0.0.1',
    author='sajagata',
    author_email='sajagataojha@gmail.com',
    packages=find_packages(),
    install_requires=[]
)

# if we want to trigger setup.py from req.txt we use -e.