import streamlit as st
import time
import random
from io import BytesIO

# --- 1. 核心相容性修復 ---
def safe_rerun():
    """自動判斷並執行重整"""
    try:
        st.rerun()
    except AttributeError:
        try:
            st.experimental_rerun()
        except:
            st.stop()

def safe_play_audio(text):
    """語音播放安全模式"""
    try:
        from gtts import gTTS
        # 使用印尼語 (id) 發音
        tts = gTTS(text=text, lang='id')
        fp = BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')
    except Exception as e:
        st.caption(f"🔇 (語音生成暫時無法使用)")

# --- 0. 系統配置 ---
st.set_page_config(page_title="Unit 21: O Lalosidan", page_icon="🪑", layout="centered")

# --- CSS 美化 (居家木質調) ---
st.markdown("""
    <style>
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .source-tag { font-size: 12px; color: #aaa; text-align: right; font-style: italic; }
    
    /* 單字卡 */
    .word-card {
        background: linear-gradient(135deg, #EFEBE9 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
        border-bottom: 4px solid #795548;
    }
    .emoji-icon { font-size: 48px; margin-bottom: 10px; }
    .amis-text { font-size: 22px; font-weight: bold; color: #5D4037; }
    .chinese-text { font-size: 16px; color: #7f8c8d; }
    
    /* 句子框 */
    .sentence-box {
        background-color: #D7CCC8;
        border-left: 5px solid #8D6E63;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }

    /* 按鈕 */
    .stButton>button {
        width: 100%; border-radius: 12px; font-size: 20px; font-weight: 600;
        background-color: #BCAAA4; color: #3E2723; border: 2px solid #795548; padding: 12px;
    }
    .stButton>button:hover { background-color: #A1887F; border-color: #5D4037; }
    .stProgress > div > div > div > div { background-color: #795548; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 資料庫 (Unit 21: User Final Corrected) ---
vocab_data = [
    {"amis": "Loma'", "chi": "家", "icon": "🏠", "source": "CSV Row 328"},
    {"amis": "'Anengan", "chi": "椅子 / 座位", "icon": "🪑", "source": "CSV Row 1846"},
    {"amis": "Cokoy", "chi": "桌子", "icon": "🔲", "source": "CSV Row 1940"},
    {"amis": "Tatakel", "chi": "床鋪", "icon": "🛏️", "source": "CSV Row 1176"},
    {"amis": "Kaysing", "chi": "碗", "icon": "🥣", "source": "CSV Row 589"},
    {"amis": "Impic", "chi": "鉛筆", "icon": "✏️", "source": "CSV Row 742"},
    {"amis": "Fawahan", "chi": "門", "icon": "🚪", "source": "CSV Row 731"},
    {"amis": "Sasingaran", "chi": "窗戶", "icon": "🪟", "source": "CSV Row 4419"},
    {"amis": "Dangah", "chi": "鍋子", "icon": "🥘", "source": "User Fix"}, # 修正
    {"amis": "Tatipelok", "chi": "紙", "icon": "📄", "source": "CSV Row 4841"},
    {"amis": "Tingwa", "chi": "電話", "icon": "☎️", "source": "CSV Row 6031"},
    {"amis": "Sasing", "chi": "照片", "icon": "🖼️", "source": "CSV Row 651"},
    {"amis": "Dawdaw", "chi": "燈", "icon": "💡", "source": "User Fix"}, # 修正
    {"amis": "Tilifi", "chi": "電視", "icon": "📺", "source": "User Fix"}, # 修正
]

# --- 句子庫 (7句: 嚴格源自 CSV + User Fix) ---
sentences = [
    {"amis": "Awa ko loma' no-ni a wawa.", "chi": "這個小孩沒有家。", "icon": "🏠", "source": "CSV Row 328"},
    {"amis": "O sa-ka-i-hacowa ko-ya a kaysing?", "chi": "那個碗是要用在何時的？", "icon": "🥣", "source": "CSV Row 589"},
    {"amis": "Pasi-cowa-en ko-ni a fawah-an?", "chi": "這道門要朝向哪裡？", "icon": "🚪", "source": "CSV Row 731"},
    {"amis": "O ka-lo-maan ni Panay ko-ra a impic?", "chi": "那支鉛筆是被Panay當成什麼？", "icon": "✏️", "source": "CSV Row 742"},
    {"amis": "Maro' kamo i 'anengan.", "chi": "你們坐在椅子上。", "icon": "🪑", "source": "CSV Row 1846"},
    {"amis": "O ma-lo-tatakel kona sapad.", "chi": "這木板要做成床鋪。", "icon": "🛏️", "source": "CSV Row 1176"},
    {"amis": "Mi-nengneng to tilifi.", "chi": "看電視。", "icon": "📺", "source": "User Fix: Tilifi"},
]

# --- 3. 隨機題庫 (User Fix Verified) ---
raw_quiz_pool = [
    {
        "q": "Awa ko loma' no-ni a wawa.",
        "audio": "Awa ko loma' no-ni a wawa",
        "options": ["這個小孩沒有家", "這個小孩在學校", "這個小孩有錢"],
        "ans": "這個小孩沒有家",
        "hint": "Loma' 是家"
    },
    {
        "q": "Pasi-cowa-en ko-ni a fawah-an?",
        "audio": "Pasi-cowa-en ko-ni a fawah-an",
        "options": ["這道門要朝向哪裡？", "這扇窗戶要開嗎？", "這個人要去哪裡？"],
        "ans": "這道門要朝向哪裡？",
        "hint": "Fawah-an 是門"
    },
    {
        "q": "單字測驗：Cokoy",
        "audio": "Cokoy",
        "options": ["桌子", "椅子", "床"],
        "ans": "桌子",
        "hint": "吃飯寫字用的平面"
    },
    {
        "q": "單字測驗：'Anengan",
        "audio": "'Anengan",
        "options": ["椅子/座位", "地板", "桌子"],
        "ans": "椅子/座位",
        "hint": "坐著的器具"
    },
    {
        "q": "單字測驗：Impic",
        "audio": "Impic",
        "options": ["鉛筆", "書", "紙"],
        "ans": "鉛筆",
        "hint": "寫字的工具"
    },
    {
        "q": "單字測驗：Dangah",
        "audio": "Dangah",
        "options": ["鍋子", "碗", "湯匙"],
        "ans": "鍋子",
        "hint": "煮飯用的 Dangah"
    },
    {
        "q": "單字測驗：Dawdaw",
        "audio": "Dawdaw",
        "options": ["燈", "電視", "電話"],
        "ans": "燈",
        "hint": "發光的 Dawdaw"
    },
     {
        "q": "單字測驗：Tilifi",
        "audio": "Tilifi",
        "options": ["電視", "電話", "電影"],
        "ans": "電視",
        "hint": "用看的 Tilifi"
    }
]

# --- 4. 狀態初始化 (洗牌邏輯) ---
if 'init' not in st.session_state:
    st.session_state.score = 0
    st.session_state.current_q_idx = 0
    st.session_state.quiz_id = str(random.randint(1000, 9999))
    
    # 抽題與洗牌
    selected_questions = random.sample(raw_quiz_pool, 3)
    final_questions = []
    for q in selected_questions:
        q_copy = q.copy()
        shuffled_opts = random.sample(q['options'], len(q['options']))
        q_copy['shuffled_options'] = shuffled_opts
        final_questions.append(q_copy)
        
    st.session_state.quiz_questions = final_questions
    st.session_state.init = True

# --- 5. 主介面 ---
st.markdown("<h1 style='text-align: center; color: #5D4037;'>Unit 21: O Lalosidan</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>家具與生活用品 (User Corrected)</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📚 詞彙與句型", "🎲 隨機挑戰"])

# === Tab 1: 學習模式 ===
with tab1:
    st.subheader("📝 核心單字")
    col1, col2 = st.columns(2)
    for i, word in enumerate(vocab_data):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="word-card">
                <div class="emoji-icon">{word['icon']}</div>
                <div class="amis-text">{word['amis']}</div>
                <div class="chinese-text">{word['chi']}</div>
                <div class="source-tag">src: {word['source']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔊 聽發音", key=f"btn_vocab_{i}"):
                safe_play_audio(word['amis'])

    st.markdown("---")
    st.subheader("🗣️ 實用句型")
    for i, s in enumerate(sentences):
        st.markdown(f"""
        <div class="sentence-box">
            <div style="font-size: 20px; font-weight: bold; color: #4E342E;">{s['icon']} {s['amis']}</div>
            <div style="font-size: 16px; color: #555; margin-top: 5px;">{s['chi']}</div>
            <div class="source-tag">src: {s['source']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"▶️ 播放句型", key=f"btn_sent_{i}"):
            safe_play_audio(s['amis'])

# === Tab 2: 隨機挑戰模式 ===
with tab2:
    st.markdown("### 🎲 隨機評量")
    
    if st.session_state.current_q_idx < len(st.session_state.quiz_questions):
        q_data = st.session_state.quiz_questions[st.session_state.current_q_idx]
        
        st.progress((st.session_state.current_q_idx) / 3)
        st.markdown(f"**Question {st.session_state.current_q_idx + 1} / 3**")
        
        st.markdown(f"### {q_data['q']}")
        if q_data['audio']:
            if st.button("🎧 播放題目音檔", key=f"btn_audio_{st.session_state.current_q_idx}"):
                safe_play_audio(q_data['audio'])
        
        # 使用洗牌後的選項
        unique_key = f"q_{st.session_state.quiz_id}_{st.session_state.current_q_idx}"
        user_choice = st.radio("請選擇正確答案：", q_data['shuffled_options'], key=unique_key)
        
        if st.button("送出答案", key=f"btn_submit_{st.session_state.current_q_idx}"):
            if user_choice == q_data['ans']:
                st.balloons()
                st.success("🎉 答對了！")
                time.sleep(1)
                st.session_state.score += 100
                st.session_state.current_q_idx += 1
                safe_rerun()
            else:
                st.error(f"不對喔！提示：{q_data['hint']}")
                
    else:
        st.progress(1.0)
        st.markdown(f"""
        <div style='text-align: center; padding: 30px; background-color: #D7CCC8; border-radius: 20px; margin-top: 20px;'>
            <h1 style='color: #5D4037;'>🏆 挑戰成功！</h1>
            <h3 style='color: #333;'>本次得分：{st.session_state.score}</h3>
            <p>你已經認識這些生活用品了！</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 再來一局 (重新抽題)", key="btn_restart"):
            st.session_state.score = 0
            st.session_state.current_q_idx = 0
            st.session_state.quiz_id = str(random.randint(1000, 9999))
            
            new_questions = random.sample(raw_quiz_pool, 3)
            final_qs = []
            for q in new_questions:
                q_copy = q.copy()
                shuffled_opts = random.sample(q['options'], len(q['options']))
                q_copy['shuffled_options'] = shuffled_opts
                final_qs.append(q_copy)
            
            st.session_state.quiz_questions = final_qs
            safe_rerun()
