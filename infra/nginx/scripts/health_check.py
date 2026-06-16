"""
Phase 1: Master Infrastructure Health Check
Validates all services are running correctly.
Usage: python scripts/health_check.py
"""

import sys
import urllib.request
import urllib.error
import json


SERVICES = [
    {
        "name": "Backend (Node/Express)",
        "url": "http://localhost:4000/api/health",
        "expect_key": "status",
        "expect_val": "ok",
    },
    {
        "name": "AI Service (FastAPI)",
        "url": "http://localhost:8000/health",
        "expect_key": "status",
        "expect_val": "ok",
    },
    {
        "name": "Qdrant Vector DB",
        "url": "http://localhost:6333/collections",
        "expect_key": "result",
        "expect_val": None,  # just check it responds
    },
    {
        "name": "Swagger Docs",
        "url": "http://localhost:4000/api/docs/",
        "expect_key": None,
        "expect_val": None,
    },
]


def check_service(service: dict) -> bool:
    name = service["name"]
    url = service["url"]
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "pnf-health-check"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            status = resp.status
            if service["expect_key"]:
                body = json.loads(resp.read().decode())
                if service["expect_val"]:
                    actual = body.get(service["expect_key"])
                    if actual != service["expect_val"]:
                        print(f"❌ {name} → unexpected value: {actual}")
                        return False
            print(f"✅ {name} → HTTP {status}")
            return True
    except urllib.error.URLError as e:
        print(f"❌ {name} → {e.reason}")
        return False
    except Exception as e:
        print(f"❌ {name} → {e}")
        return False


def main():
    print("\n" + "="*50)
    print("  Patent Novelty Finder — Infra Health Check")
    print("="*50 + "\n")

    results = []
    for service in SERVICES:
        ok = check_service(service)
        results.append(ok)

    print("\n" + "="*50)
    passed = sum(results)
    total = len(results)

    if passed == total:
        print(f"  ✅ ALL {total}/{total} SERVICES HEALTHY")
        print("  🚀 Ready for Phase 2 (Backend Auth)")
    else:
        print(f"  ⚠️  {passed}/{total} services healthy")
        print("  Fix the failing services before proceeding")

    print("="*50 + "\n")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
