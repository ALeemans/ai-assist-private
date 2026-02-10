"""
List user stories assigned to me in Azure DevOps.
Queries work items and displays them grouped by state.
"""

import requests
import yaml
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
import sys
import argparse

def load_config():
    """Load configuration from config.yaml"""
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)

def get_my_stories(config, state_filter=None):
    """Query Azure DevOps for user stories assigned to me."""
    
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
    assigned_to = config['defaults']['assigned_to']
    
    # Build WIQL query
    wiql_query = f"""
    SELECT [System.Id], [System.Title], [System.State], [System.WorkItemType], [System.AssignedTo], [System.Tags]
    FROM WorkItems
    WHERE [System.WorkItemType] IN ('User Story', 'Product Backlog Item')
        AND [System.AssignedTo] = '{assigned_to}'
    """
    
    if state_filter:
        wiql_query += f" AND [System.State] = '{state_filter}'"
    
    wiql_query += " ORDER BY [System.State] DESC, [System.ChangedDate] DESC"
    
    # Execute WIQL query
    wiql_url = f"{organization}/{project}/_apis/wit/wiql?api-version={api_version}"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    wiql_payload = {
        "query": wiql_query
    }
    
    response = requests.post(wiql_url, json=wiql_payload, headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Error querying work items: {response.status_code}")
        print(response.text)
        return []
    
    work_item_refs = response.json().get('workItems', [])
    
    if not work_item_refs:
        return []
    
    # Get full details for each work item
    work_item_ids = [str(item['id']) for item in work_item_refs]
    ids_param = ','.join(work_item_ids)
    
    details_url = f"{organization}/{project}/_apis/wit/workitems?ids={ids_param}&api-version={api_version}"
    
    details_response = requests.get(details_url, headers=headers)
    
    if details_response.status_code != 200:
        print(f"❌ Error getting work item details: {details_response.status_code}")
        return []
    
    work_items = details_response.json().get('value', [])
    
    return work_items

def display_stories(work_items):
    """Display work items grouped by state."""
    
    if not work_items:
        print("No user stories found.")
        return
    
    # Group by state
    by_state = {}
    for item in work_items:
        fields = item['fields']
        state = fields.get('System.State', 'Unknown')
        
        if state not in by_state:
            by_state[state] = []
        
        by_state[state].append({
            'id': item['id'],
            'title': fields.get('System.Title', 'No Title'),
            'tags': fields.get('System.Tags', ''),
            'url': item.get('url', '').replace('_apis/wit/workItems', '_workitems/edit')
        })
    
    # Display grouped results
    print(f"\n📊 Found {len(work_items)} user stories\n")
    
    for state, items in sorted(by_state.items()):
        print(f"\n{'='*60}")
        print(f"  {state.upper()} ({len(items)} items)")
        print(f"{'='*60}")
        
        for item in items:
            print(f"\n  🔹 [{item['id']}] {item['title']}")
            if item['tags']:
                print(f"     Tags: {item['tags']}")
            print(f"     {item['url']}")

def main():
    """Main entry point."""
    
    parser = argparse.ArgumentParser(description='List user stories assigned to me in Azure DevOps')
    parser.add_argument('--state', type=str, help='Filter by work item state (e.g., Doing, New, Te Refinen)')
    
    args = parser.parse_args()
    
    config = load_config()
    
    state_filter = args.state
    if state_filter:
        print(f"🔍 Filtering by state: {state_filter}")
    
    work_items = get_my_stories(config, state_filter)
    display_stories(work_items)

if __name__ == "__main__":
    main()
