import requests
from jinja2 import Template
import datetime

# WebEx and system monitoring API credentials
WEBEX_ACCESS_TOKEN = 'your_webex_access_token'
WEBEX_SPACE_ID = 'your_webex_space_id'
MONITORING_API_URL = 'https://api.yourmonitoringtool.com/v1/incidents'  # Replace with actual monitoring API URL
MONITORING_API_KEY = 'your_monitoring_api_key'

# Define the handover template using Jinja2
HANDOVER_TEMPLATE = """
### Shift {{ shift_from }} to {{ shift_to }} Handover

**Date:** {{ date }}  
**Time:** {{ time }}  

---

### Handover Summary

1. **Incidents and Alerts**  
   {% for incident in incidents %}
   - **Incident ID**: {{ incident['id'] }}
   - **Status**: {{ incident['status'] }}
   - **Description**: {{ incident['description'] }}
   - **Resolution**: {{ incident['resolution'] }}
   {% endfor %}

2. **System Health and Performance**  
   - **Uptime and Availability Metrics:** {{ system_health['uptime'] }}%
   - **Error Rates:** {{ system_health['error_rate'] }}%

3. **Scheduled Maintenance and Deployments**  
   - **Upcoming Maintenance:** {{ scheduled_maintenance }}
   - **Recent Deployments:** {{ recent_deployments }}

4. **Security and Compliance**  
   - **Security Incidents:** {{ security_notes }}

5. **Backup and Recovery**  
   - **Backup Status:** {{ backup_status }}
   - **DR Test Results:** {{ dr_test_results }}

---

**Prepared by:** Shift {{ shift_from }} Team  
"""

# Function to retrieve incidents from monitoring tool API
def fetch_incidents():
    headers = {"Authorization": f"Bearer {MONITORING_API_KEY}"}
    response = requests.get(MONITORING_API_URL, headers=headers)
    if response.status_code == 200:
        return response.json()  # Assuming the API returns a JSON list of incidents
    else:
        return [{"id": "N/A", "status": "No incidents", "description": "", "resolution": ""}]

# Sample data for demonstration (to be replaced with real data fetching functions)
def fetch_system_health():
    return {"uptime": 99.98, "error_rate": 0.01}

def fetch_maintenance_schedule():
    return "Scheduled database maintenance at 2 AM UTC."

def fetch_security_notes():
    return "No new security incidents."

def fetch_backup_status():
    return "All backups completed successfully."

def fetch_dr_test_results():
    return "DR test passed without issues."

def send_message_to_webex(content):
    headers = {
        "Authorization": f"Bearer {WEBEX_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    message_data = {
        "roomId": WEBEX_SPACE_ID,
        "markdown": content
    }
    response = requests.post("https://webexapis.com/v1/messages", headers=headers, json=message_data)
    if response.status_code == 200:
        print("Message sent successfully to WebEx!")
    else:
        print("Failed to send message:", response.status_code, response.text)

# Main function to compile handover data and send it to WebEx
def create_and_send_handover():
    # Fetch data for each section
    incidents = fetch_incidents()
    system_health = fetch_system_health()
    scheduled_maintenance = fetch_maintenance_schedule()
    recent_deployments = "No recent deployments."
    security_notes = fetch_security_notes()
    backup_status = fetch_backup_status()
    dr_test_results = fetch_dr_test_results()

    # Prepare template data
    handover_data = {
        "shift_from": "3",
        "shift_to": "1",
        "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.datetime.now().strftime("%H:%M %p"),
        "incidents": incidents,
        "system_health": system_health,
        "scheduled_maintenance": scheduled_maintenance,
        "recent_deployments": recent_deployments,
        "security_notes": security_notes,
        "backup_status": backup_status,
        "dr_test_results": dr_test_results,
    }

    # Render the handover template
    template = Template(HANDOVER_TEMPLATE)
    handover_content = template.render(handover_data)

    # Send handover to WebEx
    send_message_to_webex(handover_content)

# Run the function to create and send the handover
create_and_send_handover()
