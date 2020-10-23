import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Heaty",
    version="2020.10b1",
    author="Tom Christiaens",
    author_email="tom.chr@proximus.be",
    description="A building heat load calculator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TomLXXVI/heaty",
    keywords=['building heat load calculator', 'EN 12831-1'],
    license='BSD v3',
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: BSD License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ],
    python_requires=">=3.8",
    install_requires=["PyQt5", "Pint"],
    package_data={
        'heaty.gui.resources': ['*.html', '*.ico', '*.pdf']
    },
    platforms=['Win32 (MS Windows)'],
    entry_points={
        'console_scripts': ['heaty = heaty.__main__:main']
    }
)
