import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lidar_localization_dl",
    version="1.0.0",
    author="Sven Schultze, Dennis Lindt, Svenja Schuirmann",
    author_email="sven.schultze@uol.de, dennis.lindt@uol.de, svenja.schuirmann@uol.de",
    description="Indoor LiDAR Localization with Deep Learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/svenschultze/Lidar-Localization-DL",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'numpy',
        'tensorflow',
    ]
)