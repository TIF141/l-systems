from setuptools import setup

requirements = ["scikit-image"]

setup(
    name="lsystems",
    version="0.1",
    description="",
    license="MIT",
    install_requires=requirements,
    extras_require={"dev": ["flake8", "pytest", "pytest-cov"]},
)
