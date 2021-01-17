import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="EasyDraw",
    version="0.6.3",
    author="Vafa Karamzadegan",
    author_email="vafa.k@live.com",
    description="A graphical library built for visual arts. EasyDraw is built on top of tkinter and has more functionalities.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vafakaramzadegan/EasyDraw",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "pyscreenshot",
        "Pillow",
        "multipledispatch"
    ]
)
