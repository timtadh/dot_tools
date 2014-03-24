try:
    from setuptools import setup
    # arguments that distutils doesn't understand
    setuptools_kwargs = {
        'install_requires': [
          'ply',
          'betterast',
        ],
        'provides': ['dot_tools'],
        'zip_safe': False
    }
except ImportError:
    from distutils.core import setup
    setuptools_kwargs = {}

setup(name='dot_tools',
      version=0.1,
      description=(
        'Parser and Generator for the graphviz dot language.'
      ),
      author='Tim Henderson',
      author_email='tadh@case.edu',
      url='http://hackthology.com',
      packages=['dot_tools'],
      platforms=['unix'],
      scripts=[],
      **setuptools_kwargs
)

