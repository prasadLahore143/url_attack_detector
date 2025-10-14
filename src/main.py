#!/usr/bin/env python3
"""
URL Attack Detection System - Main Application
This is the main entry point for the URL-based attack detection system.
"""

import argparse
import sys
import os
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from dataset_generator import AttackDatasetGenerator
from attack_detector import URLAttackDetector
from database import AttackDatabase
from web_interface import app

def main():
    parser = argparse.ArgumentParser(description='URL Attack Detection System')
    parser.add_argument('--mode', choices=['web', 'cli', 'generate', 'analyze'], 
                       default='web', help='Operation mode')
    parser.add_argument('--url', type=str, help='URL to analyze (for CLI mode)')
    parser.add_argument('--num-records', type=int, default=1000, 
                       help='Number of records to generate')
    parser.add_argument('--port', type=int, default=5000, help='Web server port')
    parser.add_argument('--host', type=str, default='127.0.0.1', help='Web server host')
    
    args = parser.parse_args()
    
    # Initialize components
    db = AttackDatabase()
    detector = URLAttackDetector()
    generator = AttackDatasetGenerator()
    
    if args.mode == 'web':
        print("Starting URL Attack Detection Web Interface...")
        print(f"Server running at http://{args.host}:{args.port}")
        print("Press Ctrl+C to stop the server")
        try:
            app.run(debug=True, host=args.host, port=args.port)
        except KeyboardInterrupt:
            print("\nServer stopped.")
    
    elif args.mode == 'cli':
        if not args.url:
            print("Error: --url is required for CLI mode")
            sys.exit(1)
        
        print(f"Analyzing URL: {args.url}")
        result = detector.analyze_url(args.url)
        
        print(f"Status: {'MALICIOUS' if result['is_malicious'] else 'LEGITIMATE'}")
        if result['is_malicious']:
            print(f"Severity: {result['severity'].upper()}")
            print(f"Confidence: {result['confidence']:.1%}")
            print(f"Attacks detected: {len(result['attacks_detected'])}")
            for attack in result['attacks_detected']:
                print(f"  - {attack['type']}: {attack['pattern_matched']}")
        
        # Store result in database
        attack_data = {
            'url': args.url,
            'attack_type': result['attacks_detected'][0]['type'] if result['attacks_detected'] else 'none',
            'is_malicious': result['is_malicious'],
            'severity': result['severity'],
            'confidence': result['confidence']
        }
        db.insert_attack(attack_data)
        print("Result stored in database.")
    
    elif args.mode == 'generate':
        print(f"Generating {args.num_records} sample attack records...")
        dataset = generator.generate_dataset(args.num_records)
        
        # Store in database
        count = db.insert_batch(dataset)
        print(f"Generated and stored {count} records in database.")
        
        # Show statistics
        stats = db.get_statistics()
        print(f"\nDatabase Statistics:")
        print(f"  Total attacks: {stats['total_attacks']}")
        print(f"  Malicious: {stats['malicious_attacks']}")
        print(f"  Successful: {stats['successful_attacks']}")
    
    elif args.mode == 'analyze':
        print("Interactive URL Analysis Mode")
        print("Enter URLs to analyze (type 'quit' to exit):")
        
        while True:
            url = input("\nURL> ").strip()
            if url.lower() in ['quit', 'exit', 'q']:
                break
            
            if not url:
                continue
            
            result = detector.analyze_url(url)
            print(f"Status: {'MALICIOUS' if result['is_malicious'] else 'LEGITIMATE'}")
            
            if result['is_malicious']:
                print(f"Severity: {result['severity'].upper()}")
                print(f"Confidence: {result['confidence']:.1%}")
                for attack in result['attacks_detected']:
                    print(f"  - {attack['type'].replace('_', ' ').title()}")
            
            # Store in database
            attack_data = {
                'url': url,
                'attack_type': result['attacks_detected'][0]['type'] if result['attacks_detected'] else 'none',
                'is_malicious': result['is_malicious'],
                'severity': result['severity'],
                'confidence': result['confidence']
            }
            db.insert_attack(attack_data)

def show_system_info():
    """Display system information and usage instructions"""
    print("=" * 60)
    print("URL ATTACK DETECTION SYSTEM")
    print("=" * 60)
    print("This system detects various URL-based attacks including:")
    print("  • SQL Injection")
    print("  • Cross-Site Scripting (XSS)")
    print("  • Directory Traversal")
    print("  • Command Injection")
    print("  • Server-Side Request Forgery (SSRF)")
    print("  • Local/Remote File Inclusion")
    print("  • Credential Stuffing")
    print("  • Typosquatting")
    print("\nUsage:")
    print("  python main.py --mode web     # Start web interface")
    print("  python main.py --mode cli --url <URL>  # Analyze single URL")
    print("  python main.py --mode generate --num-records 1000  # Generate sample data")
    print("  python main.py --mode analyze # Interactive analysis")
    print("=" * 60)

if __name__ == "__main__":
    try:
        show_system_info()
        main()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)