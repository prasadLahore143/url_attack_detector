import sqlite3
import json
from datetime import datetime
import os

class AttackDatabase:
    def __init__(self, db_path="../data/attacks.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create attacks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attacks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                source_ip TEXT NOT NULL,
                url TEXT NOT NULL,
                method TEXT DEFAULT 'GET',
                user_agent TEXT,
                attack_type TEXT NOT NULL,
                is_malicious BOOLEAN NOT NULL,
                is_successful BOOLEAN DEFAULT FALSE,
                severity TEXT DEFAULT 'low',
                confidence REAL DEFAULT 0.0,
                pattern_matched TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create index for faster queries
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_timestamp ON attacks(timestamp)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_source_ip ON attacks(source_ip)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_attack_type ON attacks(attack_type)
        ''')
        
        conn.commit()
        conn.close()
    
    def insert_attack(self, attack_data):
        """Insert a single attack record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO attacks (
                timestamp, source_ip, url, method, user_agent, 
                attack_type, is_malicious, is_successful, severity, 
                confidence, pattern_matched
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            attack_data.get('timestamp', datetime.now().isoformat()),
            attack_data.get('source_ip', ''),
            attack_data.get('url', ''),
            attack_data.get('method', 'GET'),
            attack_data.get('user_agent', ''),
            attack_data.get('attack_type', 'unknown'),
            attack_data.get('is_malicious', False),
            attack_data.get('is_successful', False),
            attack_data.get('severity', 'low'),
            attack_data.get('confidence', 0.0),
            attack_data.get('pattern_matched', '')
        ))
        
        conn.commit()
        attack_id = cursor.lastrowid
        conn.close()
        return attack_id
    
    def insert_batch(self, attacks_list):
        """Insert multiple attack records"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        records = []
        for attack in attacks_list:
            records.append((
                attack.get('timestamp', datetime.now().isoformat()),
                attack.get('source_ip', ''),
                attack.get('url', ''),
                attack.get('method', 'GET'),
                attack.get('user_agent', ''),
                attack.get('attack_type', 'unknown'),
                attack.get('is_malicious', False),
                attack.get('is_successful', False),
                attack.get('severity', 'low'),
                attack.get('confidence', 0.0),
                attack.get('pattern_matched', '')
            ))
        
        cursor.executemany('''
            INSERT INTO attacks (
                timestamp, source_ip, url, method, user_agent, 
                attack_type, is_malicious, is_successful, severity, 
                confidence, pattern_matched
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', records)
        
        conn.commit()
        conn.close()
        return len(records)
    
    def get_attacks(self, limit=100, offset=0, filters=None):
        """Get attacks with optional filtering"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT * FROM attacks"
        params = []
        
        if filters:
            conditions = []
            if 'attack_type' in filters:
                conditions.append("attack_type = ?")
                params.append(filters['attack_type'])
            if 'source_ip' in filters:
                conditions.append("source_ip = ?")
                params.append(filters['source_ip'])
            if 'is_malicious' in filters:
                conditions.append("is_malicious = ?")
                params.append(filters['is_malicious'])
            if 'severity' in filters:
                conditions.append("severity = ?")
                params.append(filters['severity'])
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        # Convert to list of dictionaries
        result = []
        for row in rows:
            result.append(dict(row))
        
        conn.close()
        return result
    
    def get_statistics(self):
        """Get attack statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # Total attacks
        cursor.execute("SELECT COUNT(*) FROM attacks")
        stats['total_attacks'] = cursor.fetchone()[0]
        
        # Malicious attacks
        cursor.execute("SELECT COUNT(*) FROM attacks WHERE is_malicious = 1")
        stats['malicious_attacks'] = cursor.fetchone()[0]
        
        # Successful attacks
        cursor.execute("SELECT COUNT(*) FROM attacks WHERE is_successful = 1")
        stats['successful_attacks'] = cursor.fetchone()[0]
        
        # Attack types distribution
        cursor.execute("""
            SELECT attack_type, COUNT(*) as count 
            FROM attacks 
            GROUP BY attack_type 
            ORDER BY count DESC
        """)
        stats['attack_types'] = dict(cursor.fetchall())
        
        # Severity distribution
        cursor.execute("""
            SELECT severity, COUNT(*) as count 
            FROM attacks 
            GROUP BY severity 
            ORDER BY count DESC
        """)
        stats['severity_distribution'] = dict(cursor.fetchall())
        
        # Top source IPs
        cursor.execute("""
            SELECT source_ip, COUNT(*) as count 
            FROM attacks 
            WHERE is_malicious = 1
            GROUP BY source_ip 
            ORDER BY count DESC 
            LIMIT 10
        """)
        stats['top_malicious_ips'] = dict(cursor.fetchall())
        
        conn.close()
        return stats
    
    def search_by_ip_range(self, ip_start, ip_end):
        """Search attacks by IP range"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM attacks 
            WHERE source_ip BETWEEN ? AND ? 
            ORDER BY timestamp DESC
        """, (ip_start, ip_end))
        
        rows = cursor.fetchall()
        result = [dict(row) for row in rows]
        
        conn.close()
        return result
    
    def export_to_json(self, filename, filters=None):
        """Export attacks to JSON file"""
        attacks = self.get_attacks(limit=10000, filters=filters)
        with open(filename, 'w') as f:
            json.dump(attacks, f, indent=2, default=str)
        return len(attacks)
    
    def export_to_csv(self, filename, filters=None):
        """Export attacks to CSV file"""
        import csv
        
        attacks = self.get_attacks(limit=10000, filters=filters)
        if not attacks:
            return 0
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            fieldnames = attacks[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(attacks)
        
        return len(attacks)

if __name__ == "__main__":
    # Test the database
    db = AttackDatabase()
    
    # Test data
    test_attack = {
        'timestamp': datetime.now().isoformat(),
        'source_ip': '192.168.1.100',
        'url': 'http://example.com/login.php?user=admin',
        'attack_type': 'sql_injection',
        'is_malicious': True,
        'severity': 'high'
    }
    
    # Insert test record
    attack_id = db.insert_attack(test_attack)
    print(f"Inserted attack with ID: {attack_id}")
    
    # Get statistics
    stats = db.get_statistics()
    print("Database statistics:")
    print(json.dumps(stats, indent=2))