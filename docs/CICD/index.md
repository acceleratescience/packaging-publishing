# Continuous Integration and Deployment
So far, we have refactored our code, wrote some tests, built and published our package, and made some documentation. But what if the project grows in size, or we have to make continuous changes to the software? Can we automate this process?

We want to achieve the following goals:

1. Automatically detect and fix issues with our code, including:
    - Style
    - Typing clashes
    - Syntax errors
    - Organization of imports

2. Automatically test our code to protect against pushing faulty code to production.

3. Automatically publish our package, which includes:
    - Build the distribution
    - Create a release on GitHub
    - Create a release on PyPI
    - Update version numbers

4. Automatically generate and publish our documentation,

We can achieve all of this using [GitHub Actions](https://docs.github.com/en/actions).