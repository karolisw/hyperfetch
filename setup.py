from setuptools import setup, find_packages

# To read ReadMe content
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='hyperfetch-test2',
    version='0.1.0',
    description='HyperFetch. An interface for optimizing RL hyperparameters through the HyperFetch API. ',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/karolisw/hyperFetch',
    author='Karoline Sund Wahl',
    author_email='karolisw@stud.ntnu.no',
    license='BSD 2-clause',
    packages=find_packages(include=['hyperfetch', 'hyperfetch.*']),
    install_requires=['pytorch==1.13.1',
                      'torchvision==0.14.1',
                      'torchaudio==0.13.1',
                      'numpy',
                      'swig',
                      'codecarbon',
                      'databases',
                      'fastapi>=0.89.1',
                      'optuna==3.1.0',
                      'gym==0.21.0',
                      'pymongo',
                      'motor>=3.1.1',
                      'motor-stubs',
                      'mypy',
                      'pandas',
                      'pyaml',
                      'pydantic>=1.10.4',
                      'SQLAlchemy',
                      'stable-baselines3==1.7.0',
                      'starlette>=0.22.0',
                      'uvicorn',
                      'absl-py==1.4.0',
                      'alembic==1.9.3',
                      'anyio==3.6.2',
                      'arrow==1.2.3',
                      'attrs==22.2.0',
                      'bcrypt==4.0.1',
                      'box2d-py==2.3.5',
                      'cachetools==5.3.0',
                      'certifi==2022.12.7',
                      'chardet==5.1.0',
                      'charset-normalizer==3.0.1',
                      'click==8.1.3',
                      'cloudpickle==1.6.0',
                      'cmaes==0.9.1',
                      'colorama==0.4.6',
                      'colorlog==6.7.0',
                      'contourpy==1.0.7',
                      'cycler==0.11.0',
                      'databases==0.7.0',
                      'DataProperty==0.55.0',
                      'dnspython==2.3.0',
                      'email-validator==1.3.1',
                      'exceptiongroup==1.1.1',
                      'filelock==3.9.0',
                      'fonttools==4.38.0',
                      'fuzzywuzzy==0.18.0',
                      'google-auth==2.16.0',
                      'google-auth-oauthlib==0.4.6',
                      'greenlet==2.0.2',
                      'grpcio==1.51.1',
                      'gym-notices==0.0.8',
                      'gymnasium-notices==0.0.1',
                      'h11==0.14.0',
                      'httpcore==0.16.3',
                      'httptools==0.5.0',
                      'httpx==0.23.3',
                      'huggingface-hub==0.12.0',
                      'huggingface-sb3==2.2.4',
                      'idna==3.4',
                      'importlib-metadata==4.13.0',
                      'iniconfig==2.0.0',
                      'itsdangerous==2.1.2',
                      'jax-jumpy==0.2.0',
                      'Jinja2==3.1.2',
                      'joblib==1.2.0',
                      'kiwisolver==1.4.4',
                      'Mako==1.2.4',
                      'Markdown==3.4.1',
                      'markdown-it-py==2.1.0',
                      'MarkupSafe==2.1.2',
                      'matplotlib==3.6.3',
                      'mbstrdecoder==1.1.2',
                      'mdurl==0.1.2',
                      'mypy-extensions==1.0.0',
                      'oauthlib==3.2.2',
                      'orjson==3.8.5',
                      'packaging==23.0',
                      'passlib==1.7.4',
                      'pathvalidate==2.5.2',
                      'Pillow==9.4.0',
                      'pluggy==1.0.0',
                      'protobuf==3.20.3',
                      'psutil==5.9.4',
                      'py-cpuinfo==9.0.0',
                      'pyasn1==0.4.8',
                      'pyasn1-modules==0.2.8',
                      'pygame == 2.1.0',
                      'pyglet == 1.5.27',
                      'Pygments == 2.14.0',
                      'pynvml==11.5.0',
                      'PyOpenGL==3.1.6',
                      'pyparsing==3.0.9',
                      'pytablewriter==0.64.2',
                      'pytest==7.2.2',
                      'python-benedict'
                      'python-dateutil==2.8.2',
                      'python-dotenv==0.21.1',
                      'python-multipart==0.0.5',
                      'pytz==2022.7.1',
                      'PyYAML==6.0',
                      'requests==2.28.2',
                      'requests-oauthlib==1.3.1',
                      'rfc3986==1.5.0',
                      'rich==13.3.1',
                      'rl-zoo3==1.7.0',
                      'rsa==4.9',
                      'sb3-contrib==1.7.0',
                      'scikit-learn==1.2.1',
                      'scikit-optimize==0.9.0',
                      'scipy==1.10.0',
                      'six==1.16.0',
                      'sniffio==1.3.0',
                      'tabledata==1.3.0',
                      'tcolorpy==0.1.2',
                      'tensorboard==2.11.2',
                      'tensorboard-data-server==0.6.1',
                      'tensorboard-plugin-wit==1.8.1',
                      'threadpoolctl==3.1.0',
                      'tomli==2.0.1',
                      'tqdm==4.64.1',
                      'typepy==1.3.0',
                      'types-PyYAML==6.0.12.8',
                      'typing_extensions==4.4.0',
                      'ujson==5.7.0',
                      'urllib3==1.26.14',
                      'wasabi==1.1.1',
                      'watchfiles==0.18.1',
                      'websockets==10.4',
                      'Werkzeug==2.2.2',
                      'zipp==3.12.1'
                      ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Microsoft :: Windows :: Windows 11',
        'Programming Language :: Python :: 3.10',
        'Framework :: FastAPI'
    ],
)
