
with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="cocoplus",
    version="0.1",
    author="Ramin Nabati",
    description="An enhanced API for working with the COCO dataset",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mrnabati/cocoapi_plus",
    packages=setuptools.find_packages(exclude=['tests', '__pycache__', '*.__pycache__', '__pycache.*', '*.__pycache__.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    python_requires='>=3.6',
)