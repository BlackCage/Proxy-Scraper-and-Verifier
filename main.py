import re
import concurrent.futures
from scrapeProxies import ProxyScraper
from proxy_information import ProxyInformation

# Create an instance of the ProxyInformation class to check proxies
checker = ProxyInformation(timeout=2)

def write_proxy_to_file(proxy_info):
    """
    Write a proxy and its protocol to a corresponding file.

    Args:
        proxy_info (dict): Dictionary containing proxy and protocol information.
    """
    proxy = proxy_info["proxy"]
    protocol = proxy_info["protocol"]
    
    with open(f"./Proxies/{protocol}.txt", "a") as file:
        file.write(proxy + "\n")

def check_proxy_and_write(proxy):
    """
    Check a proxy using the ProxyInformation class and write it to a file if valid.

    Args:
        proxy (str): Proxy in the format "ip:port".
    """
    result = checker.check_proxy(proxy)
    if result["status"]:
        proxy_type = result['info']['protocol']
        write_proxy_to_file({"proxy": proxy, "protocol": proxy_type})

def main():
    # Use the ProxyScraper to scrape and clean proxies
    scraper = ProxyScraper()
    scraper.run_scraper()

    with open("./Proxies/Not_Processed/proxies.txt", "r", encoding="utf-8") as file:
        # Read the list of proxies from the file and remove leading/trailing whitespace
        proxies = [line.strip() for line in file]

    num_workers = 100

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        # Map the check_proxy_and_write function using the list of proxies
        executor.map(check_proxy_and_write, proxies)

if __name__ == "__main__":
    main()
