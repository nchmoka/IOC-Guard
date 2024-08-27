import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

def generate_pdf(report_data, output_file):
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle('Title', parent=styles['Title'], fontSize=18, spaceAfter=20)
    header_style = ParagraphStyle('Heading1', parent=styles['Heading1'], fontSize=14, spaceAfter=14, textColor=colors.darkblue)
    subheader_style = ParagraphStyle('Heading2', parent=styles['Heading2'], fontSize=12, spaceAfter=10)
    normal_style = ParagraphStyle('Normal', parent=styles['Normal'], spaceAfter=6)

    # Report Title and Date
    title = Paragraph("IoC Detailed Threat Report", title_style)
    date_time = Paragraph(f"Report Generated On: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style)
    elements.append(title)
    elements.append(date_time)
    elements.append(Spacer(1, 12))


    # IoC Details Section
    for data in report_data:
        ioc_type = data.get("ioc_type", "Unknown")
        ioc_value = data.get("ioc", "N/A")
        elements.append(Paragraph(f"IoC Type: {ioc_type}", header_style))
        elements.append(Paragraph(f"IoC Value: {ioc_value}", subheader_style))

        # Threat Intelligence Data (Abuse.ch)
        abuse_info = data.get("abuse_ch", {})
        if isinstance(abuse_info, list):
            for entry in abuse_info:
                elements.append(Paragraph(f"Abuse.ch Information:", subheader_style))
                elements.append(Paragraph(f"- Threat Type: {entry.get('threat_type', 'N/A')}", normal_style))
                elements.append(Paragraph(f"- Threat Description: {entry.get('threat_type_desc', 'N/A')}", normal_style))
                elements.append(Paragraph(f"- Malware: {entry.get('malware', 'N/A')} ({entry.get('malware_alias', 'N/A')})", normal_style))
                elements.append(Paragraph(f"- Confidence Level: {entry.get('confidence_level', 'N/A')}", normal_style))
                elements.append(Paragraph(f"- First Seen: {entry.get('first_seen', 'N/A')}", normal_style))
                elements.append(Paragraph(f"- Last Seen: {entry.get('last_seen', 'N/A')}", normal_style))
                elements.append(Paragraph(f"- Reporter: {entry.get('reporter', 'N/A')}", normal_style))
                elements.append(Spacer(1, 6))
        else:
            elements.append(Paragraph(f"Abuse.ch Information:", subheader_style))
            elements.append(Paragraph(f"- Threat Type: {abuse_info.get('threat_type', 'N/A')}", normal_style))
            elements.append(Paragraph(f"- Threat Description: {abuse_info.get('threat_type_desc', 'N/A')}", normal_style))
            elements.append(Paragraph(f"- Malware: {abuse_info.get('malware', 'N/A')} ({abuse_info.get('malware_alias', 'N/A')})", normal_style))
            elements.append(Paragraph(f"- Confidence Level: {abuse_info.get('confidence_level', 'N/A')}", normal_style))
            elements.append(Paragraph(f"- First Seen: {abuse_info.get('first_seen', 'N/A')}", normal_style))
            elements.append(Paragraph(f"- Last Seen: {abuse_info.get('last_seen', 'N/A')}", normal_style))
            elements.append(Paragraph(f"- Reporter: {abuse_info.get('reporter', 'N/A')}", normal_style))
            elements.append(Spacer(1, 6))

        # VirusTotal Data
        vt_info = data.get("virus_total", {})
        elements.append(Paragraph(f"VirusTotal Information:", subheader_style))
        elements.append(Paragraph(f"- Last Analysis Stats: {str(vt_info.get('last_analysis_stats', 'N/A'))}", normal_style))
        if vt_info.get('tags'):
            elements.append(Paragraph(f"- Tags: {', '.join(vt_info.get('tags', []))}", normal_style))
        elements.append(Paragraph(f"- WHOIS Info: {vt_info.get('whois_info', 'N/A')}", normal_style))
        elements.append(Paragraph(f"- Popularity Ranks: {str(vt_info.get('popularity_ranks', 'N/A'))}", normal_style))
        elements.append(Paragraph(f"- Reputation: {str(vt_info.get('reputation', 'N/A'))}", normal_style))
        elements.append(Paragraph(f"- Last HTTPS Certificate: {str(vt_info.get('last_https_certificate', 'N/A'))}", normal_style))
        elements.append(Paragraph(f"- Last DNS Records: {str(vt_info.get('last_dns_records', 'N/A'))}", normal_style))
        elements.append(Spacer(1, 12))

    # Build the PDF
    doc.build(elements)
