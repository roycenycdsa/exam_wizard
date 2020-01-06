from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='examwiz_pkg',
    packages=['examwiz_pkg'],
    include_package_data=True,
    description='Exam Grading and Reporting Automation',
    license="SupStat Inc.",
    long_decription=long_description,
    author='Charles Cohen',
    author_email='charles.cohen@nycdatascience.com',
    install_requires=[
        "google_auth_oauthlib",
        "google-api-python-client",
        "pyyaml",
        "jupyter",
        "pandas"
    ]
)