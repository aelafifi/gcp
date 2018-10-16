#!/usr/bin/env python3

import setuptools

name = 'gcp'

setuptools.setup(
    name=name,
    version='0.2.1.dev1',
    url='https://code.lm7.fr/mcy/gcp',
    license='GPL-3+',

    description="An advanced file copy tool loosely inspired from cp",
    long_description_content_type='text/markdown',
    long_description="""
    **%s** is a command-line tool to copy files, loosely inspired from the `cp`
    command, but with higher-level functionalities such as progress bar, copy
    continuation on error, logging to know which files were successfully
    copied, name mangling to workaround filesystem limitations (FAT), unique
    copy queue, copy list management, etc.""" % name,
    keywords='file copy',

    author='Goffi (Jérôme Poisson)',
    author_email='goffi@goffi.org',
    maintainer='Matteo Cypriani',
    maintainer_email='mcy@lm7.fr',

    # Cf. https://pypi.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],

    scripts=['gcp'],
#    entry_points={
#        'console_scripts': ['gcp=gcp:main'],
#    },
    data_files=[
        ('man/man1', ["gcp.1"]),
        ('share/locale/fr/LC_MESSAGES', ['i18n/fr/LC_MESSAGES/gcp.mo']),
        ('share/doc/%s' % name, ['CHANGELOG', 'LICENSE', 'README.md']),
    ],
    install_requires=['PyGObject', 'dbus-python'],
    python_requires='>=3',
)
