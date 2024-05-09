import threading
import time
from ping3 import ping
import socket
import sys
import argparse
from color import colors, fg, bg


# Tool name and help usage
def print_tool_name():
    print(fg.blue + "  ____  _                  ____                         ")
    print(" |  _ \\(_)_ __   __ _     / ___|_      _____  ___ _ __  ")
    print(" | |_) | | '_ \\ / _` |____\\___ \\ \\ /\\ / / _ \\/ _ \\ '_ \\ ")
    print(" |  __/| | | | | (_| |_____|__) \\ V  V /  __/  __/ |_) |")
    print(" |_|   |_|_| |_|\\__, |    |____/ \\_/\\_/ \\___|\\___| .__/ ")
    print("                |___/                            |_|     ")
    print(fg.green + "          Version 0.5 - Simple Ping Sweep Tool" + colors.reset)
    print(fg.purple + "\noptions:")  # Print section for options
    print("  -h, --help            show this help message and exit")
    print("  -i INPUT [INPUT ...], --input INPUT [INPUT ...]")
    print("                        List of IP addresses or DNS names to sweep" + colors.reset)



def resolve_dns(hostname):
    try:
        ip = socket.gethostbyname(hostname)
        return ip
    except socket.gaierror:
        print(fg.red + f"Error: Cannot resolve DNS name {hostname}" + colors.reset)
        sys.exit(1)



def ping_address(ip):
    try:
        response_time = ping(ip, timeout=1)
        if response_time is not None:
            result = f"{fg.green}Reachable ({ip}) - Response Time: {response_time:.2f} ms{colors.reset}"
        else:
            result = f"{fg.red}Unreachable ({ip}){colors.reset}"
    except Exception:
        result = f"{fg.orange}Error pinging {ip}{colors.reset}"
    return result



def start_ping_sweep(targets):
    print_tool_name()
    print("Ping sweep starting for target(s):",','.join(targets))
    print("Pinging.......")
    
    results = {}
    threads = []
    # Creating a lock object
    lock = threading.Lock()
    
    def ping_worker(ip):
        try:
            message = ping_address(ip)
            with lock:
                results[ip] = message
        except Exception as e:
            print(e)
            
    for ip in targets:
        thread = threading.Thread(target=ping_worker, args=(ip,))
        threads.append(thread)
        thread.start()
        
    
    for thread in threads:
        thread.join()
        
    # Printing Pinging results
    print("\nPing results:")
    for ip, message in results.items():
        print(f"{ip}: {message}")
        

    print("\nPing statistics:")
    for ip, message in results.items():
        sent = 1
        received = 1 if "Reachable" in message else 0
        lost = sent - received
        min_time = float('inf')
        max_time = float('-inf')
        total_time = 0
        
        if "Reachable" in message:
            response_time = float(message.split(" ")[-2])
            min_time = min(min_time, response_time)
            max_time = max(max_time, response_time)
            total_time += response_time

        print(f"\nStatistics for {ip}:")
        print(f"Packets: Sent = {sent}, Received = {received}, Lost = {lost} ({(lost / sent) * 100:.2f}% loss)")
        if received > 0:
            print(f"Approximate round trip times in milli-seconds:")
            print(f"    Minimum = {min_time:.2f} ms, Maximum = {max_time:.2f} ms, Average = {total_time:.2f} ms")



def main():
    parser = argparse.ArgumentParser(description="Simple Ping Sweep Tool")
    parser.add_argument("-i", "--input", nargs="+", help="List of IP addresses or DNS names to sweep")
    args = parser.parse_args()
    
    if args.input:
        targets = args.input
    else:
        parser.error("Please specify target(s) to sweep using the -i/--input option")

    start_ping_sweep(targets)
    

if __name__ == '__main__':
    main()