import random
import json
import csv
from datetime import datetime
import urllib.parse

class AttackDatasetGenerator:
    def __init__(self):
        self.sql_patterns = ["' OR '1'='1", "'; DROP TABLE users--", "' UNION SELECT *"]
        self.xss_patterns = ["<script>alert('XSS')</script>", "<img src=x onerror=alert(1)>"]
        self.traversal_patterns = ["../../../etc/passwd", "..\\..\\windows\\system32"]
    
    def generate_attack_url(self, attack_type):
        domain = "example.com"
        if attack_type == "sql_injection":
            payload = random.choice(self.sql_patterns)
            return f"http://{domain}/login.php?user={urllib.parse.quote(payload)}"
        elif attack_type == "xss":
            payload = random.choice(self.xss_patterns)
            return f"http://{domain}/search.php?q={urllib.parse.quote(payload)}"
        elif attack_type == "directory_traversal":
            payload = random.choice(self.traversal_patterns)
            return f"http://{domain}/file.php?path={urllib.parse.quote(payload)}"
        return f"http://{domain}/normal.php"
    
    def generate_dataset(self, num_records=100):
        dataset = []
        attack_types = ["sql_injection", "xss", "directory_traversal", "legitimate"]
        
        for i in range(num_records):
            attack_type = random.choice(attack_types)
            is_malicious = attack_type != "legitimate"
            
            record = {
                "id": i + 1,
                "timestamp": datetime.now().isoformat(),
                "source_ip": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                "url": self.generate_attack_url(attack_type),
                "attack_type": attack_type,
                "is_malicious": is_malicious,
                "severity": "high" if is_malicious else "none"
            }
            dataset.append(record)
        
        return dataset
    
    def save_to_file(self, dataset, filename):
        with open(filename, 'w') as f:
            json.dump(dataset, f, indent=2)
        print(f"Dataset saved to {filename}")

if __name__ == "__main__":
    generator = AttackDatasetGenerator()
    data = generator.generate_dataset(500)
    generator.save_to_file(data, "../data/sample_attacks.json")