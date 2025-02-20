## binance-speedtest
Binance API speedtest installer. Tested on Ubuntu 22.04

This script will let you measure both Futures and Spot/Magin Binance API's:
- ping
- curl_connect
- curl_ttfb
- curl_total
- api_latency
- websocket_latency

from your server to:
- [fapi.binance.com](https://fapi.binance.com/fapi/v1/ping)
- [api.binance.com](https://api.binance.com/api/v3/ping)
- [wss://fstream.binance.com](wss://fstream.binance.com/ws)
- [wss://stream.binance.com:9443](wss://stream.binance.com:9443/ws/!ticker@arr)

<b>No API keys needed.</b>


## Warinings
- <b>Outgoing/Outbond/Egress ports should be opened: 443 TCP, 80 TCP, 9443 TCP</b>
- If your server's located in the AWS Asia Pacific (Tokyo ap-northeast-1) zone you won't get the ping results from Futures API likely.


## Installation and Run

To install and run the script automatically, use the following command:

```sh
wget https://raw.githubusercontent.com/MFRealG/binance-speedtest/main/install_and_run.sh -O install_and_run.sh && bash install_and_run.sh

