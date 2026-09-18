import datetime
import xml.etree.ElementTree as ET

# 1. Constants
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

MONTH_TRANSITIONS = {
    1: 14, 2: 13, 3: 14, 4: 14, 5: 14, 6: 15, 7: 16, 8: 16, 9: 17, 10: 17, 11: 16, 12: 16
}

def calculate_tamil_date(today):
    g_year, g_month, g_day = today.year, today.month, today.day
    cycle_year = g_year - 1987
    if g_month < 4 or (g_month == 4 and g_day < 14):
        cycle_year -= 1
    tamil_year_name = TAMIL_YEARS[cycle_year % 60]
    
    transition_day = MONTH_TRANSITIONS[g_month]
    if g_day >= transition_day:
        tamil_month_idx = g_month
        tamil_day = (g_day - transition_day) + 1
    else:
        tamil_month_idx = g_month - 1 if g_month > 1 else 12
        prev_month_days = (today - datetime.timedelta(days=g_day)).day
        prev_transition = MONTH_TRANSITIONS[g_month - 1 if g_month > 1 else 12]
        tamil_day = (prev_month_days - prev_transition + 1) + g_day
        
    return TAMIL_MONTHS[tamil_month_idx % 12], tamil_day, tamil_year_name

# 2. Main Logic: Generate a 365-day loop
start_date = datetime.date.today()
ics_lines = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//My Tamil Calendar//EN",
    "X-WR-CALNAME:Tamil Daily Calendar"
]

for i in range(365):
    current_date = start_date + datetime.timedelta(days=i)
    t_month, t_day, t_year = calculate_tamil_date(current_date)
    
    # Format strings for calendar metadata
    date_str = current_date.strftime("%Y%m%d")
    next_date_str = (current_date + datetime.timedelta(days=1)).strftime("%Y%m%d")
    summary = f"{t_month} {t_day}\\, {t_year}"
    uid = f"{date_str}-tamil-date@yourgithub"
    
    # Append standalone all-day event parameters
    ics_lines.extend([
        "BEGIN:VEVENT",
        f"UID:{uid}",
        f"DTSTART;VALUE=DATE:{date_str}",
        f"DTEND;VALUE=DATE:{next_date_str}",
        f"SUMMARY:{summary}",
        f"DESCRIPTION:Tamil Solar Date - Month: {t_month}\\, Day: {t_day}\\, Year: {t_year} Varudam",
        "END:VEVENT"
    ])

ics_lines.append("END:VCALENDAR")

# Save file locally as .ics instead of xml
with open("calendar.ics", "w", encoding="utf-8") as f:
    f.write("\n".join(ics_lines))

print("Successfully compiled a 365-day outlook into calendar.ics!")
