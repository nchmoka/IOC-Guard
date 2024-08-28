from ioc_guard.ioc_checker.abusech import check_abusech
from ioc_guard.ioc_checker.virustotal import check_virustotal

def process_iocs(iocs, ioc_type):
    report_data = []
    
    for ioc in iocs:
        # Call the correct function based on IoC type
        abuse_ch_data = check_abusech(ioc, ioc_type)
        virus_total_data = check_virustotal(ioc, ioc_type)

        # Combine data from both sources
        combined_data = {
            "ioc": ioc,
            "ioc_type": ioc_type,
            "abuse_ch": abuse_ch_data,
            "virus_total": virus_total_data
        }
        report_data.append(combined_data)
    
    return report_data
