from flask import Flask, render_template, request, jsonify, send_file
import json
import os
from database import AttackDatabase
from attack_detector import URLAttackDetector
from dataset_generator import AttackDatasetGenerator

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Initialize components
db = AttackDatabase()
detector = URLAttackDetector()
generator = AttackDatasetGenerator()

@app.route('/')
def dashboard():
    """Main dashboard"""
    stats = db.get_statistics()
    recent_attacks = db.get_attacks(limit=10)
    return render_template('dashboard.html', stats=stats, recent_attacks=recent_attacks)

@app.route('/analyze', methods=['GET', 'POST'])
def analyze_url():
    """URL analysis page"""
    if request.method == 'POST':
        url = request.form.get('url')
        if url:
            result = detector.analyze_url(url)
            
            # Store in database - THIS WAS MISSING!
            attack_data = {
                'url': url,
                'source_ip': request.remote_addr or '127.0.0.1',
                'attack_type': result['attacks_detected'][0]['type'] if result['attacks_detected'] else 'legitimate',
                'is_malicious': result['is_malicious'],
                'severity': result['severity'],
                'confidence': result['confidence'],
                'pattern_matched': result['attacks_detected'][0]['pattern_matched'] if result['attacks_detected'] else ''
            }
            db.insert_attack(attack_data)
            
            return render_template('analyze.html', result=result, url=url)
    return render_template('analyze.html')

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for URL analysis"""
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    result = detector.analyze_url(url)
    
    # Store in database
    attack_data = {
        'url': url,
        'source_ip': request.remote_addr or '127.0.0.1',
        'attack_type': result['attacks_detected'][0]['type'] if result['attacks_detected'] else 'legitimate',
        'is_malicious': result['is_malicious'],
        'severity': result['severity'],
        'confidence': result['confidence'],
        'pattern_matched': result['attacks_detected'][0]['pattern_matched'] if result['attacks_detected'] else ''
    }
    db.insert_attack(attack_data)
    
    return jsonify(result)

@app.route('/attacks')
def view_attacks():
    """View all attacks with filtering"""
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
    
    return jsonify({'message': f'Generated {len(dataset)} sample records'})

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)