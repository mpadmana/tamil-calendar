import datetime

# 1. Constants in Native Tamil Script
TAMIL_MONTHS = [
    "மார்கழி", "தை", "மாசி", "பங்குனி", "சித்திரை", "வைகாசி", 
    "ஆனி", "ஆடி", "ஆவணி", "புரட்டாசி", "ஐப்பசி", "கார்த்திகை"
]

TAMIL_YEARS = [
    "பிரபவ", "விபவ", "சுக்ல", "பிரமோதூத", "பிரஜோத்பத்தி", "ஆங்கீரச", "ஸ்ரீமுக", "பவ", "யுவ", "தாது",
    "ஈஸ்வர", "பஹுதான்ய", "பிரமாதி", "விக்ரம", "விஷு", "சித்ரபானு", "சுபானு", "தாரண", "பார்த்திப", "விய",
    "சர்வஜித்", "சர்வதாரி", "விரோதி", "விக்ருதி", "கர", "நந்தன", "விஜய", "ஜய", "மன்மத", "துன்முகி",
    "ஹேவிளம்பி", "விளம்பி", "விகாரி", "சார்வரி", "ப்லவ", "சுபகிருது", "சோபகிருது", "க்ரோதி", "விஸ்வாவசு", "பராபவ",
    "ப்லவங்க", "கீலக", "சௌம்ய", "சாதாரண", "விரோதகிருது", "பரிதாபி", "பிரமாதீச", "ஆனந்த", "ராட்சஸ", "நள",
    "பிங்கள", "காளயுக்தி", "சித்தார்த்தி", "ரௌத்திரி", "துன்மதி", "துந்துபி", "ருத்ரோத்காரி", "ரக்தாட்சி", "க்ரோதன", "அட்சய"
]

# Approximate Gregorian start days for each Tamil month (Indexed 1 to 12)
MONTH_TRANSITIONS = {
    1: 14, 2: 13, 3: 14, 4: 14, 5: 14, 6: 15, 7: 16, 8: 16, 9: 17, 10: 17, 11: 16, 12: 16
}

def calculate_tamil_date(today):
    g_year, g_month, g_day = today.year, today.month, today.day
    
    # Calculate Tamil Year Index (1987 was Prabhava / பிரபவ)
    cycle_year = g_year - 1987
    if g_month < 4 or (g_month == 4 and g_day < 14):
        cycle_year -= 1
    tamil_year_name = TAMIL_YEARS[cycle_year % 60]
    
    # Determine active Tamil Month and Date Day
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
    "X-WR-CALNAME:தமிழ் நாட்காட்டி"  # Name of the calendar inside Google Calendar
]

for i in range(365):
    current_date = start_date + datetime.timedelta(days=i)
    t_month, t_day, t_year = calculate_tamil_date(current_date)
    
    # Format strings for calendar entries
    date_str = current_date.strftime("%Y%m%d")
    next_date_str = (current_date + datetime.timedelta(days=1)).strftime("%Y%m%d")
    
    # Title format: "புரட்டாசி 3, க்ரோதி வருடம்"
    summary = f"{t_month} {t_day}\\, {t_year} வருடம்"
    uid = f"{date_str}-tamil-date@yourgithub"
    
    # Add standalone all-day event
    ics_lines.extend([
        "BEGIN:VEVENT",
        f"UID:{uid}",
        f"DTSTART;VALUE=DATE:{date_str}",
        f"DTEND;VALUE=DATE:{next_date_str}",
        f"SUMMARY:{summary}",
        f"DESCRIPTION:தமிழ் சூரிய நாட்காட்டி - மாதம்: {t_month}\\, தேதி: {t_day}\\, வருடம்: {t_year} வருடம்",
        "END:VEVENT"
    ])

ics_lines.append("END:VCALENDAR")

# Save file locally as .ics with UTF-8 encoding for Tamil letters
with open("calendar.ics", "w", encoding="utf-8") as f:
    f.write("\n".join(ics_lines))

print("Successfully compiled a 365-day outlook into calendar.ics in Tamil!")
