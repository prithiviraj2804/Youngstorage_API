#!/bin/bash
echo "$1" | sudo -S sh -c wg syncconf wg0 <(wg-quick strip wg0)
echo "VPN activated"
