# Rasp Data Collector

Its a project that aims to read data for multiple sensors in raspberry pi and store that data in an SQLite or InfluxDB database.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all needed libraries.

```bash
pip install -r requirements.txt
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
python main.py -c <PATH_TO_JSON_CONFIG_FILE>

```

## Tools
### Raspberripi
[Vscode remote ssh extension](https://code.visualstudio.com/docs/remote/ssh) has been used in this project in order to connect with raspberry an devlop inside it
```
user: pi
pwd: admin
ssh pi@raspberrypi
```

### InfluxDB
InfluxDB version has been installed over raspbeerypi for more information check this [tutorial](https://pimylifeup.com/raspberry-pi-influxdb/)

```shell
sudo apt update
sudo apt upgrade

curl https://repos.influxdata.com/influxdata-archive.key | gpg --dearmor | sudo tee /usr/share/keyrings/influxdb-archive-keyring.gpg >/dev/null

echo "deb [signed-by=/usr/share/keyrings/influxdb-archive-keyring.gpg] https://repos.influxdata.com/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/influxdb.list

sudo apt update
sudo apt install influxdb
sudo systemctl start influxdb
sudo service influxdb status

```

```
user: admin
pwd: admin123
http://192.168.1.15:8086
```

![](/docs/img/influxdb1.png)
![](/docs/img/influxdb2.png)

### Grafana
check docker compose file
```
http://192.168.1.15:3000/login
user: admin123
pwd: admin123
```

![](/docs/img/grafana1.png)
![](/docs/img/grafana2.png)
![](/docs/img/grafana3.png)


## Roadmap

Here's a list of upcoming features and planned enhancements for this project. We are continuously working to improve and expand its capabilities.

- **Feature 1**: Add other sink to store data like PostgreSQL, Prometheus and make data sink to be configured in the json file or seprately in a file.
- **Feature 2**: Add an sh script part so that the agent will be a linux service.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Authors and acknowledgment

- Lhoussaine AAMER

## License
Agric 4.0

## Contact

```diff
++
Email: lhoussaine.aamer@outlook.fr
++
```
