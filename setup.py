from setuptools import setup, find_packages

setup(
    name="infra-cli",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "pyyaml",
        "jsonschema",
        "jinja2",
        "python-dotenv",
        "boto3",
        "requests"
    ],
    entry_points={
        'console_scripts': [
            'infra-cli=cli.main:cli',
        ],
    },
)
