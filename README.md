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
WIREGUARD_PUBLIC_KEY="public key"
WIREGUARD_SERVER="VPN Server IP"
AllowedIPs="Allowed IPs"
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