from flask import Flask, render_template, request, jsonify, send_file, session
import json
import os
from database import AttackDatabase
from attack_detector import URLAttackDetector
from dataset_generator import AttackDatasetGenerator

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = 'url-attack-detector-secret-key-2024'  # Change this in production

# Initialize components
db = AttackDatabase()
detector = URLAttackDetector()
generator = AttackDatasetGenerator()

@app.route('/')
def dashboard():
    """Main dashboard"""
    # Only show data from current session to keep dashboard clean on refresh
    session_attacks = session.get('current_session_attacks', [])
    
    if session_attacks:
        # Calculate stats from session data only
        stats = {
            'total_attacks': len(session_attacks),
            'successful_attacks': sum(1 for a in session_attacks if a.get('is_successful')),
            'malicious_attacks': sum(1 for a in session_attacks if a.get('is_malicious')),
            'attack_types': {},
            'severity_distribution': {}
        }
        
        for attack in session_attacks:
            attack_type_str = attack.get('attack_type', 'unknown')
            severity = attack.get('severity', 'unknown')
            
            # Handle multiple attack types (comma-separated)
            if ',' in attack_type_str:
                attack_types = [t.strip() for t in attack_type_str.split(',')]
                for attack_type in attack_types:
                    stats['attack_types'][attack_type] = stats['attack_types'].get(attack_type, 0) + 1
            else:
                stats['attack_types'][attack_type_str] = stats['attack_types'].get(attack_type_str, 0) + 1
            
            stats['severity_distribution'][severity] = stats['severity_distribution'].get(severity, 0) + 1
        
        recent_attacks = session_attacks[-10:]  # Last 10 attacks from session
    else:
        # Empty stats for clean dashboard
        stats = {
            'total_attacks': 0,
            'successful_attacks': 0,
            'malicious_attacks': 0,
            'attack_types': {},
            'severity_distribution': {}
        }
        recent_attacks = []
    
    return render_template('dashboard.html', stats=stats, recent_attacks=recent_attacks)

