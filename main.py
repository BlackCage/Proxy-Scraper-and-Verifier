import re
import concurrent.futures
from scrapeProxies import ProxyScraper
from proxy_information import ProxyInformation

# Create an instance of the ProxyInformation class to check proxies
checker = ProxyInformation(timeout=2)

# Function to write a proxy to a file based on its type
def write_to_file(proxy, proxy_type):
    if proxy:
        # Verifica si la línea es un proxy IP:puerto válido antes de escribirla
        if re.match(r'\d+\.\d+\.\d+\.\d+:\d+', proxy):
            with open(f"./Proxies/{proxy_type}.txt", "a") as file:
                file.write(proxy + "\n")

# Function to check a group of proxies
def check_proxies(proxy_group):
    for proxy in proxy_group:
        result = checker.check_proxy(proxy)
        # Only write the proxy to a file if it's valid (result is not "False")
        if not "False" in str(result):
            proxy = f"{result['ip']}:{result['port']}"
            proxy_type = result['protocol']
            write_to_file(proxy, proxy_type)

def main():
    # Use the ProxyScraper to scrape and clean proxies
    scraper = ProxyScraper()
    scraper.run_scraper()
    
    with open("./Proxies/Not_Processed/proxies.txt", "r", encoding="utf-8") as file:
        # Read the list of proxies from the file and remove leading/trailing whitespace
        proxies = [line.strip() for line in file]

    num_workers = 200
    chunk_size = len(proxies) // num_workers

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = []
        for i in range(0, len(proxies), chunk_size):
            proxy_group = proxies[i:i + chunk_size]
            # Submit the check_proxies function for parallel execution
            future = executor.submit(check_proxies, proxy_group)
            futures.append(future)

        # Wait for all futures to complete
        concurrent.futures.wait(futures, return_when=concurrent.futures.ALL_COMPLETED)

if __name__ == "__main__":
    main()
