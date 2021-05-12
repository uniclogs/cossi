import setuptools
import cossi as c

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
    project_urls={
        'Documentation': 'https://uniclogs-cosi.readthedocs.io',
        'Bug Tracking': 'https://github.com/oresat/uniclogs-cossi/labels/bug'
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Information Analysis"
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
            "setuptools",
            "wheel",
            "flake8",
            "twine",
            "sphinx",
            "sphinx_rtd_theme",
        ]
    },
    python_requires='>=3.8.5',
    entry_points={
        "console_scripts": [
            f'{c.APP_NAME} = cossi.__main__:main',
        ]
    }
)
