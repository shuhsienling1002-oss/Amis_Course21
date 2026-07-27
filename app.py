import streamlit as st
import random
import json
import os  # 引入 OS 模組，用於物理檔案路徑防禦性偵測

# 🚀 新增：定義全域系統版本號 (每次更新只需修改這裡)
APP_VERSION = "v2.0.0 (Build 20260619)"

# ---- 1. 頁面佈局設定 (Code-CRF v9.0 運行時配置) ----
st.set_page_config(
    page_title="中高級認證",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---- 2. 自動適應雙模式的 CSS 設計 (UIUX-CRF v9.0 視覺熵減) ----
st.markdown("""
    <style>
    /* 核心題目卡片式容器：只有顯式宣告的卡片才會擁有此風格 */
    .quiz-card {
        background-color: var(--secondary-background-color);
        padding: 24px;
        border-radius: 16px;
        border: 1px solid rgba(128, 128, 128, 0.2);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-top: 15px;
        margin-bottom: 25px;
        transition: all 0.3s ease;
    }
    
    /* 標題與重點文字：使用亮眼且百搭的青色 */
    h1, h2, h3 {
        color: #0D9488 !important;
    }
    
    @media (prefers-color-scheme: dark) {
        h1, h2, h3 {
            color: #2DD4BF !important;
        }
    }
    
    .stMarkdown p {
        color: var(--text-color);
        opacity: 0.85;
    }
    
    /* 覆寫提示區塊與非必要組件的預設外框，強制清除視覺干擾 */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
    }
    
    /* 清除 segmented_control 和 radio 可能觸發的隱性原生區塊背景 */
    div[data-testid="stHorizontalBlock"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    /* 小字性質註記樣式 */
    .category-note {
        font-size: 13px !important;
        color: gray !important;
        margin-top: -10px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# ---- App 頂部導覽列 ----
st.title("🎓 中高級認證")
# 🛠️ 修正 1：對齊您截圖中的文字
st.caption("[請選擇練習平台]")

# ---- 第一層：五個主要選項 (導覽選單) ----
main_options = ["📋 認證考試說明", "🎧 聽力", "🗣️ 口說", "📖 閱讀", "✍️ 寫作"]
current_tab = st.segmented_control(
    "主選單導覽", 
    main_options, 
    default=None,  # 🚀 修正 2：設為 None，代表一進來「不預設選取任何頁面」，保持畫面純淨
    label_visibility="collapsed"
)

# ---- 🧠 跨頁面狀態解耦防腐層 ----
if "previous_tab" not in st.session_state:
    # 🚀 修正 3：初始狀態同步設為 None
    st.session_state.previous_tab = None

if st.session_state.previous_tab != current_tab:
    st.session_state.submitted = False
    st.session_state.audio_triggered = False
    if "writing_submitted" in st.session_state:
        st.session_state.writing_submitted = False
    
    # 使用 del 安全註銷屬性快取，徹底根除分頁切換時的隱性異常崩潰
    if "q_show_trans" in st.session_state:
        del st.session_state["q_show_trans"]
    if "q_show_ans" in st.session_state:
        del st.session_state["q_show_ans"]
    if "s_show_q_trans" in st.session_state:
        del st.session_state["s_show_q_trans"]
    if "s_show_q_amis" in st.session_state:
        del st.session_state["s_show_q_amis"]
    if "s_show_ans" in st.session_state:
        del st.session_state["s_show_ans"]
    if "q_input_text_cache" in st.session_state:
        del st.session_state["q_input_text_cache"]
    if "s_audio_triggered" in st.session_state:
        del st.session_state["s_audio_triggered"]
        
    st.session_state.previous_tab = current_tab
    st.rerun()

# ---- 3. 原始聽力題庫 (15題標準數據庫) ----
QUIZ_DATA = [
    {"id": 1, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-01.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["riyar", "'alo", "fanaw", "sa'owac"], "correct_text": "riyar"},
    {"id": 2, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-02.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["korkor", "rohayan", "romakat", "rotarot"], "correct_text": "romakat"},
    {"id": 3, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-03.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["hadhad", "hakhak", "hawan", "hafay"], "correct_text": "hafay"},
    {"id": 4, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-04.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["tefo'", "'okoy", "tafokod", "tafolod"], "correct_text": "tafokod"},
    {"id": 5, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-05.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["fakar", "tayhi", "pitaw", "tarakar"], "correct_text": "pitaw"},
    {"id": 6, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-06.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["sariri'", "riri'", "siri", "riyar"], "correct_text": "siri"},
    {"id": 7, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-07.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["koleto", "lokot", "kewaw", "kakorot"], "correct_text": "koleto"},
    {"id": 8, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-08.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["siwoy", "kodasing", "konga", "damay"], "correct_text": "konga"},
    {"id": 9, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-09.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["mali'", "tikami", "tilifi", "pawli"], "correct_text": "tilifi"},
    {"id": 10, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-10.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["picakay", "pitangtang", "picaliw", "pafeli'"], "correct_text": "picakay"},
    {"id": 11, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-11.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["'olaw", "'alo", "fao", "tao"], "correct_text": "tao"},
    {"id": 12, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-12.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["rorang", "kolong", "lotong", "ekong"], "correct_text": "lotong"},
    {"id": 13, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-13.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["Halitamako", "Haliradiw", "Haliepah", "Hali'ecaw"], "correct_text": "Haliepah"},
    {"id": 14, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-14.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["dafak", "a'ayad", "dadaya", "kamaya"], "correct_text": "dadaya"},
    {"id": 15, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-15.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["sioy", "simal", "sinafel", "simico"], "correct_text": "sinafel"}
]

# ---- 第二層：根據選擇顯示對應架構 ----

# 1. 📋 認證考試說明頁面
if current_tab == "📋 認證考試說明":
    st.subheader("📋 認證考試說明")
    st.divider()
    
    with st.expander("1. 詞彙範圍/參考教材", expanded=False):
        st.markdown("""
        * **詞彙範圍：** 學習詞表1至800詞，以及其衍生詞。
        * **參考教材：** 包含（第1階至第9階）教材、生活會話篇、閱讀書寫篇。
        """)
        
    with st.expander("2. 測驗架構/題型配分", expanded=False):
        st.caption("中高級認證總分為100分，[聽力(20分)/口說(30分)/閱讀(30分)/寫作(20分)四個項目]")
        st.markdown("""
        * **〖聽力測驗〗**
          * 聽音選詞(5題/10%)：聽族語句子，從4個詞彙或詞組選項中，選出答案。
          * 对話理解(5題/10%)：根據2位族人的對話，從4個選項中選出答案。
        * **〖口說測驗〗**
          * 段落朗讀(1題/10%)：朗讀40至50詞的短文(備答1分半鐘，作答1分半鐘)。
          * 情境問答(5題/10%)：聆聽2句(第1句為情境鋪陳)語音，再以族語表達看法(備答時間40秒)。
          * 看圖表達(1題/10%)：依圖片情境以族語表達想法（備答2分鐘，作答2分鐘)。
        * **〖閱讀測驗〗**
          * 詞彙語意(5題/10%)：依提示於4個選項中選出答案。
          * 語言結構(10題/20%)：依提示於4個選項中選出答案。
        * **〖寫作測驗〗**
          * 句子聽寫(5題/10%)：聽寫族語句子，每題播放2遍。
          * 問答題(5題/10%)：依題目指示，以族語句子回答。
        """)
        
    with st.expander("3. 合格標準", expanded=False):
        st.markdown("""
        滿分100分中，**總分達60分以上**，且單項成績達**聽力15分、口說15分、閱讀18分、寫作12分以上**，即可取得「通過聽說讀寫」的完整資格 。考生亦可依對應門檻獨立取得「通過聽說」或「通過讀寫」的資格 。
        """)

# 2. 🎧 聽力測驗
elif current_tab == "🎧 聽力":
    st.subheader("🎧 聽力測驗 (pitengil)")
    st.divider()
    listening_sub = st.radio(
        "題型選擇：",
        ["選擇題-聽音選詞", "選擇題-對話理解"],
        horizontal=True
    )
    
    if listening_sub == "選擇題-聽音選詞":
        st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
        st.markdown("### 🔍 選擇題 - 聽音選詞")
        
        if "random_quiz_order" not in st.session_state:
            st.session_state.random_quiz_order = list(range(len(QUIZ_DATA)))
            random.shuffle(st.session_state.random_quiz_order)
            
        if "current_pointer" not in st.session_state:
            st.session_state.current_pointer = 0
        if "audio_triggered" not in st.session_state:
            st.session_state.audio_triggered = False
        if "submitted" not in st.session_state:
            st.session_state.submitted = False
        if "shuffled_options_map" not in st.session_state:
            st.session_state.shuffled_options_map = {}

        ptr = st.session_state.current_pointer
        
        if ptr < len(QUIZ_DATA):
            true_quiz_id = st.session_state.random_quiz_order[ptr]
            current_quiz = QUIZ_DATA[true_quiz_id]
            
            if true_quiz_id not in st.session_state.shuffled_options_map:
                shuffled_raw_opts = current_quiz["options"].copy()
                random.shuffle(shuffled_raw_opts)
                
                formatted_opts = []
                correct_text_formatted = ""
                correct_word_raw = current_quiz["correct_text"]
                
                for i, word_item in enumerate(shuffled_raw_opts):
                    display_text = f"({i+1}) {word_item}"
                    formatted_opts.append(display_text)
                    if word_item == correct_word_raw:
                        correct_text_formatted = display_text
                
                st.session_state.shuffled_options_map[true_quiz_id] = {
                    "options": formatted_opts,
                    "correct_text": correct_text_formatted
                }
            
            live_quiz_data = st.session_state.shuffled_options_map[true_quiz_id]
            
            st.write(f"**[當前進度：第 {ptr + 1} 題 / 共 {len(QUIZ_DATA)} 題]**")
            st.write(current_quiz["question_text"])
            
            if st.button("🔊 播放題目", key=f"play_{ptr}"):
                st.session_state.audio_triggered = True
            
            if st.session_state.audio_triggered:
                if os.path.exists(current_quiz["audio_path"]):
                    st.audio(current_quiz["audio_path"], format="audio/mp3", autoplay=True)
                else:
                    st.warning(f"⚠️ 找不到音檔：`{current_quiz['audio_path']}`，請確認檔案是否已上傳。")
                st.session_state.audio_triggered = False
            
            st.write("---")
            
            user_choice = st.radio(
                "答案選項：",
                options=live_quiz_data["options"],
                index=None,
                key=f"radio_{ptr}",
                disabled=st.session_state.submitted
            )
            
            if not st.session_state.submitted:
                if st.button("📥 提交答案", key=f"submit_{ptr}"):
                    if user_choice is None:
                        st.warning("⚠️ 未作答無法提交！")
                    else:
                        st.session_state.submitted = True
                        st.rerun()
            else:
                correct_answer_text = live_quiz_data["correct_text"]
                
                if user_choice == correct_answer_text:
                    st.markdown(f"### 🔴 答題結果：✓")
                    st.success(f" Fangcal! 正確答案：**{correct_answer_text}**")
                else:
                    st.markdown(f"### 🔴 答題結果：✕")
                    st.error(f" 再接再厲！正確答案：**{correct_answer_text}**")
                
                if st.button("➡️ 下一題", key=f"next_{ptr}"):
                    st.session_state.current_pointer += 1
                    st.session_state.submitted = False
                    st.rerun()
        else:
            st.balloons()
            st.success("🎉 您已完成本輪全部 15 道隨機題目！系統正在為您重新洗牌出題...")
            if st.button("🔄 開始下一輪隨機挑戰"):
                random.shuffle(st.session_state.random_quiz_order)
                st.session_state.shuffled_options_map = {}
                st.session_state.current_pointer = 0
                st.session_state.submitted = False
                st.rerun()
                
        st.markdown('</div>', unsafe_allow_html=True)
        
    elif listening_sub == "選擇題-對話理解":
        try:
            with open("data/listening_dialogue.json", "r", encoding="utf-8") as f:
                ld_db = json.load(f)
        except FileNotFoundError:
            st.error("☠️ 系統性毀滅異常：偵測到 `data/listening_dialogue.json` 檔案遺失，請確認是否建立！")
            ld_db = []

        if ld_db:
            st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
            st.markdown("### 💬 選擇題 - 對話理解")
            
            ld_mode = st.radio("選題模式：", ["🎲 隨機挑題", "📋 自主選題"], horizontal=True, key="ld_mode_switch")
            
            # --- 狀態變數初始化區塊 ---
            if "ld_random_order" not in st.session_state:
                st.session_state.ld_random_order = list(range(len(ld_db)))
                random.shuffle(st.session_state.ld_random_order)
            if "ld_pointer" not in st.session_state:
                st.session_state.ld_pointer = 0
            if "ld_show_text" not in st.session_state:
                st.session_state.ld_show_text = {}
            if "ld_audio_triggered" not in st.session_state:
                st.session_state.ld_audio_triggered = False
            if "ld_opts_map" not in st.session_state:
                st.session_state.ld_opts_map = {}
            if "ld_submit_map" not in st.session_state:
                st.session_state.ld_submit_map = {}
            if "ld_choice_map" not in st.session_state:
                st.session_state.ld_choice_map = {}
                
            # --- 模式與指針判斷 ---
            if ld_mode == "🎲 隨機挑題":
                ptr = st.session_state.ld_pointer
                if ptr < len(ld_db):
                    true_id = st.session_state.ld_random_order[ptr]
                    current_quiz = ld_db[true_id]
                    st.write(f"**[當前進度：第 {ptr + 1} 題 / 共 {len(ld_db)} 題 (隨機)]**")
                else:
                    true_id = None
            else:
                select_options = [f"第 {i+1} 題：對話挑戰" for i in range(len(ld_db))]
                selected_str = st.selectbox("指定練習題組：", options=select_options, index=0)
                true_id = select_options.index(selected_str)
                current_quiz = ld_db[true_id]
                st.write(f"**[當前進度：自選第 {true_id + 1} 題 練習中]**")

            if true_id is not None:
                q_id = current_quiz["quiz_id"]
                
                # 確保單題狀態隔離
                if true_id not in st.session_state.ld_show_text:
                    st.session_state.ld_show_text[true_id] = False
                if true_id not in st.session_state.ld_submit_map:
                    st.session_state.ld_submit_map[true_id] = False
                if true_id not in st.session_state.ld_choice_map:
                    st.session_state.ld_choice_map[true_id] = None
                    
                # 確保選項洗牌並固定快取
                if true_id not in st.session_state.ld_opts_map:
                    shuffled_opts = current_quiz["options"].copy()
                    random.shuffle(shuffled_opts)
                    
                    formatted_opts = []
                    correct_ans_formatted = ""
                    for i, opt in enumerate(shuffled_opts):
                        display_text = f"({i+1}) {opt}"
                        formatted_opts.append(display_text)
                        if opt == current_quiz["correct_text"]:
                            correct_ans_formatted = display_text
                            
                    st.session_state.ld_opts_map[true_id] = {
                        "options": formatted_opts,
                        "correct_text": correct_ans_formatted
                    }
                
                live_quiz_data = st.session_state.ld_opts_map[true_id]

                # --- 題幹與音檔區塊 ---
                st.write("聆聽對話音檔，選出正確的描述：")
                if st.button("🔊 播放對話音檔", key=f"ld_play_{true_id}"):
                    st.session_state.ld_audio_triggered = True
                    
                if st.session_state.ld_audio_triggered:
                    raw_id = str(q_id).strip().zfill(2)
                    audio_folder = "assets/audio/01_listening/listening_dialogue"
                    target_audio = f"{audio_folder}/dialogue_{raw_id}.mp3"
                    
                    if os.path.exists(target_audio):
                        st.audio(target_audio, format="audio/mp3", autoplay=True)
                    else:
                        st.info("💡 **對話音檔正在製作中**，您可以點選下方按鈕直接展開族語文字進行練習。")
                    st.session_state.ld_audio_triggered = False

                st.write("---")
                
                # --- 文字提示切換區塊 ---
                text_label = "🔄 隱藏對話文字" if st.session_state.ld_show_text[true_id] else "👁️ 顯示對話文字"
                if st.button(text_label, key=f"ld_text_btn_{true_id}"):
                    st.session_state.ld_show_text[true_id] = not st.session_state.ld_show_text[true_id]
                    st.rerun()
                    
                if st.session_state.ld_show_text[true_id]:
                    st.info(f"💬 **對話內容：**\n\n{current_quiz['dialogue_amis']}")
                
                st.write("---")
                
                # --- 答題與訂正區塊 ---
                saved_choice = st.session_state.ld_choice_map[true_id]
                saved_index = live_quiz_data["options"].index(saved_choice) if saved_choice in live_quiz_data["options"] else None
                
                user_choice = st.radio(
                    "答案選項：",
                    options=live_quiz_data["options"],
                    index=saved_index,
                    key=f"ld_radio_{true_id}",
                    disabled=st.session_state.ld_submit_map[true_id]
                )
                
                if not st.session_state.ld_submit_map[true_id]:
                    st.session_state.ld_choice_map[true_id] = user_choice
                
                if not st.session_state.ld_submit_map[true_id]:
                    if st.button("📥 提交答案", key=f"ld_submit_btn_{true_id}"):
                        if user_choice is None:
                            st.warning("⚠️ 未作答無法提交！")
                        else:
                            st.session_state.ld_submit_map[true_id] = True
                            st.rerun()
                else:
                    correct_ans_str = live_quiz_data["correct_text"]
                    if user_choice == correct_ans_str:
                        st.markdown(f"### 🔴 答題結果：✓")
                        st.success(f" Fangcal! 正確答案：**{correct_ans_str}**")
                    else:
                        st.markdown(f"### 🔴 答題結果：✕")
                        st.error(f" 再接再厲！正確答案：**{correct_ans_str}**")
                        
                    if ld_mode == "🎲 隨機挑題":
                        st.write("")
                        if st.button("➡️ 下一題 (隨機抽題)", key=f"ld_next_{true_id}"):
                            st.session_state.ld_pointer += 1
                            st.rerun()
            else:
                st.balloons()
                st.success("🎉 恭喜！您已完成對話理解的全部隨機練習！")
                if st.button("🔄 重新挑戰", key="ld_reset"):
                    st.session_state.ld_pointer = 0
                    random.shuffle(st.session_state.ld_random_order)
                    st.session_state.ld_show_text = {}
                    st.session_state.ld_submit_map = {}
                    st.session_state.ld_opts_map = {}
                    st.session_state.ld_choice_map = {}
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

# 3. 🗣️ 口說測驗
elif current_tab == "🗣️ 口說":
    st.subheader("🗣️ 口說測驗 (pisowal)")
    st.divider()
    speaking_sub = st.radio(
        "題型選擇：",
        ["段落朗讀", "情境問答", "看圖表達"],
        horizontal=True
    )
    
    if speaking_sub == "段落朗讀":
        st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
        st.markdown("### 📖 口說 - 段落朗讀")
        
        try:
            with open("data/speaking_quiz.json", "r", encoding="utf-8") as f:
                speaking_db = json.load(f)
                
            menu_options = ["題目選單..."] + [f"題目{item['quiz_id']}：{item['title']}" for item in speaking_db]
            
            selected_quiz = st.selectbox(
                "請選擇朗讀題目：",
                options=menu_options,
                index=0,
                key="speaking_quiz_selector"
            )
            
            st.divider()
            
            if selected_quiz == "題目選單...":
                pass
            else:
                current_id = selected_quiz.split("：")[0].replace("題目", "")
                current_article = next((item for item in speaking_db if str(item["quiz_id"]) == str(current_id)), None)
                
                if current_article:
                    st.markdown(f"#### 🎯 {current_article['title']}")
                    
                    # 🚀 新增：動態字體大小控制桿
                    font_size = st.slider("🔍 調整字體大小", min_value=16, max_value=48, value=20, step=2)
                    
                    # 🎨 修改：使用帶有 CSS 樣式的 HTML 區塊來渲染文章，取代原先的 st.info
                    st.markdown(
                        f"""
                        <div style="
                            padding: 20px; 
                            border-radius: 10px; 
                            background-color: rgba(13, 148, 136, 0.1); 
                            border-left: 5px solid #0D9488;
                            font-size: {font_size}px; 
                            line-height: 1.6;
                            margin-bottom: 15px;
                            color: var(--text-color);
                        ">
                            {current_article['content']}
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                    
                    st.caption(f"來源：{current_article['source']} ｜ 建議準備時間：1分半鐘 ｜ 建議朗讀時間：1分半鐘")
                else:
                    st.error("⚠️ 找不到該題目的對應內容，請重新選擇。")
                
        except FileNotFoundError:
            st.error("☠️ 系統性毀滅異常：偵測到 `data/speaking_quiz.json` 檔案遺失，請檢查 GitHub 儲存庫路徑！")
            
        st.markdown('</div>', unsafe_allow_html=True)
        
    # ─── 題型二：情境問答（⚡ 終極修復：強制物理路徑鎖定與優雅降級） ───
    elif speaking_sub == "情境問答":
        try:
            with open("data/speaking_situations.json", "r", encoding="utf-8") as f:
                speaking_situation_db = json.load(f)
        except FileNotFoundError:
            st.error("☠️ 系統性毀滅異常：偵測到 `data/speaking_situations.json` 檔案遺失，請確認是否建立！")
            speaking_situation_db = []

        if speaking_situations_db := speaking_situation_db:
            st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
            st.markdown("### 🗣️ 口說 - 情境問答")
            
            s_mode = st.radio("練習模式設定：", ["🎲 隨機挑題", "📋 自主選題"], horizontal=True, key="s_mode_switch")
            
            if "s_random_order" not in st.session_state:
                st.session_state.s_random_order = list(range(len(speaking_situations_db)))
                random.shuffle(st.session_state.s_random_order)
            if "s_pointer" not in st.session_state:
                st.session_state.s_pointer = 0
            if "s_show_q_amis" not in st.session_state:
                st.session_state.s_show_q_amis = {}
            if "s_show_q_trans" not in st.session_state:
                st.session_state.s_show_q_trans = {}
            if "s_show_ans" not in st.session_state:
                st.session_state.s_show_ans = {}
            if "s_audio_triggered" not in st.session_state:
                st.session_state.s_audio_triggered = False

            # 分流索引提取器
            if s_mode == "🎲 隨機挑題":
                s_ptr = st.session_state.s_pointer
                if s_ptr < len(speaking_situations_db):
                    true_s_id = st.session_state.s_random_order[s_ptr]
                    current_s_quiz = speaking_situations_db[true_s_id]
                    st.write(f"**[當前進度：第 {s_ptr + 1} 題 / 共 {len(speaking_situations_db)} 題 (隨機)]**")
                else:
                    true_s_id = None
            else:
                s_select_options = [f"第 {i+1} 題：題組挑戰" for i in range(len(speaking_situations_db))]
                selected_s_index_str = st.selectbox("選定題組：", options=s_select_options, index=0)
                true_s_id = s_select_options.index(selected_s_index_str)
                current_s_quiz = speaking_situations_db[true_s_id]
                st.write(f"**[當前進度：自選 第 {true_s_id + 1} 題練習中]**")

            if true_s_id is not None:
                if true_s_id not in st.session_state.s_show_q_amis:
                    st.session_state.s_show_q_amis[true_s_id] = False
                if true_s_id not in st.session_state.s_show_q_trans:
                    st.session_state.s_show_q_trans[true_s_id] = False
                if true_s_id not in st.session_state.s_show_ans:
                    st.session_state.s_show_ans[true_s_id] = False

                if st.button("🔊 播放題目音檔", key=f"s_play_btn_{true_s_id}"):
                    st.session_state.s_audio_triggered = True
                
                # 🔴 核心修復區塊：無視 JSON 設定，強制鎖定實體路徑
                if st.session_state.s_audio_triggered:
                    raw_id = str(current_s_quiz['quiz_id']).strip().zfill(2)
                    
                    # 🚀 強制綁定您截圖中確認的 GitHub 真實路徑
                    target_audio = f"assets/audio/02_speaking/speaking_qa/situation_{raw_id}.mp3"
                    
                    if os.path.exists(target_audio):
                        st.audio(target_audio, format="audio/mp3", autoplay=True)
                    else:
                        # 優雅降級：檔案不存在時，不顯示任何錯誤碼，僅顯示溫和提示
                        st.info("💡 **題目語音音檔正在製作中**，您可以點選下方按鈕直接展開族語或中文意思進行練習。")
                        
                    st.session_state.s_audio_triggered = False

                col_q1, col_q2 = st.columns(2)
                with col_q1:
                    s_q_amis_label = "🔄 隱藏族語" if st.session_state.s_show_q_amis[true_s_id] else "👁️ 顯示族語"
                    if st.button(s_q_amis_label, key=f"s_q_amis_toggle_{true_s_id}"):
                        st.session_state.s_show_q_amis[true_s_id] = not st.session_state.s_show_q_amis[true_s_id]
                        st.rerun()
                with col_q2:
                    s_q_trans_label = "🔄 隱藏中文" if st.session_state.s_show_q_trans[true_s_id] else "👁️ 顯示中文"
                    if st.button(s_q_trans_label, key=f"s_q_trans_toggle_{true_s_id}"):
                        st.session_state.s_show_q_trans[true_s_id] = not st.session_state.s_show_q_trans[true_s_id]
                        st.rerun()

                if st.session_state.s_show_q_amis[true_s_id]:
                    st.info(f"💬 **阿美族語：**\n\n{current_s_quiz['question_amis']}")
                if st.session_state.s_show_q_trans[true_s_id]:
                    st.markdown(f"> 💡 **中文：** {current_s_quiz['question_ch']}")

                st.write("---")
                
                s_ans_label = "🔄 關閉參考答案" if st.session_state.s_show_ans[true_s_id] else "📥 顯示參考答案"
                
                col_ans1, col_ans2 = st.columns([1, 3])
                with col_ans1:
                    if st.button(s_ans_label, key=f"s_ans_btn_{true_s_id}"):
                        st.session_state.s_show_ans[true_s_id] = not st.session_state.s_show_ans[true_s_id]
                        st.rerun()
                        
                with col_ans2:
                    if st.session_state.s_show_ans[true_s_id]:
                        st.success(f"✨ **阿美族語：**\n\n{current_s_quiz['suggested_answer_amis']}\n\n"
                                   f"───\n\n💡 **中文：**\n\n{current_s_quiz['suggested_answer_ch']}")
                        
                # 🛠️ 補丁 2：修正隨機挑戰題目模式下的換題切換指針
                if s_mode == "🎲 隨機挑題":
                    st.write("")
                    if st.button("➡️ 下一題 (隨機抽題)", key=f"s_next_btn_{true_s_id}"):
                        st.session_state.s_pointer += 1
                        st.rerun()
            else:
                st.balloons()
                st.success("🎉 恭喜！您已完成全部口說情境問答的隨機練習！")
                if st.button("🔄 重新挑戰", key="reset_speaking_situations"):
                    st.session_state.s_pointer = 0
                    if "s_show_ans" in st.session_state:
                        del st.session_state["s_show_ans"]
                    if "s_show_q_trans" in st.session_state:
                        del st.session_state["s_show_q_trans"]
                    if "s_show_q_amis" in st.session_state:
                        del st.session_state["s_show_q_amis"]
                    random.shuffle(st.session_state.s_random_order)
                    st.rerun()
                    
            st.markdown('</div>', unsafe_allow_html=True)
            
    elif speaking_sub == "看圖表達":
        try:
            with open("data/speaking_images.json", "r", encoding="utf-8") as f:
                speaking_img_db = json.load(f)
        except FileNotFoundError:
            st.error("☠️ 系統性毀滅異常：偵測到 `data/speaking_images.json` 檔案遺失，請確認是否建立！")
            speaking_img_db = []

        if speaking_img_db:
            st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
            st.markdown("### 🖼️ 口說 - 看圖表達")
            
            if "img_show_draft" not in st.session_state:
                st.session_state.img_show_draft = False
            if "img_show_ans" not in st.session_state:
                st.session_state.img_show_ans = False
            if "draft_text_cache" not in st.session_state:
                st.session_state.draft_text_cache = {}

            img_menu_options = ["請選擇題目..."] + [item["title"] for item in speaking_img_db]
            
            selected_img_title = st.selectbox(
                "主題選擇：",
                options=img_menu_options,
                index=0,
                key="img_quiz_selector"
            )
            
            st.divider()
            
            if selected_img_title == "請選擇題目...":
                pass
            else:
                current_img_quiz = next(item for item in speaking_img_db if item["title"] == selected_img_title)
                q_id = current_img_quiz["quiz_id"]
                
                if os.path.exists(current_img_quiz["image_path"]):
                    st.image(current_img_quiz["image_path"], use_container_width=True)
                else:
                    st.error(f"⚠️ 找不到題目對應的實體圖片檔案：`{current_img_quiz['image_path']}`，請確認已上傳。")
                
                st.write("---")
                
                draft_btn_label = "🔄 關閉草稿區" if st.session_state.img_show_draft else "📝 顯示草稿區"
                if st.button(draft_btn_label, key="img_draft_toggle_btn"):
                    st.session_state.img_show_draft = not st.session_state.img_show_draft
                    st.rerun()
                
                if st.session_state.img_show_draft:
                    if q_id not in st.session_state.draft_text_cache:
                        st.session_state.draft_text_cache[q_id] = ""
                        
                    user_draft = st.text_area(
                        "寫下你的回答提示（學習者書寫區）：",
                        value=st.session_state.draft_text_cache[q_id],
                        placeholder="在此輸入內容，隱藏草稿區後內容會安全保留...",
                        key=f"img_draft_input_{q_id}"
                    )
                    st.session_state.draft_text_cache[q_id] = user_draft
                
                st.write("")
                
                img_ans_label = "🔄 關閉參考答案" if st.session_state.img_show_ans else "📥 顯示參考答案"
                
                col_ans1, col_ans2 = st.columns([1, 3])
                with col_ans1:
                    if st.button(img_ans_label, key="img_ans_toggle_btn"):
                        st.session_state.img_show_ans = not st.session_state.img_show_ans
                        st.rerun()
                        
                with col_ans2:
                    if st.session_state.img_show_ans:
                        st.success(f"✨ **內建參考答案 (阿美語)：**\n\n{current_img_quiz['suggested_answer_amis']}\n\n"
                                   f"───\n\n💡 **中文翻譯：**\n\n{current_img_quiz['suggested_answer_ch']}")
            
            st.markdown('</div>', unsafe_allow_html=True)

# 4. 📖 閱讀測驗
elif current_tab == "📖 閱讀":
    st.subheader("📖 閱讀測驗 (piasip)")
    st.divider()
    reading_sub = st.radio(
        "閱讀題型選擇：",
        ["選擇題-詞彙語意", "選擇題-語言結構"],
        horizontal=True
    )
    
    try:
        with open("data/reading_quiz.json", "r", encoding="utf-8") as f:
            all_reading_data = json.load(f)
    except FileNotFoundError:
        st.error("☠️ 系統性毀滅異常：偵測到 `data/reading_quiz.json` 檔案遺失，請確認檔案是否已放置於 data/ 資料夾。")
        all_reading_data = []

    if all_reading_data:
        target_type = "vocabulary" if reading_sub == "選擇題-詞彙語意" else "structure"
        reading_db = [item for item in all_reading_data if item["type"] == target_type]
        
        state_order_key = f"r_{target_type}_order"
        state_ptr_key = f"r_{target_type}_ptr"
        state_opts_key = f"r_{target_type}_opts_map"
        state_submit_key = f"r_{target_type}_submit_map"
        state_choice_key = f"r_{target_type}_choice_map"
        
        if state_order_key not in st.session_state:
            st.session_state[state_order_key] = list(range(len(reading_db)))
            random.shuffle(st.session_state[state_order_key])
            
        if state_ptr_key not in st.session_state:
            st.session_state[state_ptr_key] = 0
            
        if state_opts_key not in st.session_state:
            st.session_state[state_opts_key] = {}
            
        if state_submit_key not in st.session_state:
            st.session_state[state_submit_key] = {}
            
        if state_choice_key not in st.session_state:
            st.session_state[state_choice_key] = {}

        r_ptr = st.session_state[state_ptr_key]
        
        if r_ptr < len(reading_db):
            st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
            
            true_r_id = st.session_state[state_order_key][r_ptr]
            current_r_quiz = reading_db[true_r_id]
            
            if true_r_id not in st.session_state[state_submit_key]:
                st.session_state[state_submit_key][true_r_id] = False
            if true_r_id not in st.session_state[state_choice_key]:
                st.session_state[state_choice_key][true_r_id] = None
                
            if true_r_id not in st.session_state[state_opts_key]:
                shuffled_raw_opts = current_r_quiz["options"].copy()
                random.shuffle(shuffled_raw_opts)
                
                formatted_opts = []
                correct_text_formatted = ""
                correct_word_raw = current_r_quiz["correct_text"]
                
                for i, word_item in enumerate(shuffled_raw_opts):
                    display_text = f"({i+1}) {word_item}"
                    formatted_opts.append(display_text)
                    if word_item == correct_word_raw:
                        correct_text_formatted = display_text
                        
                st.session_state[state_opts_key][true_r_id] = {
                    "options": formatted_opts,
                    "correct_text": correct_text_formatted
                }
                
            live_r_data = st.session_state[state_opts_key][true_r_id]
            
            st.write(f"**當前進度：第 {r_ptr + 1} 題 / 共 {len(reading_db)} 題 (隨機出題組模式)**")
            st.write(current_r_quiz["question_text"])
            st.write("---")
            
            saved_choice = st.session_state[state_choice_key][true_r_id]
            saved_index = live_r_data["options"].index(saved_choice) if saved_choice in live_r_data["options"] else None
            
            user_r_choice = st.radio(
                "請選出正確的選項：",
                options=live_r_data["options"],
                index=saved_index,
                key=f"r_radio_{target_type}_{r_ptr}",
                disabled=st.session_state[state_submit_key][true_r_id]
            )
            
            if not st.session_state[state_submit_key][true_r_id]:
                st.session_state[state_choice_key][true_r_id] = user_r_choice
            
            if not st.session_state[state_submit_key][true_r_id]:
                if st.button("📥 提交答案", key=f"r_submit_btn_{target_type}_{r_ptr}"):
                    if user_r_choice is None:
                        st.warning("⚠️ 請先選擇一個選項再行提交！")
                    else:
                        st.session_state[state_submit_key][true_r_id] = True
                        st.rerun()
            else:
                correct_ans_str = live_r_data["correct_text"]
                
                # 🚀 新增：動態讀取 JSON 中的中文解釋，並進行字串組裝
                meaning = current_r_quiz.get("chinese_meaning", "")
                display_correct_text = f"{correct_ans_str} （{meaning}）" if meaning else correct_ans_str
                
                if user_r_choice == correct_ans_str:
                    st.markdown(f"### 🔴 答題結果：✓")
                    st.success(f" Fangcal! 正確答案：**{display_correct_text}**")
                else:
                    st.markdown(f"### 🔴 答題結果：✕")
                    st.error(f" 再接再厲！正確答案：**{display_correct_text}**")
            
            st.write("")
            
            nav_col1, nav_col2 = st.columns(2)
            with nav_col1:
                if st.button("⬅️ 上一題", key=f"r_prev_btn_{target_type}_{r_ptr}", disabled=(r_ptr == 0)):
                    st.session_state[state_ptr_key] -= 1
                    st.rerun()
            with nav_col2:
                if st.button("➡️ 下一題", key=f"r_next_btn_{target_type}_{r_ptr}"):
                    st.session_state[state_ptr_key] += 1
                    st.rerun()
                    
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.balloons()
            st.success("🎉 恭喜！您已完成本項目全部 {len(reading_db)} 道隨機題組練習！")
            if st.button("🔄 重新洗牌挑戰", key=f"r_reset_{target_type}"):
                random.shuffle(st.session_state[state_order_key])
                st.session_state[state_ptr_key] = 0
                st.session_state[state_opts_key] = {}
                st.session_state[state_submit_key] = {}
                st.session_state[state_choice_key] = {}
                st.rerun()

# 5. ✍️ 寫作測驗
elif current_tab == "✍️ 寫作":
    st.subheader("✍️ 寫作測驗 (pitilid)")
    st.divider()
    writing_sub = st.radio(
        "寫作題型選擇：",
        ["句子聽寫", "問答"],
        horizontal=True
    )
    
    try:
        with open("data/writing_quiz.json", "r", encoding="utf-8") as f:
            all_writing_data = json.load(f)
    except FileNotFoundError:
        st.error("☠️ 系統性毀滅異常：偵測到 `data/writing_quiz.json` 檔案遺失，請檢查儲存庫路徑！")
        all_writing_data = []

    if all_writing_data:
        if writing_sub == "句子聽寫":
            st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
            st.markdown("### ✍️ 寫作測驗 - 句子聽寫")
            
            dictation_db = [item for item in all_writing_data if item["type"] == "dictation"]
            
            if "writing_dictation_order" not in st.session_state:
                st.session_state.writing_dictation_order = list(range(len(dictation_db)))
                random.shuffle(st.session_state.writing_dictation_order)
                
            if "writing_pointer" not in st.session_state:
                st.session_state.writing_pointer = 0
            if "writing_audio_triggered" not in st.session_state:
                st.session_state.writing_audio_triggered = False
            if "writing_submitted" not in st.session_state:
                st.session_state.writing_submitted = False

            w_ptr = st.session_state.writing_pointer
            
            if w_ptr < len(dictation_db):
                true_w_id = st.session_state.writing_dictation_order[w_ptr]
                current_w_quiz = dictation_db[true_w_id]
                
                st.write(f"**當前進度：第 {w_ptr + 1} 題 / 共 {len(dictation_db)} 題**")
                st.write(current_w_quiz["question_text"])
                
                if st.button("🔊 播放題目", key=f"w_play_{w_ptr}"):
                    st.session_state.writing_audio_triggered = True
                
                if st.session_state.writing_audio_triggered:
                    if os.path.exists(current_w_quiz["audio_path"]):
                        st.audio(current_w_quiz["audio_path"], format="audio/mp3", autoplay=True)
                    else:
                        st.error(f"⚠️ 找不到音檔！請確認此檔案是否已正確上傳至 GitHub 儲存庫：\n`{current_w_quiz['audio_path']}`")
                    st.session_state.writing_audio_triggered = False
                
                st.write("---")
                
                user_typed_answer = st.text_input(
                    "請在此輸入聽到的完整族語句子（注意大小寫與標點符號）：",
                    placeholder="請輸入答案...",
                    key=f"w_input_{w_ptr}",
                    disabled=st.session_state.writing_submitted
                )
                
                if not st.session_state.writing_submitted:
                    if st.button("📥 提交答案", key=f"w_submit_{w_ptr}"):
                        if not user_typed_answer.strip():
                            st.warning("⚠️ 請先在輸入框打字再行提交！")
                        else:
                            st.session_state.writing_submitted = True
                            st.rerun()
                else:
                    correct_sentence = current_w_quiz["correct_text"]
                    
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.button("📥 提交答案", key=f"w_sub_dis_{w_ptr}", disabled=True)
                    with col2:
                        st.info(f"💡 正確答案：**{correct_sentence}**")
                    
                    st.write("")
                    if st.button("➡️ 下一題", key=f"w_next_{w_ptr}"):
                        st.session_state.writing_pointer += 1
                        st.session_state.writing_submitted = False
                        st.rerun()
            else:
                st.balloons()
                st.success("🎉 您已完成本輪全部 5 道隨機聽寫題目！")
                if st.button("🔄 開始下一輪隨機挑戰", key="reset_writing"):
                    random.shuffle(st.session_state.writing_dictation_order)
                    st.session_state.writing_pointer = 0
                    st.session_state.writing_submitted = False
                    st.rerun()
                    
            st.markdown('</div>', unsafe_allow_html=True)
            
        elif writing_sub == "問答":
            st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
            st.markdown("### 📝 寫作測驗 - 問答")
            
            question_db = [item for item in all_writing_data if item["type"] == "question"]
            
            if "q_pointer" not in st.session_state:
                st.session_state.q_pointer = 0
            if "q_input_text_cache" not in st.session_state:
                st.session_state.q_input_text_cache = {}

            q_ptr = st.session_state.q_pointer
            
            if q_ptr < len(question_db):
                current_q_quiz = question_db[q_ptr]
                q_id = current_q_quiz.get("id", q_ptr)
                
                if "q_show_trans" not in st.session_state:
                    st.session_state.q_show_trans = {}
                if "q_show_ans" not in st.session_state:
                    st.session_state.q_show_ans = {}
                    
                if q_ptr not in st.session_state.q_show_trans:
                    st.session_state.q_show_trans[q_ptr] = False
                if q_ptr not in st.session_state.q_show_ans:
                    st.session_state.q_show_ans[q_ptr] = False
                if q_id not in st.session_state.q_input_text_cache:
                    st.session_state.q_input_text_cache[q_id] = ""
                
                st.write(f"**當前進度：第 {q_ptr + 1} 題 / 共 {len(question_db)} 題**")
                st.markdown(f"#### ❓ 問：{current_q_quiz['question_text']}")
                
                trans_btn_label = "🔄 關閉中文翻譯" if st.session_state.q_show_trans[q_ptr] else "👁️ 顯示中文翻譯"
                if st.button(trans_btn_label, key=f"q_trans_toggle_{q_ptr}"):
                    st.session_state.q_show_trans[q_ptr] = not st.session_state.q_show_trans[q_ptr]
                    st.rerun()
                
                if st.session_state.q_show_trans[q_ptr]:
                    st.info(f"💡 中文提示：{current_q_quiz['chinese_translation']}")
                
                st.write("---")
                
                user_typed_ans = st.text_input(
                    "請在此輸入答案進行練習（注意大小寫與標點符號）：",
                    value=st.session_state.q_input_text_cache[q_id],
                    placeholder="在此輸入您的練習答案...",
                    key=f"q_text_input_field_{q_id}"
                )
                st.session_state.q_input_text_cache[q_id] = user_typed_ans
                
                st.write("")
                
                ans_btn_label = "🔄 關閉參考答案" if st.session_state.q_show_ans[q_ptr] else "📥 顯示參考答案"
                
                col1, col2 = st.columns([1, 3])
                with col1:
                    if st.button(ans_btn_label, key=f"q_ans_toggle_{q_ptr}"):
                        st.session_state.q_show_ans[q_ptr] = not st.session_state.q_show_ans[q_ptr]
                        st.rerun()
                
                with col2:
                    if st.session_state.q_show_ans[q_ptr]:
                        suggested_ans = current_q_quiz["suggested_answer"]
                        st.success(f"✨ 參考答案：**{suggested_ans}**")
                
                if st.session_state.q_show_ans[q_ptr]:
                    st.write("")
                    if st.button("➡️ 下一題", key=f"q_next_{q_ptr}"):
                        st.session_state.q_pointer += 1
                        st.rerun()
            else:
                st.success("🎉 您已完成「問答」全部題目的練習！")
                if st.button("🔄 重新挑戰", key="reset_questions"):
                    st.session_state.q_pointer = 0
                    if "q_show_trans" in st.session_state:
                        del st.session_state["q_show_trans"]
                    if "q_show_ans" in st.session_state:
                        del st.session_state["q_show_ans"]
                    if "q_input_text_cache" in st.session_state:
                        del st.session_state["q_input_text_cache"]
                    st.rerun()
                    
            st.markdown('</div>', unsafe_allow_html=True)

# ---- App 底部註腳 ----
st.write("---")
st.caption(f"© 2026 中高級認證 App 三一開發團隊 ｜ 系統版本：**{APP_VERSION}**")
