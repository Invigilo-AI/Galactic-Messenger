from setuptools import find_packages, setup

setup(
    name="galactic-messenger",
    version="0.1.4",
    author="InvigiloAI",
    author_email="contact@invigilo.ai",
    description="Galactic Messenger is a versatile and efficient Python package designed for sending messages across multiple platforms.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Invigilo-AI/Galactic-Messenger",
    packages=find_packages(),
    install_requires=open("requirements.txt").readlines(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
