import os
import re
import requests
import concurrent.futures

class ProxyScraper:
    def __init__(self):
        self.output_file = "./Proxies/Not_Processed/proxies.txt"
        self.urls_and_parsers = [
            ("https://www.proxy-list.download/api/v1/get?type=http", self._parse_proxies),
            ("https://www.proxy-list.download/api/v1/get?type=https", self._parse_proxies),
            ("https://www.proxy-list.download/api/v1/get?type=socks4", self._parse_proxies),
            ("https://www.proxy-list.download/api/v1/get?type=socks5", self._parse_proxies),

            ("https://www.sslproxies.org/", self._parse_sslproxies),

            ("https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt", self._parse_proxies),
            ("https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt", self._parse_proxies),
            ("https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt", self._parse_proxies),
            ("https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt", self._parse_proxies),
            ("https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt", self._parse_proxies),
            ("https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt", self._parse_proxies),
            ("https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.txt", self._parse_proxies),
            ("https://raw.githubusercontent.com/zloi-user/hideip.me/main/http.txt", self._parse_proxies),
            ("https://raw.githubusercontent.com/zloi-user/hideip.me/main/https.txt", self._parse_proxies),
            ("https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks4.txt", self._parse_proxies),
            ("https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks5.txt", self._parse_proxies),
            ("https://raw.githubusercontent.com/casals-ar/proxy-list/main/http", self._parse_proxies),
            ("https://raw.githubusercontent.com/casals-ar/proxy-list/main/https", self._parse_proxies),
            ("https://raw.githubusercontent.com/casals-ar/proxy-list/main/socks4", self._parse_proxies),
            ("https://raw.githubusercontent.com/casals-ar/proxy-list/main/socks5", self._parse_proxies),
            ("https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt", self._parse_proxies),
            ("https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt", self._parse_proxies),
            ("https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/https.txt", self._parse_proxies),
            ("https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks4.txt", self._parse_proxies),
            ("https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks5.txt", self._parse_proxies),

            ("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=https&timeout=10000&country=all&ssl=true&anonymity=all", self._parse_proxies),
            ("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=true&anonymity=all", self._parse_proxies),
            ("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=10000&country=all&ssl=true&anonymity=all", self._parse_proxies),
            ("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=10000&country=all&ssl=true&anonymity=all", self._parse_proxies)
        ]

    def _clean_proxies_file(self, file_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()

        cleaned_lines = []
        for line in lines:
            line = line.strip()
            if ':' in line:
                parts = line.split(':')
                if len(parts) >= 2:
                    line = ':'.join(parts[:2])
            cleaned_lines.append(line)

        unique_lines = list(set(cleaned_lines))
        clean_lines = [line for line in unique_lines if line]

        with open(file_path, 'w') as f:
            f.writelines("\n".join(clean_lines))

    def _write(self, proxies):
        if not "proxies.txt" in os.listdir("./Proxies/Not_Processed/"):
            open(self.output_file, "w").close()
        with open(self.output_file, "a") as f:
            f.write(f"{proxies}\n")

    def _scrape_and_write_proxies(self, url, parser):
        print(f"Scraping Proxies from {url} ...")
        try:
            r = requests.get(url)
            r.raise_for_status()
            proxies = parser(r.text)
            self._write(proxies)
        except requests.RequestException as e:
            print(f"Error while scraping {url}: {e}")
    
    def _parse_proxies(self, text):
        text = text.strip()
        if '://' in text:
            matches = [line.split(':')[0] for line in text.split()]
            text = '\n'.join(matches)

        return text

    def _parse_sslproxies(self, text):
        return text.split("UTC.\n")[1].split("</")[0].rstrip().lstrip()

    def run_scraper(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self._scrape_and_write_proxies, url, parser) for url, parser in self.urls_and_parsers]

        concurrent.futures.wait(futures)
        self._clean_proxies_file(self.output_file)
