import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "rhythmunity",
    version = "0.1.0",
    author = "Salim Rahmani",
    author_email = "SalimRahmani@outlook.com",
    description = ("Application to generate Rehearsals schedule"
                                   "of Rhythm Unity (Music Club) Members."),
    license = "The MIT License: http://www.opensource.org/licenses/mit-license.php",
    keywords = "example documentation tutorial",
    url = "https://github.com/SalimRahmani/RhythmUnity",
    packages=['rhythmunity', 'tests'],
    long_description=read('README'),
    classifiers=[
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        "Topic :: Office/Business :: Scheduling",
        "License :: OSI Approved :: MIT License",
    ],
)

