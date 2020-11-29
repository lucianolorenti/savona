from setuptools import find_packages, setup

setup(
    name='savona',
    packages=find_packages(),
    version='0.2.0',
    description='Jupyter notebook export with beauty in mind',
    author='',
    install_requires=[
        'nbconvert',
        'python-docx',
        'mistletoe'
    ],
    license='MIT',
    include_package_data=True,
)
