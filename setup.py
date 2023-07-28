from setuptools import setup

setup(
    name="folio-web",
    version="0.1",
    description="A small package for a front end to Folio as well as simple API entries and scripts",
    url="https://github.com/balljok/folio_web",
    author="Håkan Sundblad",
    author_email="hakan.sundblad@liu.se",
    license="None",
    packages=[
        "foliocommunication",
        "foliologging",
    ],
    install_requires=[
        "python-dotenv",
        "requests",
    ],
    zip_safe=False,
)