@app.route('/analyze', methods=['GET', 'POST'])
def analyze_url():
    """URL analysis page"""
    if request.method == 'POST':
        url = request.form.get('url')
        
        if url:
            # Analyze URL with automatic validation
            result = detector.analyze_url(url, validate_existence=True)
            
            # Determine success based on URL status and safety
            is_successful = False
            if result.get('url_exists') == True:
                # URL exists and is accessible
                if not result['is_malicious']:
                    # Safe URL that exists - this is a successful legitimate access
                    is_successful = True
                else:
                    # Malicious URL that exists - potential security risk
                    is_successful = False
            else:
                # URL doesn't exist - no successful access possible
                is_successful = False
            
            # Store in database (for export/persistence)
            # Handle multiple attack types by combining them
            if result['attacks_detected']:
                attack_types = [attack['type'] for attack in result['attacks_detected']]
                combined_attack_type = ', '.join(attack_types)
                patterns_matched = [attack['pattern_matched'] for attack in result['attacks_detected']]
                combined_patterns = ' | '.join(patterns_matched)
            else:
                combined_attack_type = 'legitimate'
                combined_patterns = ''
            
            attack_data = {
                'url': url,
                'source_ip': request.remote_addr or '127.0.0.1',
                'attack_type': combined_attack_type,
                'is_malicious': result['is_malicious'],
                'is_successful': is_successful,
                'severity': result['severity'],
                'confidence': result['confidence'],
                'pattern_matched': combined_patterns
            }
            db.insert_attack(attack_data)
            
            # Also store in session for dashboard display
            if 'current_session_attacks' not in session:
                session['current_session_attacks'] = []
            
            # Add timestamp for session display
            from datetime import datetime
            attack_data['timestamp'] = datetime.now().isoformat()
            
            session['current_session_attacks'].append(attack_data)
            session.modified = True
            
            return render_template('analyze.html', result=result, url=url)
    return render_template('analyze.html')

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for URL analysis"""
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    result = detector.analyze_url(url, validate_existence=True)
    
    # Store in database
    # Handle multiple attack types by combining them
    if result['attacks_detected']:
        attack_types = [attack['type'] for attack in result['attacks_detected']]
        combined_attack_type = ', '.join(attack_types)
        patterns_matched = [attack['pattern_matched'] for attack in result['attacks_detected']]
        combined_patterns = ' | '.join(patterns_matched)
    else:
        combined_attack_type = 'legitimate'
        combined_patterns = ''
    
    attack_data = {
        'url': url,
        'source_ip': request.remote_addr or '127.0.0.1',
        'attack_type': combined_attack_type,
        'is_malicious': result['is_malicious'],
        'severity': result['severity'],
        'confidence': result['confidence'],
        'pattern_matched': combined_patterns
    }
    db.insert_attack(attack_data)
    
    return jsonify(result)

@app.route('/attacks')
def view_attacks():
    """View all attacks with filtering - shows all database data for export/review"""
    page = int(request.args.get('page', 1))
    per_page = 50
    offset = (page - 1) * per_page
    
    filters = {}
    if request.args.get('attack_type'):
        filters['attack_type'] = request.args.get('attack_type')
    if request.args.get('severity'):
        filters['severity'] = request.args.get('severity')
    if request.args.get('is_malicious'):
        filters['is_malicious'] = request.args.get('is_malicious') == 'true'
    
    attacks = db.get_attacks(limit=per_page, offset=offset, filters=filters)
    return render_template('attacks.html', attacks=attacks, page=page, filters=filters)

@app.route('/statistics')
def statistics():
    """Statistics page"""
    stats = db.get_statistics()
    return render_template('statistics.html', stats=stats)

@app.route('/generate-data', methods=['POST'])
def generate_sample_data():
    """Generate sample attack data"""
    num_records = int(request.form.get('num_records', 100))
    
    dataset = generator.generate_dataset(num_records)
    
    # Store in database
    db.insert_batch(dataset)
    
    # Also add a sample of the data to session for dashboard display
    # Show the last 10 generated records on the dashboard
    session_sample = dataset[-10:] if len(dataset) > 10 else dataset
    
    # Clear existing session data first
    session['current_session_attacks'] = session_sample
    session.modified = True
    
    return jsonify({'message': f'Generated {len(dataset)} sample records, showing {len(session_sample)} on dashboard'})

@app.route('/export')
def export_data():
    """Export data page"""
    return render_template('export.html')

@app.route('/export/<format>')
def export_attacks(format):
    """Export attacks in specified format"""
    filters = {}
    if request.args.get('attack_type'):
        filters['attack_type'] = request.args.get('attack_type')
    
    if format == 'json':
        filename = '../data/exported_attacks.json'
        count = db.export_to_json(filename, filters)
        return send_file(filename, as_attachment=True)
    elif format == 'csv':
        filename = '../data/exported_attacks.csv'
        count = db.export_to_csv(filename, filters)
        return send_file(filename, as_attachment=True)
    else:
        return jsonify({'error': 'Unsupported format'}), 400

@app.route('/api/stats')
def api_statistics():
    """API endpoint for statistics"""
    stats = db.get_statistics()
    return jsonify(stats)

@app.route('/clear-data', methods=['POST'])
def clear_data():
    """Clear all attack data from database"""
    try:
        # Clear all attacks from database
        count = db.clear_all_attacks()
        return jsonify({
            'success': True, 
            'message': f'Successfully cleared {count} records from database',
            'cleared_count': count
        })
    except Exception as e:
        return jsonify({
            'success': False, 
            'message': f'Error clearing database: {str(e)}'
        }), 500

@app.route('/clear-session', methods=['POST'])
def clear_session_data():
    """Clear session data (dashboard display)"""
    try:
        session_count = len(session.get('current_session_attacks', []))
        session.pop('current_session_attacks', None)
        session.modified = True
        return jsonify({
            'success': True, 
            'message': f'Successfully cleared {session_count} items from dashboard display',
            'cleared_count': session_count
        })
    except Exception as e:
        return jsonify({
            'success': False, 
            'message': f'Error clearing session data: {str(e)}'
        }), 500

@app.route('/reset-database', methods=['POST'])
def reset_database():
    """Completely reset the database (clear all data and recreate tables)"""
    try:
        # Reset entire database
        db.reset_database()
        return jsonify({
            'success': True, 
            'message': 'Database has been completely reset'
        })
    except Exception as e:
        return jsonify({
            'success': False, 
            'message': f'Error resetting database: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)