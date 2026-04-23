import json
import re
from pathlib import Path

def extract_vulnerabilities_from_response(response_text):
    vulnerabilities = []
    response_lower = response_text.lower()
    
    # Mapping patterns to vulnerabilities
    patterns = {
        "sql_injection": [
            "sql injection", "sql injection vulnerability", 
            "concatenat", "parameterized query", "prepared statement",
            "SELECT.*WHERE.*=", "inject"
        ],
        "command_injection": [
            "command injection", "os command", "shell injection",
            "subprocess", "shell=true"
        ],
        "path_traversal": [
            "path traversal", "directory traversal", "../",
            "file system", "read arbitrary files"
        ],
        "xss": [
            "xss", "cross-site scripting", "cross site scripting",
            "html injection", "script tag"
        ],
        "broken_access_control": [
            "broken access control", "authorization bypass",
            "privilege escalation", "missing permission check"
        ],
        "authentication_bypass": [
            "authentication bypass", "auth bypass",
            "session fixation", "weak authentication"
        ],
        "ssrf": [
            "ssrf", "server-side request forgery", "server side request forgery",
            "fetch url", "request forgery"
        ],
        "insecure_deserialization": [
            "insecure deserialization", "pickle", "unpickle",
            "deserialization vulnerability"
        ],
        "cryptographic_failure": [
            "cryptographic failure", "weak hashing", "md5", "sha1",
            "hardcoded key", "hardcoded secret"
        ],
        "security_misconfiguration": [
            "security misconfiguration", "missing header",
            "debug mode", "stack trace", "exposed"
        ],
        "vulnerable_component": [
            "vulnerable component", "outdated", "cve",
            "deprecated", "known vulnerability"
        ],
        "logging_failure": [
            "logging failure", "missing log", "audit log",
            "failed login", "sensitive data in logs"
        ]
    }
    
    # Mapping for the names expected by ground truth 
    name_mapping = {
        "sql_injection": "SQL Injection",
        "command_injection": "Command Injection",
        "path_traversal": "Path Traversal",
        "xss": "XSS",
        "broken_access_control": "Broken Access Control",
        "authentication_bypass": "Authentication Failure",
        "ssrf": "SSRF",
        "insecure_deserialization": "Insecure Deserialization",
        "cryptographic_failure": "Cryptographic Failure",
        "security_misconfiguration": "Security Misconfiguration",
        "vulnerable_component": "Vulnerable Component",
        "logging_failure": "Logging Failure"
    }
    
    for vuln_key, patterns_list in patterns.items():
        for pattern in patterns_list:
            if re.search(pattern, response_lower):
                vulnerabilities.append(name_mapping[vuln_key])
                break
    
    # Check if the model claims there are no vulnerabilities.
    if re.search(r"no vulnerabilit|no security issue|no issue found|secure", response_lower):
        if len(vulnerabilities) == 0:
            return []
    
    return list(set(vulnerabilities))

def calculate_metrics(expected, detected):
    expected_set = set(expected)
    detected_set = set(detected)
    
    true_positives = len(expected_set.intersection(detected_set))
    false_positives = len(detected_set - expected_set)
    false_negatives = len(expected_set - detected_set)
    
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        "true_positives": true_positives,
        "false_positives": false_positives,
        "false_negatives": false_negatives,
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1": round(f1, 3)
    }

def classify_error(expected, detected, response_text):
    expected_set = set(expected)
    detected_set = set(detected)
    
    if len(expected_set - detected_set) > 0 and len(detected_set - expected_set) == 0:
        if len(detected_set) == 0:
            return "total_omission"
        return "partial_omission"
    
    if len(detected_set - expected_set) > 0 and len(expected_set - detected_set) == 0:
        return "commission"
    
    if len(expected_set - detected_set) > 0 and len(detected_set - expected_set) > 0:
        return "mixed"
    
    if len(expected_set) > 0 and len(detected_set) == 0:
        return "total_omission"
    
    return "correct"

def evaluate_all_responses(raw_dir, ground_truth, output_file):
    all_metrics = []
    raw_path = Path(raw_dir)
    
    for json_file in raw_path.glob("*.json"):
        with open(json_file, "r") as f:
            data = json.load(f)
        
        case_id = data["case_id"]
        expected = ground_truth.get(case_id, [])
        
        response_content = data.get("response", {})
        response_text = ""
        
        if response_content and "candidates" in response_content:
            candidate = response_content["candidates"][0]
            if "content" in candidate and "parts" in candidate["content"]:
                response_text = candidate["content"]["parts"][0].get("text", "")
        
        detected = extract_vulnerabilities_from_response(response_text)
        metrics = calculate_metrics(expected, detected)
        error_type = classify_error(expected, detected, response_text)
        
        metrics["case_id"] = case_id
        metrics["prompt_strategy"] = data["prompt_strategy"]
        metrics["execution"] = data["execution"]
        metrics["error_type"] = error_type
        metrics["response_preview"] = response_text[:300] if response_text else ""
        
        all_metrics.append(metrics)
    
    with open(output_file, "w") as f:
        json.dump(all_metrics, f, indent=2)
    
    return all_metrics
