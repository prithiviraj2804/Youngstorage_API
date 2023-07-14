<?php
$ip = file_get_contents('https://api.ipify.org');
echo "Your public IP address is: " . $ip;
?>
