from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='shell2-cli',
    version='0.1065',
    packages=find_packages(),
    install_requires=[
        'shell2',
        'prettyprinter',
        'inquirer',
        'rich',
        'prompt_toolkit',
        'colorama',
        'google-cloud-firestore',
        'google-auth',
        'requests',
        'retry',
        'python-slugify',
        'py7zr',
        'openai',
        'rhasspy-silence',
        'webrtcvad',
        'pyaudio'
    ],
    entry_points={
        'console_scripts': [
            'shell2_cli_menu = scripts.shell2_cli_menu:main', # i switch the order of these two and it ceases working ... !
            'shell2_cli_live = scripts.shell2_cli_live:main',
            'shell2 = scripts.shell2_cli:main'
        ]
    },
    long_description=long_description,
    long_description_content_type='text/markdown'
)
