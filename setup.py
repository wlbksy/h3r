from setuptools import find_packages, setup

setup(name='h3r',
      version='0.1',
      description='h3 rotated',
      author='WANG Lei',
      author_email='wlbksy@126.com',
      license='MIT',
      packages=find_packages(),
      platforms=['Windows', 'Linux', 'Mac OS-X'],
      install_requires=['numpy', 'h3'],
      python_requires='>=3.5',
      classifiers=[
          'Intended Audience :: Education',
          'Intended Audience :: Science/Research',
          'Programming Language :: Python :: 3 :: Only',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Mathematics',
      ],
      zip_safe=False,
      setup_requires=['pytest-runner'],
      tests_require=['pytest']
      )
