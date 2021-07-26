import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import pandas as pd
total_urls_visited = 0

def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_website_links(url,internal_urls,external_urls):
    urls = []
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            continue
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
          continue
        if href in internal_urls:
            continue
        if domain_name not in href:
            if href not in external_urls:
                external_urls.append(href)
            continue
        urls.append(href)       
        internal_urls.append(href)
    return urls


def crawl(url, internal_urls, external_urls, max_urls):
    global total_urls_visited
    total_urls_visited += 1
    links = get_all_website_links(url,internal_urls,external_urls)
    for link in links:
        if total_urls_visited > max_urls:
            urls_ = list(set(internal_urls+external_urls))
            df = pd.DataFrame({"Urls":urls_})
            text = [x.split("/")[-1] for x in urls_]
            text = [x.replace("-"," ") for x in text]
            df["Text"] = text
            df.to_csv("train.csv",index=False)
            break
        crawl(link, internal_urls, external_urls, max_urls=max_urls)

if __name__ == '__main__':
    internal_urls = []
    external_urls = []
    crawl("https://www.bajajfinserv.in/", internal_urls, external_urls, max_urls=100)