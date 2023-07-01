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