# test_tools.py
"""
Test script for Weekend Wizard MCP tools.
Tests all 6 tools: jokes, weather, books, holidays, dogs, trivia.
"""

import http.client
import json
import requests
import html
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def serper_search(query: str, num_results: int = 3) -> dict:
    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({"q": query, "num": num_results})
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/search", payload, headers)
    res = conn.getresponse()
    data = res.read()
    conn.close()
    return json.loads(data.decode("utf-8"))

def test_jokes():
    print("\n" + "="*60)
    print("[JOKES] TESTING: Tell a joke")
    print("="*60)
    try:
        result = serper_search("funny clean joke of the day", 3)
        organic = result.get("organic", [])
        print(f"Count: {len(organic)}")
        return {"status": "SUCCESS"}
    except Exception as e:
        print(f"Error: {e}")
        return {"status": "ERROR", "error": str(e)}

def test_weather():
    print("\n" + "="*60)
    print("[WEATHER] TESTING: Weather search")
    print("="*60)
    try:
        result = serper_search("current weather in New York today", 2)
        print(f"Results for NYC: {len(result.get('organic', []))}")
        return {"status": "SUCCESS"}
    except Exception as e:
        print(f"Error: {e}")
        return {"status": "ERROR"}

def test_books():
    print("\n" + "="*60)
    print("[BOOKS] TESTING: Book recommendations")
    print("="*60)
    try:
        result = serper_search("best mystery thriller books 2024", 3)
        print(f"Results: {len(result.get('organic', []))}")
        return {"status": "SUCCESS"}
    except Exception as e:
        print(f"Error: {e}")
        return {"status": "ERROR"}

def test_holidays():
    print("\n" + "="*60)
    print("[HOLIDAYS] TESTING: Holiday suggestions")
    print("="*60)
    try:
        result = serper_search("top holiday activities in Bali", 5)
        print(f"Results for Bali: {len(result.get('organic', []))}")
        return {"status": "SUCCESS"}
    except Exception as e:
        print(f"Error: {e}")
        return {"status": "ERROR"}

def test_dogs():
    print("\n" + "="*60)
    print("[DOGS] TESTING: Random dog photo")
    print("="*60)
    try:
        r = requests.get("https://dog.ceo/api/breeds/image/random", timeout=10)
        r.raise_for_status()
        url = r.json().get("message")
        print(f"Dog URL: {url}")
        return {"status": "SUCCESS"}
    except Exception as e:
        print(f"Error: {e}")
        return {"status": "ERROR"}

def test_trivia():
    print("\n" + "="*60)
    print("[TRIVIA] TESTING: Trivia question")
    print("="*60)
    try:
        r = requests.get("https://opentdb.com/api.php?amount=1&type=multiple", timeout=10)
        r.raise_for_status()
        data = r.json().get("results", [])
        if data:
            print(f"Category: {data[0].get('category')}")
            print(f"Question: {html.unescape(data[0].get('question'))}")
            return {"status": "SUCCESS"}
        return {"status": "ERROR", "error": "No results"}
    except Exception as e:
        print(f"Error: {e}")
        return {"status": "ERROR"}

def main():
    print("\n" + "#"*60)
    print("#  WEEKEND WIZARD - COMPREHENSIVE TEST SUITE")
    print(f"#  Run Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("#"*60)
    
    results = {"tests": {}}
    results["tests"]["jokes"] = test_jokes()
    results["tests"]["weather"] = test_weather()
    results["tests"]["books"] = test_books()
    results["tests"]["holidays"] = test_holidays()
    results["tests"]["dogs"] = test_dogs()
    results["tests"]["trivia"] = test_trivia()
    
    print("\n" + "="*60)
    print("[SUMMARY] TEST RESULTS")
    print("="*60)
    passed = sum(1 for t in results["tests"].values() if t["status"] == "SUCCESS")
    for name, result in results["tests"].items():
        print(f"  [{'PASS' if result['status'] == 'SUCCESS' else 'FAIL'}] {name}")
    print(f"\nTotal: {passed}/6 tests passed")

if __name__ == "__main__":
    main()
