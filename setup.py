from setuptools import setup

setup(
      name='Investment Analysis',
      version='0.1',
      description='Tools and GUI for analysis of capital markets',
      url='https://github.com/sabend/investment-analysis-board',
      author='Stephan Abend',
      # author_email='',
      license='UNKNOWN',
      packages=['investment-analysis'],
      install_requires=[
            'bs4',
            'datetime',
            'dateutil',
            'dash',
            'dash_bootstrap_components',
            'dash_core_components',
            'dash_html_components',
            'pandas',
            'plotly',
            're',
            'requests',
            'selenium'
      ],
      zip_safe=False
)
