# testing which is faster, pycurl or requests


import time
import pycurl
import requests
from statistics import mean
from io import BytesIO


def pycurl_request(url, data):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.POST, 1)
    c.setopt(c.POSTFIELDS, data)
    c.setopt(c.HTTPHEADER, ["Content-Type: application/json"])

    start_time = time.time()
    c.perform()
    end_time = time.time()

    c.close()
    return end_time - start_time


def requests_request(url, data):
    start_time = time.time()
    requests.post(url, data=data, headers={"Content-Type": "application/json"})
    end_time = time.time()
    return end_time - start_time


def requests_session_request(session, url, data):
    start_time = time.time()
    session.post(url, data=data, headers={"Content-Type": "application/json"})
    end_time = time.time()
    return end_time - start_time


def run_benchmark(num_requests):
    url = "http://localhost:11434/api/generate"  # Adjust this URL to your Ollama server
    data = '{"model": "mistral:latest", "prompt": "Hello, world!"}'  # Adjust model and prompt as needed

    pycurl_times = []
    requests_times = []
    requests_session_times = []

    # Create a session for requests with session

    print("pyCurl")
    for _ in range(num_requests):
        pycurl_times.append(pycurl_request(url, data))
        # requests_times.append(requests_request(url, data))
        # requests_session_times.append(requests_session_request(session, url, data))

    print("requests")
    for _ in range(num_requests):
        # pycurl_times.append(pycurl_request(url, data))
        requests_times.append(requests_request(url, data))
        # requests_session_times.append(requests_session_request(session, url, data))

    session = requests.Session()
    print("requests with session")
    for _ in range(num_requests):
        # pycurl_times.append(pycurl_request(url, data))
        # requests_times.append(requests_request(url, data))
        requests_session_times.append(requests_session_request(session, url, data))

    # Close the session
    session.close()

    return pycurl_times, requests_times, requests_session_times


def main():
    num_requests = 10  # Adjust this number as needed

    print(f"Running benchmark with {num_requests} requests...")
    pycurl_times, requests_times, requests_session_times = run_benchmark(num_requests)

    print(pycurl_times)

    print(requests_times)

    print(requests_session_times)

    avg_pycurl_time = mean(pycurl_times)
    avg_requests_time = mean(requests_times)
    avg_requests_session_time = mean(requests_session_times)

    print(f"\nResults:")
    print(f"Average pyCurl time: {avg_pycurl_time:.4f} seconds")
    print(f"Average requests time: {avg_requests_time:.4f} seconds")
    print(
        f"Average requests with session time: {avg_requests_session_time:.4f} seconds"
    )

    # Determine the fastest method
    if (
        avg_pycurl_time < avg_requests_time
        and avg_pycurl_time < avg_requests_session_time
    ):
        faster = "pyCurl"
        difference = min(avg_requests_time, avg_requests_session_time) - avg_pycurl_time
    elif (
        avg_requests_time < avg_pycurl_time
        and avg_requests_time < avg_requests_session_time
    ):
        faster = "requests"
        difference = min(avg_pycurl_time, avg_requests_session_time) - avg_requests_time
    else:
        faster = "requests with session"
        difference = min(avg_pycurl_time, avg_requests_time) - avg_requests_session_time

    percentage = (
        difference / max(avg_pycurl_time, avg_requests_time, avg_requests_session_time)
    ) * 100

    print(f"\n{faster} is faster by {difference:.4f} seconds ({percentage:.2f}%)")


if __name__ == "__main__":
    main()
