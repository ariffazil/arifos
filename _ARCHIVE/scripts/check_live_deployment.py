#!/usr/bin/env python3
"""Check aaamcp.arif-fazil.com deployment status"""

import socket
import sys

def check_dns():
    """Check if DNS is configured"""
    print("=" * 60)
    print("CHECKING DNS CONFIGURATION")
    print("=" * 60)
    
    try:
        result = socket.gethostbyname_ex("aaamcp.arif-fazil.com")
        print(f"[OK] DNS Resolved: {result}")
        return True
    except socket.gaierror as e:
        print(f"[FAIL] DNS Not Found: {e}")
        print("\n[FIX] Add CNAME record in Cloudflare:")
        print("   Type: CNAME")
        print("   Name: aaamcp")
        print("   Value: x8ndjhgc.up.railway.app")
        return False

def check_http():
    """Check if HTTP is responding"""
    print("\n" + "=" * 60)
    print("CHECKING HTTP ENDPOINTS")
    print("=" * 60)
    
    import urllib.request
    import ssl
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    endpoints = [
        ("https://aaamcp.arif-fazil.com/", "Root"),
        ("https://aaamcp.arif-fazil.com/health", "Health"),
    ]
    
    results = []
    for url, name in endpoints:
        try:
            req = urllib.request.Request(url, method='GET')
            req.add_header('User-Agent', 'Mozilla/5.0')
            with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
                body = resp.read().decode('utf-8')[:200]
                print(f"[OK] {name}: HTTP {resp.status}")
                print(f"     Response: {body}...")
                results.append(True)
        except Exception as e:
            print(f"[FAIL] {name}: {type(e).__name__}")
            results.append(False)
    
    return all(results)

def main():
    print("aaamcp.arif-fazil.com Deployment Check")
    print("=" * 60)
    
    dns_ok = check_dns()
    
    if dns_ok:
        http_ok = check_http()
        if http_ok:
            print("\n[PASS] ALL CHECKS PASSED! Site is working.")
            return 0
        else:
            print("\n[WARN] DNS works but HTTP failed.")
            print("       Check Railway logs: railway logs")
            return 1
    else:
        print("\n[ACTION] DNS not configured. Follow the fix above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
