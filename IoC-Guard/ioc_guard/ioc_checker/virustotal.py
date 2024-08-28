import requests
import os
from urllib.parse import quote_plus

def check_virustotal(ioc, ioc_type='domain'):
    api_key = os.getenv('VIRUSTOTAL_API_KEY')
    if not api_key:
        raise Exception("VirusTotal API key not found in environment variables.")
    
    # Determine the appropriate endpoint based on IoC type
    if ioc_type == 'domain':
        endpoint = f"https://www.virustotal.com/api/v3/domains/{quote_plus(ioc)}"
    elif ioc_type == 'ip':
        endpoint = f"https://www.virustotal.com/api/v3/ip_addresses/{ioc}"
    elif ioc_type == 'hash':
        endpoint = f"https://www.virustotal.com/api/v3/files/{ioc}"
    else:
        return {"ioc": ioc, "virus_total_status": "unsupported ioc_type"}

    headers = {"x-apikey": api_key}
    response = requests.get(endpoint, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if "data" in data:
            attributes = data["data"]["attributes"]
            last_analysis_stats = attributes.get("last_analysis_stats", {})
            last_analysis_results = attributes.get("last_analysis_results", {})
            whois_info = attributes.get("whois", "N/A")
            popularity_ranks = attributes.get("popularity_ranks", {})
            reputation = attributes.get("reputation", "N/A")
            last_https_certificate = attributes.get("last_https_certificate", {})
            categories = attributes.get("categories", {})
            total_votes = attributes.get("total_votes", {})

            # Initialize tag_counts dynamically based on categories found in last_analysis_results
            tag_counts = {}

            for engine, result in last_analysis_results.items():
                category = result.get("category")
                if category and category not in ["harmless", "undetected","type-unsupported"]:
                    if category not in tag_counts:
                        tag_counts[category] = 0
                    tag_counts[category] += 1

            # Generate tags based on findings
            tags = [key for key, count in tag_counts.items() if count >= 2]

            return {
                "ioc": ioc,
                "ioc_type": ioc_type,
                "last_analysis_stats": last_analysis_stats,
                "tags": tags,
                "whois_info": whois_info,
                "popularity_ranks": popularity_ranks,
                "reputation": reputation,
                "last_https_certificate": last_https_certificate,
                "categories": categories,
                "total_votes": total_votes,
                "virus_total_status": "found"
            }
        else:
            return {"ioc": ioc, "virus_total_status": "not found"}
    else:
        return {"ioc": ioc, "virus_total_status": f"Failed to retrieve data: {response.status_code}"}
