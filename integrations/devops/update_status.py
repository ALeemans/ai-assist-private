"""
Update Azure DevOps work item status
Usage: python update_status.py <work_item_id> <new_status>
"""
import requests
import argparse
import yaml
from pathlib import Path
from azure.identity import DefaultAzureCredential

def load_config():
    """Load configuration from config.yaml"""
    config_path = Path(__file__).parent / "config.yaml"
    if not config_path.exists():
        print("⚠️  config.yaml not found.")
        return None
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def update_work_item_status(work_item_id, new_status, organization, project, api_version, token):
    """Update work item status in Azure DevOps"""
    
    url = f"{organization}/{project}/_apis/wit/workitems/{work_item_id}?api-version={api_version}"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json-patch+json"
    }
    
    data = [
        {
            "op": "replace",
            "path": "/fields/System.State",
            "value": new_status
        }
    ]
    
    print(f"🔄 Updating work item {work_item_id} to status: {new_status}...")
    
    response = requests.patch(url, json=data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Status updated successfully!")
        print(f"   State: {result['fields']['System.State']}")
        print(f"   View: {organization}/{project}/_workitems/edit/{work_item_id}")
        return result
    else:
        print(f"❌ Failed to update status")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Update Azure DevOps work item status")
    parser.add_argument("work_item_id", type=int, help="Work item ID")
    parser.add_argument("status", type=str, help="New status (e.g., 'Done', 'Active', 'Closed')")
    
    args = parser.parse_args()
    
    # Load config
    config = load_config()
    if not config:
        print("❌ Configuration failed")
        return
    
    organization = config['devops']['organization']
    project = config['devops']['project']
    api_version = config['devops']['api_version']
    
    # Authenticate
    print("🔐 Authenticating with Azure DevOps...")
    credential = DefaultAzureCredential()
    token_obj = credential.get_token("499b84ac-1321-427f-aa17-267ca6975798/.default")
    token = token_obj.token
    print("✅ Authentication successful!\n")
    
    # Update status
    update_work_item_status(args.work_item_id, args.status, organization, project, api_version, token)

if __name__ == "__main__":
    main()
