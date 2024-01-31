from setuptools import setup, find_packages

setup(
    name='pisegment',
    version='0.3',
    description='Light weight semi-supervised image segmentation tool in python.',
    author='Amitoz Azad',
    url='https://github.com/aGIToz/PiSegment',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'numpy',
        'scipy',
        'pyinpaint',
        'pillow',
        'matplotlib',
    ],
    entry_points={
        'console_scripts': [
            'pisegment=pisegment.cli:main',
        ],
    },
)
