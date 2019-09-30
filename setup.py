import setuptools

setuptools.setup(
    name='linguini',
    version='0.0.1',
    author='rjboas',
    description='A Flask web app',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'flask-login',
    ],
    url="https://github.com/rjboas/linguini",
    python_requires='>=3.6',
)