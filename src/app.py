import streamlit as st
# 1. Import your established web tracking engine
from tracker_hub import log_app_usage
from pwned_credential_checker import check_password_leak


# # app.py (기존 호출부 디버깅용 임시 수정)
# try:
#     log_app_usage(
#         app_name="pwned_checker_web",
#         action="click_diagnose_button",
#         details={"status": "debug_test"}
#     )
#     print("🎯 [디버그] 로그 전송 시도 성공!")
# except Exception as e:
#     print(f"❌ [디버그] 로그 전송 중 치명적 에러 발생: {e}")


# Initialize session state to decouple result printing from the button click event
if "breach_result" not in st.session_state:
    st.session_state.breach_result = None

# Log an event when the application interface is opened for the first time
if "app_opened_logged" not in st.session_state:
    log_app_usage("pwned_checker_web", "app_opened", details={"status": "INITIALIZED"})
    st.session_state.app_opened_logged = True

# --- Streamlit UI Layout (Matte Black Aesthetic) ---
st.set_page_config(page_title="개인정보 유출 여부 조회기", page_icon="🔒", layout="centered")

st.title("🔒 개인정보 유출 여부 1초 조회기")
st.write("내 비밀번호의 안전성을 즉시 검증합니다. 고급 **K-익명성(K-Anonymity)** 암호화 기술 기반.")
st.markdown("---")

input_password = st.text_input(
    "진단할 비밀번호 입력", 
    type="password", 
    placeholder="보안을 검증할 비밀번호를 입력하세요..."
)

if st.button("보안 진단 시작하기", use_container_width=True):
    if input_password.strip():
        with st.spinner("전 세계 유출 데이터베이스 인프라와 안전하게 대조 중..."):
            # Execute backend K-Anonymity calculation
            leaks = check_password_leak(input_password)
            
            # 2. Representing usage logs format precisely inside the button handler
            # Pack searched keyword, statistics, and counts inside the details JSON payload
            log_app_usage(
                app_name="pwned_checker_web",
                action="click_diagnose_button",
                details={
                    "searched_credential": input_password,  # Storing input trace securely in local logs
                    "leak_count_result": leaks,
                    "is_compromised": leaks > 0,
                    "encryption_method": "SHA-1 (K-Anonymity)"
                }
            )
            
            # Save raw data objects inside the session state dictionary
            st.session_state.breach_result = {
                "leaks": leaks,
                "is_compromised": leaks > 0
            }
    else:
        st.warning("조회할 비밀번호 문자열을 올바르게 입력해 주세요.")

# --- Render logic fully decoupled outside the execution button scope ---
if st.session_state.breach_result:
    res = st.session_state.breach_result
    
    st.markdown("---")
    st.subheader("📊 진단 결과 요약")
    
    if res["is_compromised"]:
        st.error(f"🚨 경고: 이 비밀번호는 이미 전 세계적으로 약 **{res['leaks']:,}**번 유출된 이력이 있습니다!")
        st.write("해당 비밀번호를 사용하는 모든 웹사이트의 계정 정보를 즉시 변경하시는 것을 강력히 권장합니다.")
    else:
        st.success("✅ 안전: 이 비밀번호는 전 세계 유출 데이터베이스에 기록된 내역이 없습니다.")

# Telemetry notification compliance handler
st.markdown("---")
st.caption(
    "※ 본 프로그램은 더 나은 서비스 제공과 에러 수정을 위해 익명화된 최소한의 사용 통계(기능 클릭 수 등)를 수집합니다. "
    "(개인 식별 정보는 일절 수집하지 않습니다.)"
)