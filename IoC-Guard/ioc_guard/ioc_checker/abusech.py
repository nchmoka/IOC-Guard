import requests

def check_abusech(ioc, ioc_type='ip'):
    # ThreatFox API endpoint
    url = "https://threatfox-api.abuse.ch/api/v1/"
    headers = {
        'Content-Type': 'application/json'
    }

    if ioc_type in ['ip', 'domain']:
        # Payload for IP or Domain IoC search
        payload = {
            "query": "search_ioc",
            "search_term": ioc
        }
    elif ioc_type == 'hash':
        # Payload for File Hash IoC search
        payload = {
            "query": "search_hash",
            "hash": ioc
        }
    else:
        return {"ioc": ioc, "abuse_ch_status": "Unsupported IoC type"}

    # Make the POST request to the ThreatFox API
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("query_status") == "ok" and data.get("data"):
            abuse_data_list = data["data"]
            processed_data = []
            for abuse_data in abuse_data_list:
                processed_data.append({
                    "ioc": abuse_data.get("ioc"),
                    "threat_type": abuse_data.get("threat_type"),
                    "threat_type_desc": abuse_data.get("threat_type_desc"),
                    "ioc_type": abuse_data.get("ioc_type"),
                    "ioc_type_desc": abuse_data.get("ioc_type_desc"),
                    "malware": abuse_data.get("malware"),
                    "malware_alias": abuse_data.get("malware_alias"),
                    "malware_malpedia": abuse_data.get("malware_malpedia"),
                    "confidence_level": abuse_data.get("confidence_level"),
                    "first_seen": abuse_data.get("first_seen"),
                    "last_seen": abuse_data.get("last_seen"),
                    "reporter": abuse_data.get("reporter"),
                    "tags": abuse_data.get("tags"),
                    "reference": abuse_data.get("reference"),
                })
            return processed_data
        else:
            return {"ioc": ioc, "abuse_ch_status": "No data found"}
    else:
        return {"ioc": ioc, "abuse_ch_status": f"Failed to retrieve data: {response.status_code}"}
