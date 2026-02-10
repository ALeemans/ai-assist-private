"""
Add comment to Azure DevOps work item
Usage: python add_comment.py <work_item_id> "Your comment text"
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

def add_comment(work_item_id, comment_text, organization, project, api_version, token):
    """Add a comment to a work item in Azure DevOps"""
    
    # Comments API requires -preview suffix
    url = f"{organization}/{project}/_apis/wit/workitems/{work_item_id}/comments?api-version={api_version}-preview"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "text": comment_text
    }
    
    print(f"📝 Adding comment to work item {work_item_id}...")
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200 or response.status_code == 201:
        print(f"✅ Comment added successfully!")
        print(f"   View: {organization}/{project}/_workitems/edit/{work_item_id}")
        return response.json()
    else:
        print(f"❌ Failed to add comment")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Add comment to Azure DevOps work item")
    parser.add_argument("work_item_id", type=int, help="Work item ID")
    parser.add_argument("comment", type=str, help="Comment text to add")
    
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
    
    # Add comment
    add_comment(args.work_item_id, args.comment, organization, project, api_version, token)

if __name__ == "__main__":
    main()
