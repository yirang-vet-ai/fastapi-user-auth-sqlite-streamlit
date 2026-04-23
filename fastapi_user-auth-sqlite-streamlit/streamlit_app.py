import streamlit as st
import requests

st.set_page_config(page_title="FastAPI 인증 😊 API 테스트", layout="wide")

st.title("FastAPI 회원가입 · 로그인 테스트 화면")

base_url = st.text_input(
    "서버 주소 입력",
    value="http://127.0.0.1:8000"
)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("회원가입")

    reg_username = st.text_input("Username", key="reg_username")
    reg_email = st.text_input("Email", key="reg_email")
    reg_nickname = st.text_input("Nickname", key="reg_nickname")
    reg_password = st.text_input("Password", type="password", key="reg_password")

    if st.button("회원가입 실행"):
        url = f"{base_url}/register"
        payload = {
            "username": reg_username,
            "email": reg_email,
            "nickname": reg_nickname,
            "password": reg_password
        }

        try:
            response = requests.post(url, json=payload)
            st.write("상태 코드:", response.status_code)
            st.json(response.json())
        except Exception as e:
            st.error(f"오류 발생: {e}")

with col2:
    st.subheader("로그인")

    login_username_or_email = st.text_input("Username 또는 Email", key="login_id")
    login_password = st.text_input("Login Password", type="password", key="login_password")

    if st.button("로그인 실행"):
        url = f"{base_url}/login"
        payload = {
            "username_or_email": login_username_or_email,
            "password": login_password
        }

        try:
            response = requests.post(url, json=payload)
            st.write("상태 코드:", response.status_code)
            result = response.json()
            st.json(result)

            if response.status_code == 200 and "access_token" in result:
                st.session_state["access_token"] = result["access_token"]
        except Exception as e:
            st.error(f"오류 발생: {e}")

st.markdown("---")

st.subheader("사용자 조회")

user_id = st.text_input("조회할 사용자 ID", value="1")

col3, col4 = st.columns(2)

with col3:
    if st.button("전체 사용자 조회"):
        url = f"{base_url}/users"
        try:
            response = requests.get(url)
            st.write("상태 코드:", response.status_code)
            st.json(response.json())
        except Exception as e:
            st.error(f"오류 발생: {e}")

with col4:
    if st.button("특정 사용자 조회"):
        url = f"{base_url}/users/{user_id}"
        try:
            response = requests.get(url)
            st.write("상태 코드:", response.status_code)
            st.json(response.json())
        except Exception as e:
            st.error(f"오류 발생: {e}")

st.markdown("---")

st.subheader("비밀번호 변경")

change_user_key = st.text_input("비밀번호 변경 대상 사용자 ID", value="1")
current_password = st.text_input("현재 비밀번호", type="password", key="current_pw")
new_password = st.text_input("새 비밀번호", type="password", key="new_pw")

if st.button("비밀번호 변경 실행"):
    url = f"{base_url}/users/{change_user_key}/change-password"
    payload = {
        "current_password": current_password,
        "new_password": new_password
    }

    try:
        response = requests.post(url, json=payload)
        st.write("상태 코드:", response.status_code)
        st.json(response.json())
    except Exception as e:
        st.error(f"오류 발생: {e}")