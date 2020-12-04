from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='fast_ner', 
    version='0.0.1', 
    description='A Fast Named-Entity Recognition module', 
    long_description=long_description, 
    long_description_content_type='text/markdown', 
    url='https://github.com/loanchip/fast_ner', 
    author='Akshat Pancholi', 
    author_email='itsakshatpancholi@gmail.com', 
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='nlp, ner, keyword-extraction, fuzzy-matching, entity-detection', 
    packages=['fast_ner'], 
    python_requires='>=3.5', 
    install_requires=['pandas>=1.0.5', 'sklearn>=0.23.1'], 
    project_urls={ 
        'Bug Reports': 'https://github.com/loanchip/fast_ner/issues', 
        'Source': 'https://github.com/loanchip/fast_ner/', 
    }, 
)