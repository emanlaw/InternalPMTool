from app import create_app

app = create_app()

if __name__ == '__main__':
    # Start notification scheduler after app is created
    with app.app_context():
        from app.services.notification_service import schedule_daily_notifications
        schedule_daily_notifications()
    
    app.run(debug=True)