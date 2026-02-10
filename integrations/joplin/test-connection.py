"""
Test connection to Joplin API
Verifies that the Web Clipper Service is running and accessible
"""
import requests
import yaml
import os
from pathlib import Path

def load_config():
    """Load Joplin API configuration"""
    config_path = Path(__file__).parent / "config.yaml"
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Read API token from environment variable if not set in config
    if not config.get('api_token'):
        config['api_token'] = os.environ.get('JOPLIN_API_TOKEN')
    
    return config

def test_connection(config):
    """Test connection to Joplin API"""
    api_url = config['api_url']
    api_token = config['api_token']
    
    print("🔌 Testing Joplin API Connection")
    print("=" * 50)
    print(f"API URL: {api_url}")
    print()
    
    # Test ping endpoint
    try:
        response = requests.get(f"{api_url}/ping")
        if response.status_code == 200 and response.text == "JoplinClipperServer":
            print("✅ Joplin Web Clipper Service is running")
        else:
            print("❌ Unexpected response from ping endpoint")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Joplin API")
        print("   Make sure Joplin is running and Web Clipper Service is enabled")
        return False
    
    # Test authentication by fetching notebooks
    try:
        response = requests.get(
            f"{api_url}/folders",
            params={'token': api_token}
        )
        
        if response.status_code == 200:
            print("✅ Authentication successful")
            notebooks = response.json()['items']
            print(f"\n📚 Found {len(notebooks)} notebook(s):")
            for nb in notebooks:
                print(f"   - {nb['title']}")
        elif response.status_code == 401:
            print("❌ Authentication failed")
            print("   Check your API token in config.yaml")
            return False
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error during authentication test: {e}")
        return False
    
    # Check for inbox notebook
    inbox_name = config['inbox_notebook']
    inbox_exists = any(nb['title'] == inbox_name for nb in notebooks)
    
    if inbox_exists:
        print(f"\n✅ Inbox notebook '{inbox_name}' found")
        
        # Get notes from inbox
        inbox_id = next(nb['id'] for nb in notebooks if nb['title'] == inbox_name)
        response = requests.get(
            f"{api_url}/notes",
            params={'token': api_token, 'folder_id': inbox_id}
        )
        
        if response.status_code == 200:
            notes = response.json()['items']
            print(f"   Contains {len(notes)} note(s)")
            if notes:
                print("   Latest notes:")
                for note in notes[:3]:  # Show first 3
                    print(f"      - {note['title']}")
    else:
        print(f"\n⚠️  Inbox notebook '{inbox_name}' not found")
        print(f"   Create it in Joplin or update config.yaml")
    
    print("\n✅ All tests passed!")
    return True

if __name__ == "__main__":
    config = load_config()
    
    if not config.get('api_token') or config['api_token'] == "YOUR_TOKEN_HERE":
        print("❌ Please configure your API token")
        print("   Option 1 (Recommended): Set environment variable JOPLIN_API_TOKEN")
        print("   Option 2: Set api_token in config.yaml")
        print()
        print("   Get token from: Joplin > Tools > Options > Web Clipper")
        exit(1)
    
    test_connection(config)
