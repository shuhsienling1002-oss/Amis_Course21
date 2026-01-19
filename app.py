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
st.set_page_config(page_title="Unit 20: O 'Aadopen", page_icon="🐾", layout="centered")

# --- CSS 美化 (大地與森林色系) ---
st.markdown("""
    <style>
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .source-tag { font-size: 12px; color: #aaa; text-align: right; font-style: italic; }
    
    /* 單字卡 */
    .word-card {
        background: linear-gradient(135deg, #E8F5E9 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
        border-bottom: 4px solid #43A047;
    }
    .emoji-icon { font-size: 48px; margin-bottom: 10px; }
    .amis-text { font-size: 22px; font-weight: bold; color: #2E7D32; }
    .chinese-text { font-size: 16px; color: #7f8c8d; }
    
    /* 句子框 */
    .sentence-box {
        background-color: #F1F8E9;
        border-left: 5px solid #81C784;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }

    /* 按鈕 */
    .stButton>button {
        width: 100%; border-radius: 12px; font-size: 20px; font-weight: 600;
        background-color: #C8E6C9; color: #1B5E20; border: 2px solid #43A047; padding: 12px;
    }
    .stButton>button:hover { background-color: #A5D6A7; border-color: #2E7D32; }
    .stProgress > div > div > div > div { background-color: #43A047; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 資料庫 (Unit 20: 全新單字) ---
vocab_data = [
    {"amis": "'Aadopen", "chi": "動物", "icon": "🐾", "source": "New: Animal"},
    {"amis": "Waco", "chi": "狗", "icon": "🐕", "source": "New: Dog"},
    {"amis": "Posi", "chi": "貓", "icon": "🐈", "source": "New: Cat"},
    {"amis": "Fafoy", "chi": "豬", "icon": "🐖", "source": "New: Pig"},
    {"amis": "Kolong", "chi": "牛", "icon": "🐂", "source": "New: Buffalo/Cow"},
    {"amis": "Siri", "chi": "羊", "icon": "🐐", "source": "New: Goat"},
    {"amis": "Ayam", "chi": "鳥", "icon": "🐦", "source": "New: Bird"},
    {"amis": "'Oney", "chi": "蛇", "icon": "🐍", "source": "New: Snake"},
    {"amis": "Lotong", "chi": "猴子", "icon": "🐒", "source": "New: Monkey"},
    {"amis": "Karang", "chi": "螃蟹", "icon": "🦀", "source": "New: Crab"},
]

sentences = [
    {"amis": "Ciwaco kiso?", "chi": "你有養狗嗎？(你有狗嗎？)", "icon": "🐕", "source": "Ci- (Have) + Waco"},
    {"amis": "Tata'ang ko fafoy.", "chi": "豬很大。", "icon": "🐖", "source": "Tata'ang (Big) + Fafoy"},
    {"amis": "I omah ko kolong.", "chi": "牛在田裡。", "icon": "🐂", "source": "Unit 13 Review"},
    {"amis": "Maolah ko posi a mafoti'.", "chi": "貓喜歡睡覺。", "icon": "🐈", "source": "Unit 12 + Unit 17 Review"},
    {"amis": "Kohecalay ko ayam.", "chi": "那隻鳥是白色的。", "icon": "🕊️", "source": "Unit 19 Review"},
]

# --- 3. 隨機題庫 (定義) ---
raw_quiz_pool = [
    {
        "q": "Ciwaco kiso?",
        "audio": "Ciwaco kiso",
        "options": ["你有狗嗎？", "你有貓嗎？", "你有錢嗎？"],
        "ans": "你有狗嗎？",
        "hint": "Waco 是狗"
    },
    {
        "q": "Tata'ang ko fafoy.",
        "audio": "Tata'ang ko fafoy",
        "options": ["豬很大", "豬很小", "豬很瘦"],
        "ans": "豬很大",
        "hint": "Fafoy 是豬"
    },
    {
        "q": "I omah ko kolong.",
        "audio": "I omah ko kolong",
        "options": ["牛在田裡", "羊在山上", "鳥在天上"],
        "ans": "牛在田裡",
        "hint": "Kolong 是牛"
    },
    {
        "q": "單字測驗：Posi",
        "audio": "Posi",
        "options": ["貓", "狗", "豬"],
        "ans": "貓",
        "hint": "喵喵叫的動物"
    },
    {
        "q": "單字測驗：'Oney",
        "audio": "'Oney",
        "options": ["蛇", "猴子", "鳥"],
        "ans": "蛇",
        "hint": "沒有腳的動物"
    },
    {
        "q": "單字測驗：Siri",
        "audio": "Siri",
        "options": ["羊", "牛", "馬"],
        "ans": "羊",
        "hint": "咩咩叫的動物"
    },
    {
        "q": "「猴子」的阿美語怎麼說？",
        "audio": None,
        "options": ["Lotong", "Karang", "Ayam"],
        "ans": "Lotong",
        "hint": "喜歡爬樹的"
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
st.markdown("<h1 style='text-align: center; color: #2E7D32;'>Unit 20: O 'Aadopen</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>動物 (New Vocabulary Only)</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📚 詞彙與句型", "🎲 隨機挑戰"])

# === Tab 1: 學習模式 ===
with tab1:
    st.subheader("📝 核心單字 (New)")
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
            <div style="font-size: 20px; font-weight: bold; color: #1B5E20;">{s['icon']} {s['amis']}</div>
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
        <div style='text-align: center; padding: 30px; background-color: #C8E6C9; border-radius: 20px; margin-top: 20px;'>
            <h1 style='color: #1B5E20;'>🏆 挑戰成功！</h1>
            <h3 style='color: #333;'>本次得分：{st.session_state.score}</h3>
            <p>你已經認識這些動物了！</p>
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
