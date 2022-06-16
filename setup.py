import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='grid_pptx',  # This is the name of the package
    version='0.1',  # The initial release version
    author_email='max.hill@pm.me',
    description='Simplifying the PowerPoint creation process in Python',
    long_description=long_description,  # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),  # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],  # Information to filter the project on PyPi website
    python_requires='>=3.6',  # Minimum version requirement of the package
    py_modules=["grid_pptx"],  # Name of the python package
    url='http://github.com/rogue26/grid_pptx',
    package_dir={'': 'src'},  # Directory of the source code of the package
    license='MIT',
    zip_safe=False,
    install_requires=[
        'python-pptx==0.6.21',
        'pandas==1.4.2',
    ]  # Install other dependencies if any
)
