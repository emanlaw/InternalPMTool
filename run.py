from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Skip notification service on Windows to avoid threading issues
    if os.name != 'nt':  # Only run on non-Windows systems
        try:
            with app.app_context():
                from app.services.notification_service import schedule_daily_notifications
                schedule_daily_notifications()
        except Exception as e:
            print(f"Warning: Could not start notification service: {e}")
    
    app.run(debug=True, host='127.0.0.1', port=5002)