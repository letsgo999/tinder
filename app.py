import streamlit as st
import random
from PIL import Image
import io
import base64

def init_session_state():
    if 'profiles' not in st.session_state:
        st.session_state.profiles = []
    if 'current_pair' not in st.session_state:
        st.session_state.current_pair = None
    if 'game_active' not in st.session_state:
        st.session_state.game_active = True

def add_profile(uploaded_file):
    if uploaded_file is not None:
        # 이미지 파일 처리
        image = Image.open(uploaded_file)
        # 이미지 크기 표준화 (선택사항)
        image = image.resize((300, 300))
        # 이미지를 바이트로 변환
        buf = io.BytesIO()
        image.save(buf, format='PNG')
        image_bytes = buf.getvalue()
        # Base64로 인코딩
        encoded_image = base64.b64encode(image_bytes).decode()
        
        # 프로필 추가
        st.session_state.profiles.append({
            'id': len(st.session_state.profiles),
            'image': encoded_image,
            'name': uploaded_file.name
        })

def select_random_pair():
    if len(st.session_state.profiles) >= 2:
        profiles = st.session_state.profiles
        first = random.choice(profiles)
        second = random.choice([p for p in profiles if p['id'] != first['id']])
        st.session_state.current_pair = [first, second]

def main():
    st.set_page_config(page_title="프로필 비교 게임", layout="wide")
    
    # 세션 상태 초기화
    init_session_state()
    
    # 제목
    st.title("프로필 비교 게임")
    
    # 파일 업로더
    st.header("프로필 사진 업로드")
    uploaded_file = st.file_uploader("이미지를 선택하세요", type=['png', 'jpg', 'jpeg'])
    if uploaded_file:
        add_profile(uploaded_file)
    
    # 업로드된 프로필 개수 표시
    st.write(f"업로드된 프로필: {len(st.session_state.profiles)}개")
    
    # 게임 영역
    if st.session_state.game_active and len(st.session_state.profiles) >= 2:
        if st.session_state.current_pair is None:
            select_random_pair()
            
        # 두 프로필 이미지 나란히 표시
        if st.session_state.current_pair:
            col1, col2 = st.columns(2)
            
            # 첫 번째 프로필
            with col1:
                if st.button("왼쪽 선택", key="left"):
                    select_random_pair()
                st.image(
                    f"data:image/png;base64,{st.session_state.current_pair[0]['image']}", 
                    use_column_width=True
                )
            
            # 두 번째 프로필
            with col2:
                if st.button("오른쪽 선택", key="right"):
                    select_random_pair()
                st.image(
                    f"data:image/png;base64,{st.session_state.current_pair[1]['image']}", 
                    use_column_width=True
                )
    
    # Exit 버튼
    if st.button("Exit"):
        st.session_state.game_active = False
        st.session_state.current_pair = None
        st.experimental_rerun()

if __name__ == "__main__":
    main()
