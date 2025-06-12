import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env")
OPENCELLID_API_KEY = os.getenv("OPENCELLID_API_KEY")

# Cape Town coordinates - using city center area around CBD
# Cape Town CBD is roughly between -33.91 to -33.93 latitude and 18.41 to 18.43 longitude
test_bbox = {
    'south': -33.93,    # Southern boundary (more negative = further south)
    'west': 18.41,      # Western boundary  
    'north': -33.91,    # Northern boundary (less negative = further north)
    'east': 18.43       # Eastern boundary
}

# OpenCellID API endpoint for area queries
url = 'https://opencellid.org/cell/getInArea'

# API parameters
params = {
    'key': OPENCELLID_API_KEY,
    'BBOX': f"{test_bbox['south']},{test_bbox['west']},{test_bbox['north']},{test_bbox['east']}",
    'format': 'json',
    'limit': 100
}

print(f"Testing with Cape Town CBD coordinates: {params['BBOX']}")
print(f"Latitude range: {test_bbox['south']} to {test_bbox['north']}")
print(f"Longitude range: {test_bbox['west']} to {test_bbox['east']}")
print(f"Area covers approximately Cape Town city center")
print("-" * 50)

# Make the API request
try:
    response = requests.get(url, params=params, timeout=30)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print(f"Response length: {len(response.text)} characters")
        print(f"First 500 characters of response:")
        print(response.text[:500])
        
        # Try to parse as JSON for better formatting
        try:
            import json
            data = response.json()
            if isinstance(data, dict) and 'cells' in data:
                print(f"\nFound {len(data['cells'])} cell towers in Cape Town CBD area")
                if data['cells']:
                    print(f"Sample cell tower data:")
                    print(json.dumps(data['cells'][0], indent=2))
            elif isinstance(data, list):
                print(f"\nFound {len(data)} cell towers in Cape Town CBD area")
                if data:
                    print(f"Sample cell tower data:")
                    print(json.dumps(data[0], indent=2))
            else:
                print(f"\nUnexpected response format: {type(data)}")
                print(data)
        except json.JSONDecodeError:
            print("\nResponse is not valid JSON")
            
    elif response.status_code == 401:
        print("❌ Authentication failed - check your API key")
    elif response.status_code == 429:
        print("⏳ Rate limit exceeded - try again later")
    else:
        print(f"❌ Error: HTTP {response.status_code}")
        print(f"Response: {response.text}")
        
except requests.exceptions.Timeout:
    print("❌ Request timed out")
except requests.exceptions.ConnectionError:
    print("❌ Connection error - check your internet connection")
except Exception as e:
    print(f"❌ Unexpected error: {e}")

print("\n" + "="*50)
print("Cape Town Test Complete")
print("="*50)
