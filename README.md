

# Traffic-1-10
</b> We understand that many users in Iran have severe restrictions from Iran's data centers, so we have decided to create a
script based on the udp protocol, which can bypass the 1/10 limitation of Iran's servers.</br>

Usage: `python Traffic-1-10/Traffic-1-10.py <ip> -p <port> -t <time> -s <size>`

Use cron job (crontab -e) epeat and increase output traffic (upload).<br>
for example : ` * * * * *  python Traffic-1-10/Traffic-1-10.py <ip> -p <port> -t <time> -s <size>`<br>
It will work every minute and restart the Python service every two minutes with the following command so that your ISP does<br>
not notice unusual traffic. <br>
command : `pkill -9 python`<br>

 <h1> On your server run </h1>
 Install with one click 
<pre> wget https://raw.githubusercontent.com/alirezaezzatofficial/Traffic-1-10/main/setup.sh && bash setup.sh </pre>    
 

Only the IP is required.<hr>
If no port is specified, it will send packets on random ports.<br>
If no time is specified, it will take forever. The time is in seconds.<br>
Size defaults to 1024 bytes. The maximum value is 65530.<br>
  

