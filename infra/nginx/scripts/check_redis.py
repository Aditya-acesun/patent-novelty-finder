"""
Phase 1: Redis Health Check
Validates Redis is alive and Celery broker is reachable.
Usage: python scripts/check_redis.py
"""

import os
import sys
import redis


REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


def check_redis():
    print(f"\n🔌 Connecting to Redis at {REDIS_URL}...")
    try:
        r = redis.from_url(REDIS_URL, socket_connect_timeout=5)
        pong = r.ping()
        if pong:
            print("✅ Redis PING → PONG")
        
        # Write and read a test key
        r.set("pnf:health_check", "ok", ex=60)
        val = r.get("pnf:health_check")
        print(f"✅ Redis read/write OK → {val.decode()}")

        # Check memory info
        info = r.info("memory")
        used_mb = info["used_memory_human"]
        print(f"✅ Redis memory used: {used_mb}")

        print("\n✅ Redis is healthy — Celery broker ready\n")

    except redis.ConnectionError as e:
        print(f"❌ Redis connection failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Redis error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    check_redis()
