import setuptools

# Parse requirements.txt
with open("requirements.txt") as f:
    required = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="richterin-great-expectations",  # Replace with your own username
    version="0.0.1",
    author="Omio",
    author_email="open-source@omio.com",
    description="Great Expectations runner for Richterin",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/omio-labs/richterin",
    packages=setuptools.find_packages(),
    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
