import hashlib
import requests

def check_password_leak(password: str) -> int:
    """
    Check if a password has been leaked using the Have I Been Pwned API (K-Anonymity).
    Returns the leak count if leaked, 0 otherwise.
    """
    if not password:
        return 0

    # 1. Hash the password using SHA-1 and convert to uppercase
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    
    # 2. Split the hash into the first 5 characters (prefix) and the rest (suffix)
    hash_prefix = sha1_hash[:5]
    hash_suffix = sha1_hash[5:]
    
    # 3. Query the API with only the first 5 characters of the hash
    url = f"https://api.pwnedpasswords.com/range/{hash_prefix}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return 0
            
        # 4. Parse the response lines (Format: SUFFIX:COUNT)
        lines = response.text.splitlines()
        for line in lines:
            target_suffix, count_str = line.split(':')
            # 5. Check if the suffix matches our local memory hash's suffix
            if target_suffix == hash_suffix:
                return int(count_str)
                
    except Exception:
        return 0

    return 0

# ==========================================
# Terminal Shooting Test Code (CONSOLE ONLY)
# ==========================================
if __name__ == "__main__":
    # 1. Hardcoded test password known to be leaked millions of times globally
    test_pw = "password123!"
    
    print("\n[정보] K-익명성 기반 보안 유출 이력 조회를 시작합니다...")
    print(f"[정보] 진단 대상 테스트 비밀번호: '{test_pw}'\n")
    
    # 2. Execute the backend K-Anonymity calculation core function
    leak_count = check_password_leak(test_pw)
    
    # 3. Print out clean and explicit response lines for your Korean localized GoPro shot
    if leak_count > 0:
        print(f"[🚨 경고] 이 비밀번호는 전 세계적으로 이미 약 {leak_count:,}번 유출된 이력이 있습니다!")
        print("[🚨 경고] 해당 암호를 사용하는 모든 사이트의 계정 정보를 즉시 변경할 것을 강력히 권장합니다.\n")
    else:
        print("[✅ 안전] 이 비밀번호는 데이터베이스에 기록된 보안 유출 내역이 없습니다.\n")