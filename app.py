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

# --- CSS 美化 (居家溫馨色調) ---
st.markdown("""
    <style>
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .source-tag { font-size: 12px; color: #aaa; text-align: right; font-style: italic; }
    
    /* 單字卡 */
    .word-card {
        background: linear-gradient(135deg, #D7CCC8 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
        border-bottom: 4px solid #8D6E63;
    }
    .emoji-icon { font-size: 48px; margin-bottom: 10px; }
    .amis-text { font-size: 22px; font-weight: bold; color: #5D4037; }
    .chinese-text { font-size: 16px; color: #7f8c8d; }
    .morph-tag { 
        background-color: #EFEBE9; color: #5D4037; 
        padding: 2px 8px; border-radius: 10px; font-size: 12px; font-weight: bold;
        display: inline-block; margin-top: 5px;
    }
    
    /* 句子框 */
    .sentence-box {
        background-color: #EFEBE9;
        border-left: 5px solid #A1887F;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }

    /* 按鈕 */
    .stButton>button {
        width: 100%; border-radius: 12px; font-size: 20px; font-weight: 600;
        background-color: #D7CCC8; color: #4E342E; border: 2px solid #8D6E63; padding: 12px;
    }
    .stButton>button:hover { background-color: #BCAAA4; border-color: #5D4037; }
    .stProgress > div > div > div > div { background-color: #8D6E63; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 資料庫 (Unit 21: 14個單字) ---
vocab_data = [
    {"amis": "Lalosidan", "chi": "物品 / 器具", "icon": "📦", "source": "Moedict", "morph": "Root: Losid"},
    {"amis": "Loma'", "chi": "家 / 房子", "icon": "🏠", "source": "Row 328", "morph": "Root"},
    {"amis": "Takar", "chi": "桌子", "icon": "🔲", "source": "Moedict", "morph": "Root"},
    {"amis": "Anan", "chi": "椅子", "icon": "🪑", "source": "Moedict", "morph": "Root"},
    {"amis": "Kamaro'an", "chi": "座位 / 住處", "icon": "🧘", "source": "Moedict", "morph": "Ka-maro'-an (坐的地方)"},
    {"amis": "Kaysing", "chi": "碗", "icon": "🥣", "source": "Row 589", "morph": "Root"},
    {"amis": "Safing", "chi": "掃把", "icon": "🧹", "source": "Moedict", "morph": "Root"},
    {"amis": "Impic", "chi": "鉛筆", "icon": "✏️", "source": "Row 742", "morph": "Loan: Enpitsu"},
    {"amis": "Sapitilid", "chi": "筆 (寫字的工具)", "icon": "🖊️", "source": "Grammar", "morph": "Sa-pi-tilid (用來寫的)"},
    {"amis": "Tilid", "chi": "書 / 字", "icon": "📖", "source": "Row 318", "morph": "Root"},
    {"amis": "Tilibi", "chi": "電視", "icon": "📺", "source": "Loan", "morph": "Loan: TV"},
    {"amis": "Dingwa", "chi": "電話", "icon": "☎️", "source": "Loan", "morph": "Loan: Denwa"},
    {"amis": "Panan", "chi": "門", "icon": "🚪", "source": "Moedict", "morph": "Root"},
    {"amis": "Sasing", "chi": "照片 / 照相", "icon": "🖼️", "source": "Moedict", "morph": "Root"},
]

# --- 句子庫 (7句: 優先使用 data.csv) ---
sentences = [
    {"amis": "Awa ko loma' noni a wawa.", "chi": "這個小孩沒有家。", "icon": "🏠", "source": "Row 328"},
    {"amis": "O saka-i-hacowa koya a kaysing?", "chi": "那個碗是要用在何時的(工具)？", "icon": "🥣", "source": "Row 589"},
    {"amis": "O kalomaan ni Panay kora a impic?", "chi": "那支鉛筆是被Panay當成什麼(做什麼用的)？", "icon": "✏️", "source": "Row 742 (Modified)"},
    {"amis": "I cowa ko kamaro'an?", "chi": "座位在哪裡？", "icon": "🧘", "source": "Morph: Maro' -> Kamaro'an"},
    {"amis": "Minengneng to tilibi i loma'.", "chi": "在家看電視。", "icon": "📺", "source": "Basic"},
    {"amis": "Fangcal ko takar.", "chi": "桌子很漂亮。", "icon": "✨", "source": "Structure: Fangcal + Noun"},
    {"amis": "Cima ko mitiliday to dingwa?", "chi": "誰在打電話？(誰是寫電話的人?)", "icon": "☎️", "source": "Structure practice"},
]

# --- 3. 隨機題庫 (Moedict Verified) ---
raw_quiz_pool = [
    {
        "q": "Awa ko loma' noni a wawa.",
        "audio": "Awa ko loma' noni a wawa",
        "options": ["這個小孩沒有家", "這個小孩在學校", "這個小孩有錢"],
        "ans": "這個小孩沒有家",
        "hint": "Awa (沒有) + Loma' (家)"
    },
    {
        "q": "O saka-i-hacowa koya a kaysing?",
        "audio": "O saka-i-hacowa koya a kaysing",
        "options": ["那個碗是何時用的？", "那個碗是誰的？", "那個碗在哪裡？"],
        "ans": "那個碗是何時用的？",
        "hint": "Hacowa (何時) + Kaysing (碗)"
    },
    {
        "q": "O kalomaan ni Panay kora a impic?",
        "audio": "O kalomaan ni Panay kora a impic",
        "options": ["那支鉛筆是做什麼用的？", "那支鉛筆是誰的？", "那支鉛筆多少錢？"],
        "ans": "那支鉛筆是做什麼用的？",
        "hint": "Impic 是鉛筆 (Row 742)"
    },
    {
        "q": "單字測驗：Kamaro'an",
        "audio": "Kamaro'an",
        "options": ["座位/住處", "吃飯", "睡覺"],
        "ans": "座位/住處",
        "hint": "Ka-maro'-an (坐的地方)"
    },
    {
        "q": "單字測驗：Sapitilid",
        "audio": "Sapitilid",
        "options": ["筆(寫字工具)", "書", "橡皮擦"],
        "ans": "筆(寫字工具)",
        "hint": "Sa-pi-tilid (用來寫的)"
    },
    {
        "q": "單字測驗：Takar",
        "audio": "Takar",
        "options": ["桌子", "椅子", "床"],
        "ans": "桌子",
        "hint": "吃飯寫字用的平面"
    },
    {
        "q": "單字測驗：Anan",
        "audio": "Anan",
        "options": ["椅子", "桌子", "門"],
        "ans": "椅子",
        "hint": "坐著的器具"
    },
    {
        "q": "「家」的阿美語怎麼說？",
        "audio": None,
        "options": ["Loma'", "Omah", "Patiyamay"],
        "ans": "Loma'",
        "hint": "Row 328: Awa ko loma'..."
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
st.markdown("<p style='text-align: center; color: #666;'>家具與生活用品 (Household Items)</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📚 詞彙與句型", "🎲 隨機挑戰"])

# === Tab 1: 學習模式 ===
with tab1:
    st.subheader("📝 核心單字 (構詞分析)")
    col1, col2 = st.columns(2)
    for i, word in enumerate(vocab_data):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="word-card">
                <div class="emoji-icon">{word['icon']}</div>
                <div class="amis-text">{word['amis']}</div>
                <div class="chinese-text">{word['chi']}</div>
                <div class="morph-tag">{word['morph']}</div>
                <div class="source-tag">src: {word['source']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔊 聽發音", key=f"btn_vocab_{i}"):
                safe_play_audio(word['amis'])

    st.markdown("---")
    st.subheader("🗣️ 實用句型 (Data-Driven)")
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
