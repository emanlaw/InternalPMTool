from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
from app.services.firebase_service import firebase_service

firebase_bp = Blueprint('firebase', __name__)

@firebase_bp.route('/migrate-to-firebase')
@login_required
def migrate_to_firebase():
    """Migrate existing JSON data to Firebase"""
    try:
        success = firebase_service.migrate_json_data('data.json')
        if success:
            return jsonify({'success': True, 'message': 'Data migrated to Firebase successfully!'})
        else:
            return jsonify({'success': False, 'message': 'Migration failed'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': f'Migration error: {str(e)}'}), 500

@firebase_bp.route('/firebase-status')
@login_required
def firebase_status():
    """Check Firebase connection status"""
    try:
        from config.firebase_config import firebase_config
        
        # Check if Firebase is configured
        if firebase_config.db is None:
            return jsonify({
                'success': False,
                'status': 'Firebase not configured',
                'error': 'Firebase credentials not set up. Please run setup_firebase_credentials.py'
            }), 500
        
        # Test Firebase connection by getting data counts
        users = firebase_service.get_all_users()
        projects = firebase_service.get_all_projects()
        cards = firebase_service.get_all_cards()
        
        return jsonify({
            'success': True,
            'status': 'Connected to Firebase',
            'data': {
                'users_count': len(users),
                'projects_count': len(projects),
                'cards_count': len(cards)
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'status': 'Firebase connection failed',
            'error': str(e)
        }), 500

@firebase_bp.route('/firebase-dashboard')
@login_required
def firebase_dashboard():
    """Firebase management dashboard"""
    return render_template('firebase_dashboard.html')