import streamlit as st
from PIL import Image
import numpy as np
import pytesseract
import re
import time
from datetime import datetime
import json
import cv2  # تم إضافة مكتبة المعالجة

# --------------------------------------------------
# Tesseract Path (Windows)
# --------------------------------------------------
#pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="ID Scanner Pro",
    page_icon="🪪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# Custom CSS (نفس التصميم الاحترافي)
# --------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1d3a 100%);
    }
    
    .hero-section {
        text-align: center;
        padding: 3rem 0 2rem 0;
        animation: fadeInDown 0.8s ease-out;
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { filter: drop-shadow(0 0 10px rgba(102, 126, 234, 0.5)); }
        to { filter: drop-shadow(0 0 20px rgba(118, 75, 162, 0.8)); }
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        color: #a8b2d1;
        margin-bottom: 2rem;
        animation: fadeIn 1.2s ease-out;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        margin: 1.5rem 0;
        animation: slideUp 0.8s ease-out;
    }
    
    .info-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        animation: fadeIn 0.6s ease-out;
    }
    
    .info-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        border-color: rgba(102, 126, 234, 0.6);
    }
    
    .info-label {
        font-size: 0.85rem;
        color: #667eea;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .info-value {
        font-size: 1.4rem;
        color: #ffffff;
        font-weight: 600;
        word-wrap: break-word;
    }
    
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        color: white;
        animation: pulse 2s ease-in-out infinite;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    .feature-box {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
        animation: fadeIn 1s ease-out;
    }
    
    .feature-box:hover {
        background: rgba(102, 126, 234, 0.1);
        transform: translateY(-10px);
        border-color: rgba(102, 126, 234, 0.5);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        color: #a8b2d1;
        font-size: 0.95rem;
    }
    
    .raw-text-container {
        background: #0d1117;
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        color: #00ff88;
        max-height: 400px;
        overflow-y: auto;
        line-height: 1.6;
        direction: rtl;
        text-align: right;
    }
    
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    }
    
    .sidebar-content {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    /* Animations */
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    @keyframes fadeInDown { from { opacity: 0; transform: translateY(-30px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes slideUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Initialize Session State
# --------------------------------------------------
if 'scan_count' not in st.session_state:
    st.session_state.scan_count = 0
if 'scan_history' not in st.session_state:
    st.session_state.scan_history = []

# --------------------------------------------------
# Image Preprocessing Function
# --------------------------------------------------
def preprocess_for_ocr(image_np):
    # 1. تحويل الصورة إلى تدرجات الرمادي (Grayscale)
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
    
    # 2. تحسين التباين التكيفي (CLAHE) لإبراز النصوص المكتوبة خصوصاً في الخلفيات المزعجة
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    contrast_enhanced = clahe.apply(gray)
    
    # 3. تكبير الصورة قليلاً (Scaling) لتوضيح الحروف الصغيرة
    scaled = cv2.resize(contrast_enhanced, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    
    # 4. تصفية الضوضاء (Denoising)
    denoised = cv2.bilateralFilter(scaled, 9, 75, 75)
    
    return denoised

# --------------------------------------------------
# OCR Function
# --------------------------------------------------
def extract_text_from_id(image):
    try:
        # --psm 3 يساعد Tesseract على فهم الهيكل العام للنص
        custom_config = r'--oem 3 --psm 3'
        text = pytesseract.image_to_string(image, lang='ara+eng', config=custom_config)
    except Exception as e:
        text = pytesseract.image_to_string(image)
    return text

# --------------------------------------------------
# Helper Function (Smart Extraction)
# --------------------------------------------------
def parse_id_text(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    data = {
        "organization": "",
        "name": "",
        "phone": "",
        "email": "",
        "address": "",
        "id_number": "",
        "dates": [],
        "gender": "",
        "raw": lines
    }

    if len(lines) >= 2:
        data["organization"] = lines[0] + " " + lines[1]

    for line in lines:
        line_lower = line.lower()
        
        if not data["email"]:
            email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", line)
            if email_match:
                data["email"] = email_match.group()

        if not data["phone"]:
            phone_match = re.search(r"\+?\d[\d\-\s]{7,15}", line)
            if phone_match and len(phone_match.group().replace(" ", "").replace("-", "")) >= 10:
                data["phone"] = phone_match.group()

        if not data["address"]:
            if 'address' in line_lower or 'عنوان' in line_lower:
                if ':' in line:
                    data["address"] = line.split(':', 1)[1].strip()
                else:
                    data["address"] = line

        if not data["id_number"]:
            id_match = re.search(r'\b\d{10,14}\b', line.replace(" ", ""))
            if id_match:
                data["id_number"] = id_match.group()

        date_match = re.search(r'\b\d{2}[-/]\d{2}[-/]\d{4}\b', line)
        if date_match and date_match.group() not in data["dates"]:
            data["dates"].append(date_match.group())
            
        if not data["gender"]:
            if "ذكر" in line_lower or "male" in line_lower and "female" not in line_lower:
                data["gender"] = "Male / ذكر"
            elif "أنثى" in line_lower or "انثى" in line_lower or "female" in line_lower:
                data["gender"] = "Female / أنثى"

    job_keywords = ["director", "manager", "engineer", "officer", "designer", "president", "executive", "ceo", "مهندس", "مدير", "طالب", "عامل", "محاسب"]
    for i, line in enumerate(lines):
        if any(job in line.lower() for job in job_keywords):
            if i > 0 and not data["name"]:
                data["name"] = lines[i - 1]
            break
            
    if not data["name"] and len(lines) >= 3:
        data["name"] = lines[2]

    return data

# --------------------------------------------------
# Sidebar
# --------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Control Panel")
    
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown("#### 📊 Statistics")
    st.markdown(f'<div class="stat-box"><div class="stat-number">{st.session_state.scan_count}</div><div class="stat-label">Total Scans</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown("#### 🎛️ Settings")
    show_preprocessing = st.checkbox("Show Preprocessed Image", value=True) # تم تفعيل هذا الخيار ليظهر لك فلتر التوضيح
    show_raw_text = st.checkbox("Show Raw OCR Text", value=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown("#### ℹ️ About")
    st.info("🪪 **ID Scanner Pro**\n\nAdvanced OCR technology powered by Tesseract & OpenCV.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.scan_count > 0:
        st.markdown("---")
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.scan_count = 0
            st.session_state.scan_history = []
            st.rerun()

# --------------------------------------------------
# Main Content
# --------------------------------------------------

st.markdown("""
<div class="hero-section">
    <div class="hero-title">🪪 ID SCANNER PRO</div>
    <div class="hero-subtitle">Extract information from ID cards using OpenCV & Tesseract OCR</div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "📤 Upload Your ID Card",
    type=["jpg", "jpeg", "png"],
    help="Supported formats: JPG, JPEG, PNG"
)

if uploaded_file:
    st.session_state.scan_count += 1
    
    col_img, col_data = st.columns([1, 1], gap="large")
    
    with col_img:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📸 Image Viewer")
        image = Image.open(uploaded_file)
        image_np = np.array(image)
        
        # إنشاء تبويبات (Tabs) للمقارنة بين الصورة الأصلية والمعالجة
        if show_preprocessing:
            tab1, tab2 = st.tabs(["Original", "Preprocessed (Enhanced)"])
            with tab1:
                st.image(image, use_container_width=True)
            with tab2:
                processed_img = preprocess_for_ocr(image_np)
                st.image(processed_img, use_container_width=True)
        else:
            st.image(image, use_container_width=True, caption="Original ID Card")
            processed_img = preprocess_for_ocr(image_np) # لا تزال المعالجة تحدث في الخلفية لضمان الدقة
            
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_data:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🔄 Processing")
        
        progress_placeholder = st.empty()
        status_placeholder = st.empty()
        
        with progress_placeholder.container():
            progress_bar = st.progress(0)
            
        status_placeholder.info("🔍 Enhancing image quality with OpenCV...")
        # يتم استخدام الصورة المعالجة هنا
        final_image_for_ocr = processed_img if 'processed_img' in locals() else preprocess_for_ocr(image_np)
        time.sleep(0.3)
        progress_bar.progress(30)
        
        status_placeholder.info("🧠 Running OCR engine (Tesseract)...")
        extracted_text = extract_text_from_id(final_image_for_ocr)
        time.sleep(0.4)
        progress_bar.progress(60)
        
        status_placeholder.info("📝 Parsing information with AI logic...")
        parsed_data = parse_id_text(extracted_text)
        time.sleep(0.3)
        progress_bar.progress(90)
        
        status_placeholder.success("✨ Finalizing results...")
        time.sleep(0.2)
        progress_bar.progress(100)
        
        time.sleep(0.3)
        progress_placeholder.empty()
        status_placeholder.success("✅ Extraction Complete!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Results Section
    st.markdown("---")
    st.markdown("## 📋 Extracted Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="info-card">
            <div class="info-label">👤 Name</div>
            <div class="info-value">{parsed_data['name'] or 'Not detected'}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="info-card">
            <div class="info-label">🏢 Organization / Job</div>
            <div class="info-value">{parsed_data['organization'] or 'Not detected'}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="info-card">
            <div class="info-label">📅 Dates (DOB/Expiry)</div>
            <div class="info-value">{' <br> '.join(parsed_data['dates']) if parsed_data['dates'] else 'Not detected'}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="info-card">
            <div class="info-label">🆔 ID Number</div>
            <div class="info-value">{parsed_data['id_number'] or 'Not detected'}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="info-card">
            <div class="info-label">📞 Phone</div>
            <div class="info-value">{parsed_data['phone'] or 'Not detected'}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="info-card">
            <div class="info-label">⚧ Gender</div>
            <div class="info-value">{parsed_data['gender'] or 'Not detected'}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="info-card">
            <div class="info-label">📍 Address</div>
            <div class="info-value">{parsed_data['address'] or 'Not detected'}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="info-card">
            <div class="info-label">📧 Email</div>
            <div class="info-value">{parsed_data['email'] or 'Not detected'}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Raw OCR Output
    if show_raw_text:
        st.markdown("---")
        st.markdown("## 🧠 Raw OCR Output")
        st.markdown(f"""
        <div class="raw-text-container">
            {'<br>'.join(parsed_data['raw']) if parsed_data['raw'] else 'No text detected'}
        </div>
        """, unsafe_allow_html=True)
    
    # Download Section
    st.markdown("---")
    col_d1, col_d2, col_d3 = st.columns(3)
    
    with col_d1:
        download_text = f"""
ID CARD INFORMATION
{'='*50}

Name: {parsed_data['name']}
ID Number: {parsed_data['id_number']}
Organization: {parsed_data['organization']}
Dates: {', '.join(parsed_data['dates'])}
Gender: {parsed_data['gender']}
Email: {parsed_data['email']}
Phone: {parsed_data['phone']}
Address: {parsed_data['address']}

{'='*50}
Extracted on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        st.download_button(
            label="📥 Download Text",
            data=download_text,
            file_name=f"id_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col_d2:
        json_data = json.dumps({
            "name": parsed_data['name'],
            "id_number": parsed_data['id_number'],
            "organization": parsed_data['organization'],
            "dates": parsed_data['dates'],
            "gender": parsed_data['gender'],
            "email": parsed_data['email'],
            "phone": parsed_data['phone'],
            "address": parsed_data['address'],
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }, indent=2, ensure_ascii=False)
        
        st.download_button(
            label="📦 Download JSON",
            data=json_data,
            file_name=f"id_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col_d3:
        if st.button("🔄 Scan Another", use_container_width=True):
            st.rerun()

else:
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">👁️</div>
            <div class="feature-title">Computer Vision</div>
            <div class="feature-desc">OpenCV image enhancement for maximum text clarity</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">High Accuracy</div>
            <div class="feature-desc">Powered by Tesseract OCR with Arabic & English support</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">🔒</div>
            <div class="feature-title">100% Secure</div>
            <div class="feature-desc">All processing happens locally on your machine</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div class="glass-card">
        <h3>📝 How to Use</h3>
        <ol style="color: #a8b2d1; font-size: 1.1rem; line-height: 2;">
            <li>Click the <strong>"Browse files"</strong> button above</li>
            <li>Select an ID card image (JPG, JPEG, or PNG)</li>
            <li>Use the <strong>Tabs</strong> above the image to see how OpenCV enhances the clarity</li>
            <li>Review and download the extracted information</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
