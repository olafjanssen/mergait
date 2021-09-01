import setuptools


def requirements():
    with open("requirements.txt", "r") as fh:
        return [x for x in fh.read().split("\n") if x]


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mergait",
    version="0.0.4",
    description="Read and process running gait related dataframes, ranging from raw (iPhone) activity and IMU data to footpod per-step data and music parameters.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/olafjanssen/mergait",
    packages=setuptools.find_packages(),
    author="Olaf T.A. Janssen",
    author_email="olaf.janssen@fontys.nl",
    keywords=[
        "running",
        "gait",
        "mergait",
        "imu",
        "symmetry",
        "accelerometer",
        "footpods",
        "spotify",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    python_requires=">=3.6",
    zip_safe=False,
    install_requires=requirements(),
    include_package_data=True,
)
