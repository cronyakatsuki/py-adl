from setuptools import setup, find_packages

try:
    LONG_DESCRIPTION = open("README.md").read()
except IOError:
    LONG_DESCRIPTION = __doc__

VERSION = '0.1.5'
NAME = "py-adl"
DESCRIPTION = 'Python wrapper for trackma and anime-downloader'
REQUIREMENTS = ['trackma', 'pillow']

setup(
    name=NAME,
    version=VERSION,
    packages=find_packages(),

    install_requires=REQUIREMENTS,
    
    entry_points='''
        [console_scripts]
        py-adl=py_adl.adl:main
    ''',
    package_data={'': ['py_adl/good_title.txt', 'py_adl/problem_title.txt']},
    include_package_data=True,

    author='CronyAkatsuki',
    author_email='cronyakatsuki@gmail.com',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/cronyakatsuki/py-adl',
    keywords='list manager, anime, watch',
    license="GPL-3",
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'Topic :: Internet',
        'Programming Language :: Python :: 3',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ]
    )