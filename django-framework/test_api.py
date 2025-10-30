#!/usr/bin/env python
"""
Test script for Graph Database API
Run this after starting the server to verify all endpoints work correctly
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://127.0.0.1:8000/api"

def print_section(title: str):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def print_result(test_name: str, passed: bool, details: str = ""):
    """Print test result"""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} - {test_name}")
    if details:
        print(f"       {details}")

def test_get_node_by_id():
    """Test: Get node by ID"""
    print_section("Test 1: Get Node by ID")
    
    try:
        response = requests.get(f"{BASE_URL}/nodes/", params={"by": "node_id", "value": "n001"})
        data = response.json()
        
        # Check status code
        passed = response.status_code == 200
        print_result("Status Code 200", passed)
        
        # Check response structure
        passed = "count" in data and "nodes" in data
        print_result("Response Structure", passed)
        
        # Check node count
        passed = data.get("count") == 1
        print_result("Single Node Returned", passed, f"Count: {data.get('count')}")
        
        # Check node ID
        if data.get("nodes"):
            node_id = data["nodes"][0].get("node_id")
            passed = node_id == "n001"
            print_result("Correct Node ID", passed, f"ID: {node_id}")
        
        print("\n📄 Sample Response:")
        print(json.dumps(data, indent=2)[:500] + "...")
        
        return True
    except Exception as e:
        print_result("Test Execution", False, str(e))
        return False

def test_get_nodes_by_name():
    """Test: Get nodes by name"""
    print_section("Test 2: Get Nodes by Name")
    
    try:
        response = requests.get(f"{BASE_URL}/nodes/", params={"by": "name", "value": "Alice Johnson"})
        data = response.json()
        
        passed = response.status_code == 200
        print_result("Status Code 200", passed)
        
        passed = data.get("count") >= 1
        print_result("Node(s) Found", passed, f"Count: {data.get('count')}")
        
        if data.get("nodes"):
            name = data["nodes"][0]["properties"].get("name")
            passed = name == "Alice Johnson"
            print_result("Correct Name", passed, f"Name: {name}")
        
        return True
    except Exception as e:
        print_result("Test Execution", False, str(e))
        return False

def test_get_nodes_by_label():
    """Test: Get nodes by label"""
    print_section("Test 3: Get Nodes by Label")
    
    try:
        response = requests.get(f"{BASE_URL}/nodes/", params={"by": "label", "value": "Person"})
        data = response.json()
        
        passed = response.status_code == 200
        print_result("Status Code 200", passed)
        
        passed = data.get("count") >= 3
        print_result("Multiple Nodes Found", passed, f"Count: {data.get('count')}")
        
        if data.get("nodes"):
            labels = data["nodes"][0].get("labels", [])
            passed = "Person" in labels
            print_result("Correct Label", passed, f"Labels: {labels}")
        
        return True
    except Exception as e:
        print_result("Test Execution", False, str(e))
        return False

def test_get_nodes_by_city():
    """Test: Get nodes by city"""
    print_section("Test 4: Get Nodes by City")
    
    try:
        response = requests.get(f"{BASE_URL}/nodes/", params={"by": "city", "value": "Chicago"})
        data = response.json()
        
        passed = response.status_code == 200
        print_result("Status Code 200", passed)
        
        passed = data.get("count") >= 1
        print_result("Node(s) Found", passed, f"Count: {data.get('count')}")
        
        if data.get("nodes"):
            city = data["nodes"][0]["properties"].get("city")
            passed = city == "Chicago"
            print_result("Correct City", passed, f"City: {city}")
        
        return True
    except Exception as e:
        print_result("Test Execution", False, str(e))
        return False

def test_get_nodes_by_status():
    """Test: Get nodes by status"""
    print_section("Test 5: Get Nodes by Status")
    
    try:
        response = requests.get(f"{BASE_URL}/nodes/", params={"by": "status", "value": "active"})
        data = response.json()
        
        passed = response.status_code == 200
        print_result("Status Code 200", passed)
        
        passed = data.get("count") >= 3
        print_result("Multiple Active Nodes", passed, f"Count: {data.get('count')}")
        
        return True
    except Exception as e:
        print_result("Test Execution", False, str(e))
        return False

def test_get_all_nodes():
    """Test: Get all nodes"""
    print_section("Test 6: Get All Nodes")
    
    try:
        response = requests.get(f"{BASE_URL}/nodes/all/")
        data = response.json()
        
        passed = response.status_code == 200
        print_result("Status Code 200", passed)
        
        passed = data.get("count") == 6
        print_result("All 6 Nodes Retrieved", passed, f"Count: {data.get('count')}")
        
        if data.get("nodes"):
            passed = len(data["nodes"]) == 6
            print_result("Correct Node Array Length", passed, f"Length: {len(data['nodes'])}")
        
        return True
    except Exception as e:
        print_result("Test Execution", False, str(e))
        return False

def test_get_node_by_id_direct():
    """Test: Get specific node by ID (direct URL)"""
    print_section("Test 7: Get Node by ID (Direct URL)")
    
    try:
        response = requests.get(f"{BASE_URL}/nodes/n001/")
        data = response.json()
        
        passed = response.status_code == 200
        print_result("Status Code 200", passed)
        
        passed = data.get("node_id") == "n001"
        print_result("Correct Node ID", passed, f"ID: {data.get('node_id')}")
        
        passed = "properties" in data and "labels" in data
        print_result("Complete Node Structure", passed)
        
        return True
    except Exception as e:
        print_result("Test Execution", False, str(e))
        return False

def test_invalid_field():
    """Test: Invalid field error handling"""
    print_section("Test 8: Error Handling - Invalid Field")
    
    try:
        response = requests.get(f"{BASE_URL}/nodes/", params={"by": "invalid_field", "value": "test"})
        
        passed = response.status_code == 400
        print_result("Status Code 400 (Bad Request)", passed, f"Code: {response.status_code}")
        
        data = response.json()
        passed = "error" in data
        print_result("Error Message Returned", passed)
        
        return True
    except Exception as e:
        print_result("Test Execution", False, str(e))
        return False

def test_node_not_found():
    """Test: Node not found scenario"""
    print_section("Test 9: Error Handling - Node Not Found")
    
    try:
        response = requests.get(f"{BASE_URL}/nodes/", params={"by": "node_id", "value": "n999"})
        
        passed = response.status_code == 404
        print_result("Status Code 404 (Not Found)", passed, f"Code: {response.status_code}")
        
        data = response.json()
        passed = data.get("count") == 0
        print_result("Zero Results", passed, f"Count: {data.get('count')}")
        
        passed = "message" in data
        print_result("Helpful Message Included", passed)
        
        return True
    except Exception as e:
        print_result("Test Execution", False, str(e))
        return False

def test_response_structure():
    """Test: Response structure validation"""
    print_section("Test 10: Response Structure Validation")
    
    try:
        response = requests.get(f"{BASE_URL}/nodes/", params={"by": "node_id", "value": "n001"})
        data = response.json()
        
        if not data.get("nodes"):
            print_result("Test Execution", False, "No nodes in response")
            return False
        
        node = data["nodes"][0]
        
        # Check required fields
        required_fields = ["node_id", "labels", "properties", "created_at", "updated_at", 
                          "relationship_count", "degree"]
        
        for field in required_fields:
            passed = field in node
            print_result(f"Field '{field}' Present", passed)
        
        # Check degree structure
        if "degree" in node:
            degree_fields = ["incoming", "outgoing", "total"]
            for field in degree_fields:
                passed = field in node["degree"]
                print_result(f"Degree '{field}' Present", passed)
        
        return True
    except Exception as e:
        print_result("Test Execution", False, str(e))
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("  🧪 Graph Database API Test Suite")
    print("=" * 70)
    print(f"\n📍 Testing API at: {BASE_URL}")
    print("⚠️  Make sure the server is running: python manage.py runserver\n")
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/nodes/all/", timeout=2)
        print("✅ Server is running and accessible\n")
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to server!")
        print("   Please start the server first: python manage.py runserver\n")
        return
    except Exception as e:
        print(f"❌ ERROR: {e}\n")
        return
    
    # Run all tests
    tests = [
        test_get_node_by_id,
        test_get_nodes_by_name,
        test_get_nodes_by_label,
        test_get_nodes_by_city,
        test_get_nodes_by_status,
        test_get_all_nodes,
        test_get_node_by_id_direct,
        test_invalid_field,
        test_node_not_found,
        test_response_structure
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test in tests:
        if test():
            passed_tests += 1
    
    # Print summary
    print_section("Test Summary")
    print(f"\n✅ Passed: {passed_tests}/{total_tests}")
    print(f"❌ Failed: {total_tests - passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("\n🎉 All tests passed! The API is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
    
    print("\n" + "=" * 70)
    print("\n💡 Next Steps:")
    print("   1. Open Swagger UI: http://127.0.0.1:8000/swagger/")
    print("   2. Try the interactive API documentation")
    print("   3. Read EXAMPLES.md for more usage examples")
    print("\n")

if __name__ == "__main__":
    main()
