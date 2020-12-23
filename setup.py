import cosi as c
import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name=c.APP_NAME,
    version=c.APP_VERSION,
    author=c.APP_AUTHOR,
    license=c.APP_LICENSE,
    description=c.APP_DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=c.APP_URL,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "parsedatetime",
        "ConfigArgParse",
        "ballcosmos",
        "SQLAlchemy",
        "requests",
        "pytz",
        "kaitaistruct",
        "psycopg2"
    ],
    extras_require={
        "dev": [
            "pytest",
            "wheel"
        ]
    },
    python_requires='>=3.8.5',
    entry_points={
        "console_scripts": [
            '{} = cosi.__main__:main'.format(c.APP_NAME),
        ]
    }
)
