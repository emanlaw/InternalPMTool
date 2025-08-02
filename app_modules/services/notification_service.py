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

def send_admin_notification(notification_type, user_data):
    """Send notification to admin about user registration"""
    try:
        data = load_data()
        admin_users = [u for u in data.get('users', []) if u.get('role') == 'admin' and u.get('email')]
        
        if not admin_users:
            print("No admin users with email found")
            return
        
        if notification_type == 'new_user_registration':
            subject = f"PM Tool: New User Registration - {user_data['display_name']}"
            
            html_body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background: #0079bf; color: white; padding: 20px; text-align: center;">
                    <h1>👤 New User Registration</h1>
                </div>
                
                <div style="padding: 20px;">
                    <p>A new user has registered and is awaiting approval:</p>
                    
                    <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 20px 0;">
                        <h3 style="margin: 0 0 10px 0; color: #172b4d;">User Details</h3>
                        <p><strong>Display Name:</strong> {user_data['display_name']}</p>
                        <p><strong>Username:</strong> {user_data['username']}</p>
                        <p><strong>Email:</strong> {user_data['email']}</p>
                        <p><strong>Registration Date:</strong> {user_data['created_at']}</p>
                        <p><strong>Status:</strong> <span style="color: #ffab00; font-weight: bold;">Pending Approval</span></p>
                    </div>
                    
                    <p>Please review and approve or reject this registration in the admin dashboard.</p>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="http://localhost:5000/admin/users" 
                           style="background: #0079bf; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                            Manage Users
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
            
            for admin in admin_users:
                try:
                    msg = Message(
                        subject=subject,
                        recipients=[admin['email']],
                        html=html_body
                    )
                    
                    if current_app.extensions.get('mail'):
                        current_app.extensions['mail'].send(msg)
                        print(f"Admin notification sent to {admin['username']}")
                    else:
                        print(f"Mail not configured, would send to {admin['username']}: {subject}")
                        
                except Exception as e:
                    print(f"Error sending admin notification to {admin['username']}: {e}")
                    
    except Exception as e:
        print(f"Error sending admin notification: {e}")

def send_user_status_notification(user_data, old_status, new_status):
    """Send notification to user about status change"""
    try:
        if not user_data.get('email'):
            return
        
        status_messages = {
            'active': 'Your account has been approved and is now active!',
            'inactive': 'Your account registration has been rejected.',
            'suspended': 'Your account has been suspended.',
            'pending': 'Your account is pending approval.'
        }
        
        subject = f"PM Tool: Account Status Update - {new_status.title()}"
        status_message = status_messages.get(new_status, f'Your account status has been changed to {new_status}.')
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: #0079bf; color: white; padding: 20px; text-align: center;">
                <h1>📧 Account Status Update</h1>
            </div>
            
            <div style="padding: 20px;">
                <p>Hello {user_data['display_name']},</p>
                
                <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin: 0 0 10px 0; color: #172b4d;">Status Update</h3>
                    <p>{status_message}</p>
                    <p><strong>Previous Status:</strong> {old_status.title()}</p>
                    <p><strong>Current Status:</strong> {new_status.title()}</p>
                </div>
                
                {f'<div style="text-align: center; margin: 30px 0;"><a href="http://localhost:5000/login" style="background: #0079bf; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">Login to PM Tool</a></div>' if new_status == 'active' else ''}
                
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
            subject=subject,
            recipients=[user_data['email']],
            html=html_body
        )
        
        if current_app.extensions.get('mail'):
            current_app.extensions['mail'].send(msg)
            print(f"Status notification sent to {user_data['username']}")
        else:
            print(f"Mail not configured, would send to {user_data['username']}: {subject}")
            
    except Exception as e:
        print(f"Error sending user status notification: {e}")