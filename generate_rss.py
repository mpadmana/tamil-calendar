import datetime
from email.utils import formatdate
import xml.etree.ElementTree as ET

# 1. Configuration & Constants
FEED_TITLE = "Daily Tamil Calendar Feed"
FEED_LINK = "https://github.io"
FEED_DESC = "Automatically generated daily Tamil month, date, and year"

TAMIL_MONTHS = [
    "Margazhi", "Thai", "Maasi", "Panguni", "Chithirai", "Vaikasi", 
    "Aani", "Aadi", "Aavani", "Purattasi", "Aippasi", "Karthigai"
]

TAMIL_YEARS = [
    "Prabhava", "Vibhava", "Shukla", "Pramodoota", "Prajopathi", "Angirasa", "Srimukha", "Bhava", "Yuva", "Dhatri",
    "Eeswara", "Bahudhanya", "Pramathi", "Vikrama", "Vishu", "Chitrabanu", "Subhanu", "Tharana", "Parthiba", "Viya",
    "Sarvajith", "Sarvadhari", "Virodhi", "Vikruthi", "Khara", "Nandhana", "Vijaya", "Jaya", "Manmadha", "Dhunmuki",
    "Hevilambi", "Vilambi", "Vikari", "Sarvari", "Plava", "Subhakrithi", "Sobhakrithi", "Krodhi", "Visvavasu", "Paridhaabi",
    "Pramadhicha", "Anandhanda", "Rakshasa", "Nala", "Pingala", "Kalayukthi", "Siddharthi", "Raudhri", "Dunmathi", "Dhundubhi",
    "Rudhirodhgari", "Raktakshi", "Krodhana", "Akshaya"
]

# Approximate Gregorian start days for each Tamil month (Indexed 1 to 12)
MONTH_TRANSITIONS = {
    1: 14,  # Thai starts Jan 14
    2: 13,  # Maasi starts Feb 13
    3: 14,  # Panguni starts Mar 14
    4: 14,  # Chithirai starts Apr 14 (New Year)
    5: 14,  # Vaikasi starts May 14
    6: 15,  # Aani starts Jun 15
    7: 16,  # Aadi starts Jul 16
    8: 16,  # Aavani starts Aug 16
    9: 17,  # Purattasi starts Sep 17
    10: 17, # Aippasi starts Oct 17
    11: 16, # Karthigai starts Nov 16
    12: 16  # Margazhi starts Dec 16
}

def calculate_tamil_date(today):
    g_year, g_month, g_day = today.year, today.month, today.day
    
    # Calculate Tamil Year (New Year starts mid-April)
    cycle_year = g_year - 1987  # 1987 was Prabhava (Index 0)
    if g_month < 4 or (g_month == 4 and g_day < 14):
        cycle_year -= 1
    tamil_year_name = TAMIL_YEARS[cycle_year % 60]
    
    # Determine active Tamil Month and Date Day
    transition_day = MONTH_TRANSITIONS[g_month]
    
    if g_day >= transition_day:
        tamil_month_idx = g_month  # Maps nicely to list indices because of list rotation
        tamil_day = (g_day - transition_day) + 1
    else:
        tamil_month_idx = g_month - 1 if g_month > 1 else 12
        prev_month_days = (today - datetime.timedelta(days=g_day)).day
        prev_transition = MONTH_TRANSITIONS[g_month - 1 if g_month > 1 else 12]
        tamil_day = (prev_month_days - prev_transition + 1) + g_day
        
    return TAMIL_MONTHS[tamil_month_idx % 12], tamil_day, tamil_year_name

# 2. Main Logic Execution
today = datetime.datetime.now()
t_month, t_day, t_year = calculate_tamil_date(today)

item_title = f"{t_month} {t_day}, {t_year} Varudam"
item_desc = f"Today is day {t_day} of the solar month {t_month} in the Tamil year {t_year}."
pub_date = formatdate(tuple_time=None, usegmt=True)

# 3. Build RSS XML Structure
rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")

ET.SubElement(channel, "title").text = FEED_TITLE
ET.SubElement(channel, "link").text = FEED_LINK
ET.SubElement(channel, "description").text = FEED_DESC

item = ET.SubElement(channel, "item")
ET.SubElement(item, "title").text = item_title
ET.SubElement(item, "description").text = item_desc
ET.SubElement(item, "pubDate").text = pub_date
ET.SubElement(item, "guid", isPermaLink="false").text = today.strftime("%Y-%m-%d-tamil-date")

# Save file locally
tree = ET.ElementTree(rss)
ET.indent(tree, space="  ", level=0)
tree.write("rss.xml", encoding="utf-8", xml_declaration=True)
print(f"Generated entry: {item_title}")
