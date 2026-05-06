import urllib.request
import urllib.parse
from urllib.error import HTTPError, URLError

def test_rate_limiting():
    print("\n--- Testing Rate Limiting (Excessive API requests) ---")
    url = "http://127.0.0.1:8000/api/login/"
    data = urllib.parse.urlencode({"username": "wrong", "password": "wrong"}).encode("utf-8")
    
    print("Sending 6 login requests (Limit is 5 per minute)...")
    for i in range(1, 7):
        try:
            req = urllib.request.Request(url, data=data)
            with urllib.request.urlopen(req) as response:
                print(f"Request {i}: Status Code: {response.getcode()} - {response.read().decode('utf-8')}")
        except HTTPError as e:
            if e.code == 403: 
                print(f"Request {i}: Blocked by Rate Limiting! Status Code: {e.code}")
            elif e.code == 401:
                print(f"Request {i}: Failed Login (Expected). Status Code: {e.code}")
            else:
                print(f"Request {i}: Status Code: {e.code}")
        except URLError as e:
            print("Server is not running. Please start the Django development server first.")
            break

if __name__ == "__main__":
    test_rate_limiting()
