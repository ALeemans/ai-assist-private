"""
Get details of a specific work item by ID.
"""

import requests
import yaml
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
import sys
import json

def load_config():
    """Load configuration from config.yaml"""
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)

def get_work_item(config, work_item_id):
    """Get specific work item details."""
    
    # Set up authentication
    credential = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(
        credential, 
        "499b84ac-1321-427f-aa17-267ca6975798/.default"
    )
    token = token_provider()
    
    organization = config['devops']['organization']
    project = config['devops']['project']
    api_version = config['devops']['api_version']
    
    # Get work item details
    url = f"{organization}/{project}/_apis/wit/workitems/{work_item_id}?api-version={api_version}"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Error getting work item: {response.status_code}")
        print(response.text)
        return None
    
    return response.json()

def display_work_item(item):
    """Display work item details."""
    if not item:
        print("No work item found.")
        return
    
    fields = item.get('fields', {})
    
    print(f"\n{'='*60}")
    print(f"Work Item #{item['id']}")
    print(f"{'='*60}")
    print(f"Type: {fields.get('System.WorkItemType', 'Unknown')}")
    print(f"Title: {fields.get('System.Title', 'No Title')}")
    print(f"State: {fields.get('System.State', 'Unknown')}")
    print(f"Assigned To: {fields.get('System.AssignedTo', {}).get('displayName', 'Unassigned')}")
    print(f"Assigned To (unique): {fields.get('System.AssignedTo', {}).get('uniqueName', 'N/A')}")
    print(f"Tags: {fields.get('System.Tags', 'None')}")
    print(f"\nDescription:")
    print(fields.get('System.Description', 'No description'))
    print(f"\n{'='*60}")
    
    # Print full assigned to structure
    print("\nFull AssignedTo structure:")
    print(json.dumps(fields.get('System.AssignedTo', {}), indent=2))

def main():
    """Main entry point."""
    
    if len(sys.argv) < 2:
        print("Usage: python get_work_item.py <work_item_id>")
        sys.exit(1)
    
    work_item_id = sys.argv[1]
    
    config = load_config()
    item = get_work_item(config, work_item_id)
    display_work_item(item)

if __name__ == "__main__":
    main()
