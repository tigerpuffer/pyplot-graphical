from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyplot-draw-tool',
    version='1.1.0',
    author='红鳍东方鲀',
    author_email='',
    description='A GUI tool for creating various types of charts with Matplotlib',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/pyplot-draw-tool',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'matplotlib',
        'numpy',
        'tkinter'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'pyplot-draw-tool=pyplot_draw_tool.draw_tool:main',
        ],
    },
)