from setuptools import setup, find_packages

setup(
    name="m11_specification",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "PyPDF2>=3.0.0",
        "pdfplumber>=0.10.2",
        "python-json-logger>=2.0.7",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A package for processing ICH M11 clinical trial protocol documents",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
)
