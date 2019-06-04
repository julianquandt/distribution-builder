import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="distribution-builder",
    version="0.0.1",
    author="Julian Quandt",
    author_email="julian_quandt@live.de",
    description="Distribution builder for `pygame` that can be used to elicit probability / value distributions from people, adapted from Sharpe, Goldstein, and Blythe (2000) and Goldstein, Johnson, and Sharpe (2008).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/julianquandt/distribution_builder",
    include_package_data = True,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)