from setuptools import setup, find_packages


setup(
    name='Mcq-Generator',
    version='0.1',
    author='Vansh Malhotra',
    author_email='vanshmalhotra353@gmail.com',
    install_requires=['openai','langchain','streamlit','python-dotenv','PyPDF2'],
    packages=find_packages()
    )
    