from setuptools import setup, find_packages 

setup(
    name="stock-sentiment-analyzer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'praw'
    ]
)