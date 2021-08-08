from setuptools import setup, find_packages


setup(
    name="leaderboards-scraper",
    version="0.1.0",
    description=("Super Mario Bros 3 Leaderboards"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="leaderboards-scraper",
    author="Jon Robison",
    author_email="narfman0@gmail.com",
    license="LICENSE",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=["requests", "pydantic", "beautifulsoup4"],
    test_suite="tests",
)
