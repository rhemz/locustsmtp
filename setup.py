from setuptools import setup

setup(
    name='locustsmtp',
    version='0.1',
    description='Generate SMTP load with LocustIO',

    url='https://github.com/rhemz/locustsmtp',
    author='Russ Zeien',
    author_email='rzeien@dyn.com',

    license='MIT',

    packages=[
        'locustsmtp'
    ],

    zip_safe=False,

    install_requires=[
        'locustio'
    ]
)
