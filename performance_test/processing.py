import multiprocessing
import requests
from multiprocessing import Pool

workers = multiprocessing.cpu_count()
print(workers)

def send_request(url):
    response = requests.get(url)
    print(f"Response from {url}: {response.status_code}")

if __name__ == "__main__":
    urls = ["http://localhost:8444/api"] * 10  # Replace with your actual URL
    with Pool(processes=10) as pool:
        pool.map(send_request, urls)