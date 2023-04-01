# Data Agent

Its a project that aims to read data for multiple sensors in raspberry pi and store that data in an SQLite database

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all needed libraries.

```bash
pip install requirements.txt
```

## Usage
command for test
```shell
python -m unittest discover
```
command for flake8
```shell
flake8 --config setup.cfg
```
command for pylint
```shell
pylint --rcfile=setup.cfg main
```

lunch the script, need to specify the path for the config file
```shell
# example
python main.py -c ./tests/utils/

```
### connect to raspberripi
user: pi
pwd: admin
ssh pi@raspberrypi
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
Agric 4.0

## Authors and acknowledgment

Great thanks to Lhoussaine AAMER, Brahim AAMER & Youssef IZIKITNE

## Contact

```diff
++
Email: lhoussaine.aamer@outlook.fr
++
```
