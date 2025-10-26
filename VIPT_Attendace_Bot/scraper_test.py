import time
from datetime import datetime

class EcapScraper:
    def __init__(self):
        print("🔧 ECAP Scraper initialized (Test Mode)")
    
    def login(self, username, password):
        """Simulate login to ECAP portal"""
        print(f"🔐 Login attempt: {username}")
        time.sleep(1)
        
        if len(username) < 8 or len(password) < 4:
            print("❌ Login failed - Invalid credentials")
            return False
        
        print("✅ Login successful")
        return True
    
    def get_attendance(self, roll_number):
        """
        Fetch attendance data from:
        1. Academic Register (current day register + subject attendance)
        2. Attendance page (overall attendance)
        """
        print(f"📊 Fetching attendance for {roll_number}...")
        time.sleep(1)
        
        # TEST DATA based on your ECAP portal structure
        attendance_data = {
            'roll_number': roll_number,
            'total_present': 329,
            'total_classes': 347,
            'overall_percentage': 94.81,
            'skip_hours': 69,
            
            # Current day register (from Academic Register page)
            'today_attendance': {
                'MC-II (OV)': 'P',
                'IP-I (PJK)': 'P',
                'PCOL-II GV': 'P'
            },
            
            # Subject-wise attendance (from Attendance page after clicking Show)
            'subjects': [
                {'name': 'MC-II (OV)', 'present': 14, 'total': 14, 'percentage': 100.00},
                {'name': 'IP-I (PJK)', 'present': 18, 'total': 20, 'percentage': 90.00},
                {'name': 'PCOL-II GV', 'present': 19, 'total': 19, 'percentage': 100.00},
                {'name': 'PCOG DKD', 'present': 26, 'total': 31, 'percentage': 83.87},
                {'name': 'PJ (KBR)', 'present': 20, 'total': 22, 'percentage': 90.91},
                {'name': 'IP-I L', 'present': 44, 'total': 44, 'percentage': 100.00},
                {'name': 'PCOL-II L', 'present': 28, 'total': 28, 'percentage': 100.00},
                {'name': 'PCOP-II L', 'present': 40, 'total': 40, 'percentage': 100.00},
                {'name': 'MC-II (PM)', 'present': 23, 'total': 25, 'percentage': 92.00},
                {'name': 'IP-I (PHN)', 'present': 25, 'total': 25, 'percentage': 100.00},
                {'name': 'PCOL SK', 'present': 21, 'total': 25, 'percentage': 84.00},
                {'name': 'PCOG DAK', 'present': 23, 'total': 23, 'percentage': 100.00},
                {'name': 'PJ (RM)', 'present': 28, 'total': 31, 'percentage': 90.32},
            ],
            
            'last_updated': datetime.now().strftime('%d/%m/%Y, %I:%M:%S %p')
        }
        
        return attendance_data
    
    def format_attendance_message(self, attendance_data):
        """Format attendance data in your exact requested format"""
        
        if 'error' in attendance_data:
            return f"❌ Error: {attendance_data['error']}"
        
        # Build message exactly as you requested
        message = f"Hi, Roll Number: {attendance_data['roll_number']}\n"
        message += f"Total: {attendance_data['total_present']}/{attendance_data['total_classes']} "
        message += f"({attendance_data['overall_percentage']:.2f}%)\n\n"
        
        # Skip hours calculation
        skip_hours = attendance_data['skip_hours']
        if skip_hours > 0:
            message += f"You can skip {skip_hours} hours and still maintain above 75%.\n\n"
        else:
            message += "⚠️ Your attendance is below 75%! Attend all classes.\n\n"
        
        # Today's Attendance (from Academic Register - Current Day)
        if attendance_data['today_attendance']:
            message += "Today's Attendance:\n"
            for subject, status in attendance_data['today_attendance'].items():
                message += f"{subject}: {status}\n"
            message += "\n"
        
        # Subject-wise Attendance (from Attendance page)
        message += "Subject-wise Attendance:\n"
        for subject in attendance_data['subjects']:
            message += f"{subject['name']}: {subject['present']}/{subject['total']} "
            message += f"({subject['percentage']:.2f}%)\n"
        
        message += f"\nLast Updated: {attendance_data['last_updated']}"
        
        return message

# Create instance for use in bot
scraper = EcapScraper()
