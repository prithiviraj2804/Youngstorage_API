# Youngstorage

> A private labs to practic every thing in linux arch

## setup required package

```
sudo apt install wireguard qrencode
```

## project setup
```
git clone https://github.com/prithiviraj2804/Youngstorage_API.git
cd Youngstorage_API
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## .env file setup
```
pip install python-dotenv
```

> create .env in root of the project

```
# wireguard congid
WIREGUARD_PUBLIC_KEY = <private key>
WIREGUARD_SERVER = <server with port>
AllowedIPs = <allowed ips> 

# mqtt server config
MQTT_SERVER = <server url>

# db config for mongo
MONGODB_URL = <url>
MONGODB_NAME = <db name>
DOMAIN_NAME = <domain name>

# JWTconfig
JWT_SECRET_KEY = <secret key>
JWT_ALGORITHM = <algo>

# Email Configuration
MAIL_SERVER = 'smtp.office365.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = <username>
MAIL_PASSWORD = <password>
MAIL_DEFAULT_SENDER = <default send mail>
MAIL_TITLE = <subject>
```

## microservices 

- storage (mongodb)
- data transfer (mqtt)
- fron-end rabbitmq_web_mqtt (paho)

> Rabbitmq server setup and features should be enable

```
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 -p 1883:1883  -p 15674:15674  rabbitmq:3.12-management

# after docker exec 

rabbitmq-plugins enable rabbitmq_mqtt
rabbitmq-plugins enable rabbitmq_web_mqtt 
rabbitmq-plugins enable rabbitmq_web_mqtt_examples
```

> rabbitmq_web_mqtt (15675)
> mqtt (1883)