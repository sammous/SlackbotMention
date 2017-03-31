from setuptools import setup, find_packages

setup(
    # Application name
    name='Annotation',

    # Version number (initial)
    version='0.1.0',

    # Application author details:
    author='Sami Moustachir',
    author_email='sami@mention.com',

    # Packages
    packages=find_packages(where='src'),
    package_dir={'': 'src'},

    long_description=open('README.md').read(),

    include_package_data=True,

    # Dependent packages (distributions)
    install_requires=[
        'aniso8601==1.2.0',
        'click==6.6',
        'Flask==0.11.1',
        'Flask-RESTful==0.3.5',
        'itsdangerous==0.24',
        'Jinja2==2.8',
        'MarkupSafe==0.23',
        'mysqlclient==1.3.9',
        'nltk==3.2.2',
        'pluggy==0.4.0',
        'py==1.4.31',
        'python-dateutil==2.5.3',
        'pytz==2016.7',
        'requests==2.11.1',
        'schedule==0.4.2',
        'six==1.10.0',
        'slackclient==1.0.5',
        'tox==2.4.1',
        'uWSGI==2.0.14',
        'virtualenv==15.0.3',
        'websocket-client==0.40.0',
        'Werkzeug==0.11.11',
    ],
)
