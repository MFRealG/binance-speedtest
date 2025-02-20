import subprocess
import requests
import time
import socket
import json
import statistics
import websocket
import os
from tabulate import tabulate
from tqdm import tqdm

BINANCE_APIS = {
    "fapi": "https://fapi.binance.com/fapi/v1/ping",
    "api": "https://api.binance.com/api/v3/ping"
}
BINANCE_WS_SUBSCRIPTION = {
    "fapi": {"method": "SUBSCRIBE", "params": ["btcusdt@aggTrade"], "id": 1},
    "api": {"method": "SUBSCRIBE", "params": ["btcusdt@trade"], "id": 1}
}
BINANCE_WS = {
    "fapi": "wss://fstream.binance.com/ws",
    "api": "wss://stream.binance.com:9443/ws/!ticker@arr"
}
ERROR_LOG = "error.log"
RESULTS_FILE = "results.txt"


def log_error(message):
    with open(ERROR_LOG, "a") as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")


def save_results(results, title):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    with open(RESULTS_FILE, "a") as file:
        file.write(f"\n[{timestamp}] \n* {title} *\n")
        for key, value in results.items():
            if value is not None:
                file.write(f"{key}: {value:.4f} sec\n")


def get_binance_ip(api_url):
    try:
        hostname = api_url.split("//")[-1].split("/")[0]
        return socket.gethostbyname(hostname)
    except socket.gaierror as e:
        log_error(f"Error retrieving IP: {e}")
        return None


def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip()


def measure_latency(task_name, func, progress_bar, *args):
    result = func(*args)
    progress_bar.update(1)
    return result


def measure_ping(ip, count=10):
    try:
        output = run_command(f"ping -c {count} {ip}")
        for line in output.split("\n"):
            if "avg" in line:
                return float(line.split("/")[-3])
    except Exception as e:
        log_error(f"Ping measurement error: {e}")
    return None


def measure_curl_latency(api_url):
    try:
        output = run_command(
            f'curl -o /dev/null -s -w "Connect: %{{time_connect}}s\nTTFB: %{{time_starttransfer}}s\nTotal: %{{time_total}}s\n" {api_url}')
        latencies = {}
        for line in output.split("\n"):
            if "Connect" in line:
                latencies["connect"] = float(line.split(": ")[1].replace("s", ""))
            elif "TTFB" in line:
                latencies["ttfb"] = float(line.split(": ")[1].replace("s", ""))
            elif "Total" in line:
                latencies["total"] = float(line.split(": ")[1].replace("s", ""))
        return latencies
    except Exception as e:
        log_error(f"Curl measurement error: {e}")
        return {}


def measure_api_latency(api_url):
    try:
        times = []
        for _ in range(5):
            start = time.time()
            requests.get(api_url).raise_for_status()
            times.append(time.time() - start)
        return statistics.mean(times)
    except Exception as e:
        log_error(f"API latency measurement error: {e}")
        return None


def measure_ws_latency(ws_url, subscription_message=None):
    ws = websocket.WebSocket()
    try:
        ws.connect(ws_url, timeout=5)
        if subscription_message:
            ws.send(json.dumps(subscription_message))
        times = []
        for _ in range(5):
            start = time.time()
            ws.recv()
            times.append(time.time() - start)
        ws.close()
        return statistics.mean(times)
    except Exception as e:
        log_error(f"WebSocket latency measurement error: {e}")
        return None


def analyze_results(results, title):
    headers = ["Metric", "Value"]
    data = [[key, f"{value:.4f} sec"] for key, value in results.items() if value is not None]
    print(f"\n=== {title} ===")
    print(tabulate(data, headers=headers, tablefmt="grid"))
    save_results(results, title)


def main():
    print("Select API for testing: 1 - Futures (fapi.binance.com), 2 - Spot (api.binance.com), 3 - Both")
    choice = input("Enter 1, 2, or 3: ").strip()
    server_name = os.uname().nodename

    tasks = []
    total_steps = 6 if choice in ["1", "2"] else 12
    with tqdm(total=total_steps, desc="Running Tests", bar_format="{l_bar}{bar} {n_fmt}/{total_fmt}") as pbar:
        if choice in ["1", "3"]:
            fapi_subscription = {"method": "SUBSCRIBE", "params": ["btcusdt@aggTrade"], "id": 1}
            tasks.append(("Futures API Latency", {
                "ping": measure_latency("Measuring Ping", measure_ping, pbar, get_binance_ip(BINANCE_APIS["fapi"])),
                "curl_connect": measure_latency("Measuring Curl Connect", measure_curl_latency, pbar,
                                                BINANCE_APIS["fapi"]).get("connect"),
                "curl_ttfb": measure_latency("Measuring Curl TTFB", measure_curl_latency, pbar,
                                             BINANCE_APIS["fapi"]).get("ttfb"),
                "curl_total": measure_latency("Measuring Curl Total", measure_curl_latency, pbar,
                                              BINANCE_APIS["fapi"]).get("total"),
                "api_latency": measure_latency("Measuring API Latency", measure_api_latency, pbar,
                                               BINANCE_APIS["fapi"]),
                "websocket_latency": measure_latency("Measuring WebSocket Latency", measure_ws_latency, pbar,
                                                     BINANCE_WS["fapi"], fapi_subscription),
            }))

        if choice in ["2", "3"]:
            tasks.append(("Spot API Latency", {
                "ping": measure_latency("Measuring Ping", measure_ping, pbar, get_binance_ip(BINANCE_APIS["api"])),
                "curl_connect": measure_latency("Measuring Curl Connect", measure_curl_latency, pbar,
                                                BINANCE_APIS["api"]).get("connect"),
                "curl_ttfb": measure_latency("Measuring Curl TTFB", measure_curl_latency, pbar,
                                             BINANCE_APIS["api"]).get("ttfb"),
                "curl_total": measure_latency("Measuring Curl Total", measure_curl_latency, pbar,
                                              BINANCE_APIS["api"]).get("total"),
                "api_latency": measure_latency("Measuring API Latency", measure_api_latency, pbar, BINANCE_APIS["api"]),
                "websocket_latency": measure_latency("Measuring WebSocket Latency", measure_ws_latency, pbar,
                                                     BINANCE_WS["api"]),
            }))

    for title, results in tasks:
        analyze_results(results, f"{title} for {server_name}")


if __name__ == "__main__":
    main()
