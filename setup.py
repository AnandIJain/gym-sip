from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="gym_sips",
    version="0.20",
    description="gym env for sports betting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Anand Jain",
    author_email="anandj@uchicago.edu",
    packages=["gym_sips"],  # same as name
    url="https://github.com/anandijain/gym-sips",
    install_requires=[
        "pandas",
        "numpy",
        "torch",
        "gym",
        # "spinup"
    ],  # external packages as dependencies
    python_requires=">=3.6",
)
