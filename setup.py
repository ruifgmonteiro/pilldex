from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()
        
setup(
    name='pilldex',
    version='1.0.0',
    description='Pill recognition API',
    long_description=readme(),
    author='Rui Monteiro',
    author_email='ruifgmonteiro@gmail.com',
    url='https://github.com/ruifgmonteiro/pilldex',
    packages=find_packages(include=['pilldex', 'pilldex.*']),
    install_requires=[
          'markdown'
    ],
    license='MIT',
    include_package_data=True
)