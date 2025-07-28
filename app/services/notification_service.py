from flask import current_app
from flask_mail import Message
from datetime import datetime, date
import threading
from app.models.user import load_data

def send_overdue_notifications():
    """Send email notifications for overdue cards"""
    try:
        data = load_data()
        today = date.today()
        
        # Find overdue cards
        overdue_cards = []
        for card in data['cards']:
            if card.get('due_date'):
                try:
                    due_date = datetime.strptime(card['due_date'], '%Y-%m-%d').date()
                    if due_date < today and card['status'] != 'done':
                        overdue_cards.append(card)
                except:
                    continue
        
        if not overdue_cards:
            return
        
        # Get users with email notifications enabled
        users_to_notify = []
        for user in data.get('users', []):
            if user.get('email_notifications', True):  # Default to True
                users_to_notify.append(user)
        
        # Send emails
        for user in users_to_notify:
            if user.get('email'):  # Only if user has email set
                send_overdue_email(user, overdue_cards)
                
    except Exception as e:
        print(f"Error sending notifications: {e}")

def send_overdue_email(user, overdue_cards):
    """Send overdue cards email to a specific user"""
    try:
        projects = {p['id']: p['name'] for p in load_data()['projects']}
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: #0079bf; color: white; padding: 20px; text-align: center;">
                <h1>🚨 Overdue Cards Alert</h1>
            </div>
            
            <div style="padding: 20px;">
                <p>Hello {user['username']},</p>
                <p>You have <strong>{len(overdue_cards)} overdue cards</strong> that need attention:</p>
                
                <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 20px 0;">
        """
        
        for card in overdue_cards:
            project_name = projects.get(card['project_id'], 'Unknown')
            html_body += f"""
                    <div style="border-left: 4px solid #ff5630; padding: 10px; margin: 10px 0; background: white;">
                        <h3 style="margin: 0 0 5px 0; color: #172b4d;">#{card['id']} - {card['title']}</h3>
                        <p style="margin: 5px 0; color: #5e6c84;">Project: {project_name}</p>
                        <p style="margin: 5px 0; color: #5e6c84;">Due: {card['due_date']} | Priority: {card['priority']} | Assignee: {card.get('assignee', 'Unassigned')}</p>
                        <p style="margin: 5px 0;">{card.get('description', '')}</p>
                    </div>
            """
        
        html_body += f"""
                </div>
                
                <p>Please review and update these cards as soon as possible.</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="http://localhost:5000/issues" 
                       style="background: #0079bf; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                        View All Issues
                    </a>
                </div>
                
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
                <p style="font-size: 12px; color: #5e6c84; text-align: center;">
                    This is an automated notification from PM Tool.<br>
                    Generated on {datetime.now().strftime('%Y-%m-%d at %H:%M')}
                </p>
            </div>
        </body>
        </html>
        """
        
        msg = Message(
            subject=f"PM Tool: {len(overdue_cards)} Overdue Cards Need Attention",
            recipients=[user['email']],
            html=html_body
        )
        
        current_app.extensions['mail'].send(msg)
        print(f"Overdue notification sent to {user['username']}")
        
    except Exception as e:
        print(f"Error sending email to {user['username']}: {e}")

def schedule_daily_notifications():
    """Schedule daily email notifications (runs in background)"""
    def run_notifications():
        import time
        while True:
            # Check time - send at 9 AM daily
            now = datetime.now()
            if now.hour == 9 and now.minute == 0:
                send_overdue_notifications()
                time.sleep(60)  # Wait 1 minute to avoid duplicate sends
            time.sleep(30)  # Check every 30 seconds
    
    # Run in background thread
    thread = threading.Thread(target=run_notifications, daemon=True)
    thread.start()