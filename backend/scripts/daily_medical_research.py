#!/usr/bin/env python3
"""
Script to run daily medical research task
This can be scheduled with cron or systemd timer

Usage:
    # With virtual environment (recommended):
    cd /root/personal_page && source venv/bin/activate && python backend/scripts/daily_medical_research.py
    
    # Or if venv is activated:
    python backend/scripts/daily_medical_research.py
    
Or add to crontab for daily execution at 9 AM:
    0 9 * * * cd /root/personal_page && source venv/bin/activate && python backend/scripts/daily_medical_research.py >> /var/log/medical_research.log 2>&1
"""

import sys
import os
from datetime import datetime
from pathlib import Path

# Add parent directory to path to import backend modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("❌ Error: 'python-dotenv' module not found. Please install dependencies:")
    print("   cd /root/personal_page/backend && pip install -r requirements.txt")
    sys.exit(1)

try:
    from backend.services.medical_research_service import medical_research_service
except ImportError as e:
    print(f"❌ Error importing medical_research_service: {e}")
    print("\nPlease ensure all dependencies are installed:")
    print("   cd /root/personal_page/backend && pip install -r requirements.txt")
    sys.exit(1)

def main():
    """Main function to run daily medical research"""
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"\n{'='*60}")
    print(f"🩺 Daily Medical Research - {current_time}")
    print(f"{'='*60}\n")
    
    result = medical_research_service.run_daily_research()
    
    if result["status"] == "success":
        print(f"\n✅ Successfully created blog post: {result['markdown_file']}")
        if result.get("image_file"):
            print(f"✅ Image saved: {result['image_file']}")
        return 0
    else:
        print(f"\n❌ Error: {result.get('error', 'Unknown error')}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
