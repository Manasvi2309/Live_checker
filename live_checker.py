#!/usr/bin/env python3

import requests
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

def banner():
    print(r"""
 ██╗     ██╗██╗   ██╗███████╗     ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗ 
██║     ██║██║   ██║██╔════╝    ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗
██║     ██║██║   ██║█████╗      ██║     ███████║█████╗  ██║     █████╔╝ █████╗  ██████╔╝
██║     ██║╚██╗ ██╔╝██╔══╝      ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██╔══╝  ██╔══██╗
███████╗██║ ╚████╔╝ ███████╗    ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗███████╗██║  ██║
╚══════╝╚═╝  ╚═══╝  ╚══════╝     ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝

            Live Subdomain Checker 🚀
""")

def check_subdomain(sub, timeout):
    for proto in ["http://", "https://"]:
        url = proto + sub.strip()
        try:
            r = requests.get(url, timeout=timeout)
            return f"{url} [{r.status_code}]"
        except requests.RequestException:
            continue
    return None

def main():
    banner()

    parser = argparse.ArgumentParser(description="Live Subdomain Checker")
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("-t", "--threads", type=int, default=50)
    parser.add_argument("--timeout", type=int, default=3)

    args = parser.parse_args()

    with open(args.input, "r") as f:
        subs = f.read().splitlines()

    total = len(subs)
    print(f"[+] Checking {total} subdomains with {args.threads} threads...\n")

    live = []
    checked = 0

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = {executor.submit(check_subdomain, sub, args.timeout): sub for sub in subs}

        for future in as_completed(futures):
            checked += 1
            percent = (checked / total) * 100

            print(f"\r[Progress] {checked}/{total} ({percent:.2f}%)", end="")

            result = future.result()
            if result:
                print(f"\n[LIVE] {result}")
                live.append(result)

    print("\n\n[+] Saving results...")

    with open(args.output, "w") as f:
        for i in live:
            f.write(i + "\n")

    print(f"[+] Done! Live subdomains saved in {args.output}")

if __name__ == "__main__":
    main()
