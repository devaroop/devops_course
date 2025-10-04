#!/usr/bin/env python3
"""
Demo script for the Health API Service

This script demonstrates the functionality of the Health API Service
by making requests to all available endpoints and displaying the results.

Usage:
    python demo.py

Author: DevOps Course Student
Date: 2025-01-13
"""

import requests
import json
import time
from datetime import datetime


class HealthAPIDemo:
    """Demo class for testing the Health API Service."""
    
    def __init__(self, base_url="http://localhost:8000"):
        """
        Initialize the demo with the API base URL.
        
        Args:
            base_url (str): The base URL of the API service
        """
        self.base_url = base_url
        self.session = requests.Session()
    
    def test_connection(self):
        """Test if the API service is running."""
        try:
            response = self.session.get(f"{self.base_url}/", timeout=5)
            if response.status_code == 200:
                print("✅ API service is running")
                return True
            else:
                print(f"❌ API service returned status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Cannot connect to API service: {e}")
            return False
    
    def demo_root_endpoint(self):
        """Demonstrate the root endpoint."""
        print("\n" + "="*50)
        print("DEMO: Root Endpoint (GET /)")
        print("="*50)
        
        try:
            response = self.session.get(f"{self.base_url}/")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except Exception as e:
            print(f"Error: {e}")
    
    def demo_health_endpoint(self):
        """Demonstrate the health endpoint."""
        print("\n" + "="*50)
        print("DEMO: Health Endpoint (GET /health)")
        print("="*50)
        
        try:
            response = self.session.get(f"{self.base_url}/health")
        except Exception as e:
            print(f"Error: {e}")
            return
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Status: {data.get('status')}")
            print(f"Timestamp: {data.get('timestamp')}")
            
            if 'system_info' in data:
                system_info = data['system_info']
                print("\nSystem Information:")
                print(f"  Python Version: {system_info.get('python_version', 'N/A')[:50]}...")
                print(f"  Platform: {system_info.get('platform', 'N/A')}")
                print(f"  CPU Count: {system_info.get('cpu_count', 'N/A')}")
                print(f"  Memory Total: {system_info.get('memory_total', 'N/A'):,} bytes")
                print(f"  Memory Available: {system_info.get('memory_available', 'N/A'):,} bytes")
                print(f"  Disk Usage: {system_info.get('disk_usage', 'N/A')}%")
        else:
            print(f"Error Response: {response.text}")
    
    def demo_simple_health_endpoint(self):
        """Demonstrate the simple health endpoint."""
        print("\n" + "="*50)
        print("DEMO: Simple Health Endpoint (GET /health/simple)")
        print("="*50)
        
        try:
            response = self.session.get(f"{self.base_url}/health/simple")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except Exception as e:
            print(f"Error: {e}")
    
    def demo_performance_test(self):
        """Demonstrate performance by making multiple requests."""
        print("\n" + "="*50)
        print("DEMO: Performance Test (5 concurrent requests)")
        print("="*50)
        
        import threading
        import time
        
        results = []
        
        def make_request():
            start_time = time.time()
            try:
                response = self.session.get(f"{self.base_url}/health/simple")
                end_time = time.time()
                results.append({
                    'status_code': response.status_code,
                    'response_time': end_time - start_time,
                    'success': response.status_code == 200
                })
            except Exception as e:
                results.append({
                    'status_code': 0,
                    'response_time': 0,
                    'success': False,
                    'error': str(e)
                })
        
        # Create and start threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Display results
        successful_requests = [r for r in results if r['success']]
        failed_requests = [r for r in results if not r['success']]
        
        print(f"Total Requests: {len(results)}")
        print(f"Successful: {len(successful_requests)}")
        print(f"Failed: {len(failed_requests)}")
        
        if successful_requests:
            response_times = [r['response_time'] for r in successful_requests]
            avg_response_time = sum(response_times) / len(response_times)
            min_response_time = min(response_times)
            max_response_time = max(response_times)
            
            print(f"Average Response Time: {avg_response_time:.3f}s")
            print(f"Min Response Time: {min_response_time:.3f}s")
            print(f"Max Response Time: {max_response_time:.3f}s")
        
        if failed_requests:
            print("\nFailed Requests:")
            for i, result in enumerate(failed_requests):
                print(f"  Request {i+1}: {result.get('error', 'Unknown error')}")
    
    def demo_error_handling(self):
        """Demonstrate error handling with invalid endpoints."""
        print("\n" + "="*50)
        print("DEMO: Error Handling (Invalid Endpoint)")
        print("="*50)
        
        try:
            response = self.session.get(f"{self.base_url}/nonexistent")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
        except Exception as e:
            print(f"Error: {e}")
    
    def run_full_demo(self):
        """Run the complete demo."""
        print("🏥 Health API Service Demo")
        print("=" * 50)
        print(f"Testing API at: {self.base_url}")
        print(f"Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Test connection first
        if not self.test_connection():
            print("\n❌ Cannot proceed with demo. Please ensure the API service is running.")
            print("To start the API service, run: python main.py")
            return
        
        # Run all demos
        self.demo_root_endpoint()
        self.demo_health_endpoint()
        self.demo_simple_health_endpoint()
        self.demo_performance_test()
        self.demo_error_handling()
        
        print("\n" + "="*50)
        print("✅ Demo completed successfully!")
        print("="*50)


def main():
    """Main function to run the demo."""
    print("Starting Health API Service Demo...")
    print("Make sure the API service is running on http://localhost:8000")
    print("To start the service, run: python main.py")
    print()
    
    # Wait a moment for user to read
    time.sleep(2)
    
    demo = HealthAPIDemo()
    demo.run_full_demo()


if __name__ == "__main__":
    main()
