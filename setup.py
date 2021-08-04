from setuptools import setup, find_packages


setup(
    name="smb3-leaderboards",
    version="0.1.0",
    description=("Super Mario Bros 3 Leaderboards"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="smb3-leaderboards",
    author="Jon Robison",
    author_email="narfman0@gmail.com",
    license="LICENSE",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=["requests"],
    test_suite="tests",
)
