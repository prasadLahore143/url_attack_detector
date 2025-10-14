import re
import urllib.parse
import base64
import json
import requests
import time
from urllib.parse import urlparse

class URLAttackDetector:
    def __init__(self):
        self.sql_patterns = [
            r"('|(\\x27)|(\\x2D)|(\\x23))",
            r"(\\x23)|(#)|(\\x2D)|(-)",
            r"union.*select",
            r"insert.*into",
            r"delete.*from",
            r"drop.*table",
            r"exec.*xp_",
            r"sp_.*execute"
        ]
        
        self.xss_patterns = [
            r"<script[^>]*>.*</script>",
            r"javascript:",
            r"<iframe.*src",
            r"<img.*onerror",
            r"<svg.*onload",
            r"alert\(",
            r"document\.cookie",
            r"<object.*data"
        ]
        
        self.traversal_patterns = [
            r"\.\./",
            r"\.\.\\",
            r"/etc/passwd",
            r"/windows/system32",
            r"boot\.ini",
            r"etc/shadow",
            r"proc/self/environ"
        ]
        
        self.command_patterns = [
            r";\s*(cat|ls|dir|type|ping|wget|curl)",
            r"\|\s*(nc|netcat|telnet)",
            r"&&\s*(whoami|id|uname)",
            r"`.*`",
            r"\$\(.*\)"
        ]
        
        self.ssrf_patterns = [
            r"(localhost|127\.0\.0\.1)",
            r"169\.254\.169\.254",
            r"192\.168\.",
            r"10\.\d+\.",
            r"172\.(1[6-9]|2\d|3[0-1])\.",
            r"file://",
            r"gopher://"
        ]

    def detect_sql_injection(self, url):
        """Detect SQL injection patterns"""
        decoded_url = urllib.parse.unquote(url).lower()
        for pattern in self.sql_patterns:
            if re.search(pattern, decoded_url, re.IGNORECASE):
                return True, pattern
        return False, None

    def detect_xss(self, url):
        """Detect XSS patterns"""
        decoded_url = urllib.parse.unquote(url).lower()
        for pattern in self.xss_patterns:
            if re.search(pattern, decoded_url, re.IGNORECASE):
                return True, pattern
        return False, None

    def detect_directory_traversal(self, url):
        """Detect directory traversal patterns"""
        decoded_url = urllib.parse.unquote(url)
        for pattern in self.traversal_patterns:
            if re.search(pattern, decoded_url, re.IGNORECASE):
                return True, pattern
        return False, None

    def detect_command_injection(self, url):
        """Detect command injection patterns"""
        decoded_url = urllib.parse.unquote(url)
        for pattern in self.command_patterns:
            if re.search(pattern, decoded_url, re.IGNORECASE):
                return True, pattern
        return False, None

    def detect_ssrf(self, url):
        """Detect SSRF patterns"""
        decoded_url = urllib.parse.unquote(url)
        for pattern in self.ssrf_patterns:
            if re.search(pattern, decoded_url, re.IGNORECASE):
                return True, pattern
        return False, None
    
    def validate_url_exists(self, url, timeout=5):
        """Check if URL exists and is accessible (optional feature)"""
        try:
            # Parse URL to check if it's well-formed
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return {
                    'exists': False,
                    'status': 'invalid_format',
                    'response_code': None,
                    'response_time': None,
                    'error': 'Invalid URL format'
                }
            
            start_time = time.time()
            
            # Make HEAD request first (lighter than GET)
            headers = {
                'User-Agent': 'URL Attack Detection System (Security Scanner)',
                'Accept': '*/*'
            }
            
            response = requests.head(url, timeout=timeout, headers=headers, allow_redirects=True)
            response_time = round((time.time() - start_time) * 1000, 2)  # ms
            
            return {
                'exists': response.status_code < 400,
                'status': 'accessible' if response.status_code < 400 else 'not_accessible',
                'response_code': response.status_code,
                'response_time': response_time,
                'error': None,
                'server': response.headers.get('Server', 'Unknown'),
                'content_type': response.headers.get('Content-Type', 'Unknown')
            }
            
        except requests.exceptions.ConnectTimeout:
            return {
                'exists': False,
                'status': 'timeout',
                'response_code': None,
                'response_time': None,
                'error': 'Connection timeout'
            }
        except requests.exceptions.ConnectionError:
            return {
                'exists': False,
                'status': 'connection_error',
                'response_code': None,
                'response_time': None,
                'error': 'Connection failed - URL may not exist'
            }
        except requests.exceptions.RequestException as e:
            return {
                'exists': False,
                'status': 'request_error',
                'response_code': None,
                'response_time': None,
                'error': str(e)
            }
        except Exception as e:
            return {
                'exists': False,
                'status': 'unknown_error',
                'response_code': None,
                'response_time': None,
                'error': str(e)
            }
    
    def calculate_pattern_confidence(self, pattern, url_data, attack_type):
        """Calculate dynamic confidence based on pattern specificity and context"""
        base_confidence = 0.6  # Start with 60%
        
        # High-confidence patterns (very specific)
        high_confidence_patterns = [
            r"('|(\\x27)|(\\x2D)|(\\x23))",  # SQL injection quotes
            r"<script[^>]*>.*</script>",        # Complete script tags
            r"union.*select",                   # SQL UNION SELECT
            r"drop.*table",                     # SQL DROP TABLE
            r"/etc/passwd",                     # Linux password file
            r"\.\./.*/.*\.\./.*/.*\.\./"       # Multiple directory traversals
        ]
        
        # Medium-confidence patterns
        medium_confidence_patterns = [
            r"javascript:",
            r"alert\(",
            r"\.\./",
            r"127\.0\.0\.1"
        ]
        
        # Check pattern specificity
        if any(p in pattern for p in high_confidence_patterns):
            base_confidence = 0.9  # 90% for very specific patterns
        elif any(p in pattern for p in medium_confidence_patterns):
            base_confidence = 0.75  # 75% for medium patterns
        else:
            base_confidence = 0.65  # 65% for general patterns
        
        # Boost confidence for multiple suspicious indicators
        suspicious_chars = self.count_suspicious_characters(url_data.get('decoded', url_data.get('original', '')))
        if suspicious_chars > 5:
            base_confidence += 0.1
        elif suspicious_chars > 3:
            base_confidence += 0.05
        
        # Boost for dangerous attack types
        dangerous_types = ['sql_injection', 'command_injection']
        if attack_type in dangerous_types:
            base_confidence += 0.05
        
        # Check for encoding (suggests obfuscation)
        original_url = url_data.get('original', '')
        decoded_url = url_data.get('decoded', '')
        if original_url != decoded_url and ('%' in original_url or '+' in original_url):
            base_confidence += 0.08
        
        # Cap at 0.95 (95%) to leave room for uncertainty
        return min(base_confidence, 0.95)
    
    def count_suspicious_characters(self, url_string):
        """Count suspicious characters in URL that might indicate attacks"""
        suspicious_chars = r'[<>\'"`;(){}[\\|&$`%]'
        import re
        matches = re.findall(suspicious_chars, url_string)
        return len(matches)

    def analyze_url(self, url, validate_existence=True, timeout=5):
        """Comprehensive URL analysis
        
        Args:
            url (str): URL to analyze
            validate_existence (bool): Whether to check if URL actually exists (now default True)
            timeout (int): Timeout in seconds for URL validation
        """
        results = {
            'url': url,
            'is_malicious': False,
            'attacks_detected': [],
            'severity': 'none',
            'confidence': 0.0,
            'url_validation': None,  # Will contain validation results
            'url_exists': None  # Simple boolean for URL existence
        }
        
        # Always validate URL existence first
        if validate_existence:
            print(f"🔍 Validating URL existence: {url}")
            validation_result = self.validate_url_exists(url, timeout)
            results['url_validation'] = validation_result
            results['url_exists'] = validation_result['exists']
        
        # Preprocess URL for pattern analysis
        url_data = {
            'original': url,
            'decoded': urllib.parse.unquote(url),
            'double_decoded': urllib.parse.unquote(urllib.parse.unquote(url))
        }
        
        # Check for different attack types
        attacks = [
            ('sql_injection', self.detect_sql_injection),
            ('xss', self.detect_xss),
            ('directory_traversal', self.detect_directory_traversal),
            ('command_injection', self.detect_command_injection),
            ('ssrf', self.detect_ssrf)
        ]
        
        total_confidence = 0
        for attack_name, detector in attacks:
            detected, pattern = detector(url)
            if detected:
                # Calculate dynamic confidence based on pattern and context
                pattern_confidence = self.calculate_pattern_confidence(pattern, url_data, attack_name)
                results['attacks_detected'].append({
                    'type': attack_name,
                    'pattern_matched': pattern,
                    'confidence': pattern_confidence
                })
                total_confidence += pattern_confidence
        
        if results['attacks_detected']:
            results['is_malicious'] = True
            results['confidence'] = min(total_confidence, 1.0)
            results['severity'] = self.calculate_severity(results['attacks_detected'])
        
        return results

    def calculate_severity(self, attacks):
        """Calculate attack severity based on detected attacks"""
        severity_map = {
            'sql_injection': 4,
            'command_injection': 5,
            'directory_traversal': 3,
            'xss': 3,
            'ssrf': 4
        }
        
        max_severity = max([severity_map.get(attack['type'], 1) for attack in attacks])
        
        if max_severity >= 5:
            return 'critical'
        elif max_severity >= 4:
            return 'high'
        elif max_severity >= 3:
            return 'medium'
        else:
            return 'low'

    def batch_analyze(self, urls):
        """Analyze multiple URLs"""
        results = []
        for url in urls:
            result = self.analyze_url(url)
            results.append(result)
        return results

if __name__ == "__main__":
    detector = URLAttackDetector()
    
    # Test URLs
    test_urls = [
        "http://example.com/login.php?user=' OR '1'='1",
        "http://example.com/search.php?q=<script>alert('XSS')</script>",
        "http://example.com/file.php?path=../../../etc/passwd",
        "http://example.com/normal.php?page=home"
    ]
    
    for url in test_urls:
        result = detector.analyze_url(url)
        print(f"URL: {url}")
        print(f"Malicious: {result['is_malicious']}")
        print(f"Attacks: {[a['type'] for a in result['attacks_detected']]}")
        print("---")