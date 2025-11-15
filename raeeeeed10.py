import streamlit as st
import base64

# ================= إعداد عام للصفحة ================
st.set_page_config(
    page_title="منصّة دعم القلق والاكتئاب",
    page_icon="💚",
    layout="centered"
)

# ====================== إعداد روابط فيديوهات النتائج ======================

# قلق إيجابي (نتيجة منخفضة)
ANXIETY_POSITIVE = "Pcho3GzMlg4"

# قلق سلبي (نتيجة عالية)
ANXIETY_NEGATIVE = "A0vYcXStfQw"

# اكتئاب إيجابي (نتيجة منخفضة)
DEPRESSION_POSITIVE = "0Rs5hqrWt_s"

# اكتئاب سلبي (نتيجة عالية)
DEPRESSION_NEGATIVE = "PHdTOBJOp0g"

# ====================== تنسيقات عامة (CSS) ======================
def set_style():
    st.markdown("""
    <style>
        .main {
            background-color: #f5f7fb;
            font-family: "Cairo", sans-serif;
        }

        .app-header {
            background: linear-gradient(90deg, #1f4e79, #3b82f6);
            padding: 16px 24px;
            border-radius: 18px;
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 24px;
            color: #ffffff;
        }

        .logo-circle {
            width: 54px;
            height: 54px;
            border-radius: 50%;
            background: rgba(255,255,255,0.15);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
        }

        .header-title {
            font-size: 24px;
            font-weight: 700;
        }

        .header-subtitle {
            font-size: 14px;
            opacity: 0.9;
        }

        .page-note {
            text-align: center;
            color: #555;
            margin-bottom: 10px;
        }

        .question {
            font-size: 18px;
            color: #222;
            margin-top: 12px;
            margin-bottom: 4px;
        }
    </style>
    """, unsafe_allow_html=True)


set_style()

# ====================== هيدر / شعار المنصّة ======================
st.markdown(
    """
    <div class="app-header">
        <div class="logo-circle">🧠</div>
        <div>
            <div class="header-title">منصّة دعم القلق والاكتئاب</div>
            <div class="header-subtitle">
                تقييم ذاتي رسمي عالمي مع فيديوهات دعم نفسية مخصّصة لحالتك 💚
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "<div class='page-note'>هذه الأداة لا تُعتبر تشخيصًا طبيًا، وإنما وسيلة لمساعدتك على فهم حالتك الحالية.</div>",
    unsafe_allow_html=True,
)

# ====================== فيديو المقدّمة اوتوماتيكي ======================
def render_intro_video():
    video_path = "نص فقرتك.mp4"  # اسم ملف الفيديو كما هو في GitHub
    try:
        with open(video_path, "rb") as video_file:
            video_bytes = video_file.read()
        b64 = base64.b64encode(video_bytes).decode()
        video_html = f"""
        <video autoplay muted loop playsinline
               style="width:100%; border-radius:18px; box-shadow:0 0 15px rgba(0,0,0,0.18);">
            <source src="data:video/mp4;base64,{b64}" type="video/mp4">
            متصفحك لا يدعم تشغيل الفيديو.
        </video>
        """
        st.markdown(video_html, unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("لم يتم العثور على ملف المقدمة (نص فقرتك.mp4). تأكد من أنه داخل المستودع.")

render_intro_video()

st.write("---")

# ====================== دالة تشغيل يوتيوب AutoPlay ======================
def autoplay_youtube(video_id: str):
    st.markdown(
        f"""
        <iframe width="100%" height="360"
            src="https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1&controls=0&loop=1&playlist={video_id}"
            title="YouTube video player"
            frameborder="0"
            allow="autoplay; encrypted-media; picture-in-picture"
            allowfullscreen>
        </iframe>
        """,
        unsafe_allow_html=True,
    )

# ====================== اختيار نوع الاستبيان ======================
st.subheader("📝 اختر نوع التقييم العالمي")

scale_type = st.radio(
    "اختر نوع التقييم",
    ["استبيان القلق العالمي (GAD-7)", "استبيان الاكتئاب العالمي (PHQ-9)"],
    horizontal=True,
    label_visibility="collapsed"
)

st.write("اختر الإجابة التي تعبّر عنك خلال **الأسبوعين الماضيين**:")

# ====================== أسئلة الاستبيانات ======================

gad7_questions = [
    "كم مرة شعرت بالتوتر أو القلق أو العصبية؟",
    "كم مرة لم تستطع التوقف عن القلق أو السيطرة عليه؟",
    "كم مرة شعرت بالقلق الشديد بشأن أشياء مختلفة؟",
    "كم مرة كان من الصعب عليك الاسترخاء؟",
    "كم مرة كنت منزعجًا لدرجة لا تستطيع فيها الجلوس بهدوء؟",
    "كم مرة شعرت بالانزعاج أو الضيق بسهولة؟",
    "كم مرة شعرت بالخوف وكأن شيئًا سيئًا قد يحدث؟",
]

phq9_questions = [
    "قلة الاهتمام أو المتعة في الأنشطة اليومية.",
    "الشعور بالحزن أو الاكتئاب أو اليأس.",
    "صعوبة النوم أو النوم المفرط.",
    "الشعور بالتعب أو انخفاض الطاقة.",
    "قلة الشهية أو الإفراط في الأكل.",
    "الشعور بعدم القيمة أو الفشل.",
    "صعوبة التركيز على الأنشطة اليومية.",
    "الحركة البطيئة جدًا أو العصبية الزائدة.",
    "أفكار عن إيذاء الذات أو تمني الموت.",
]

options = ["أبدًا", "عدة أيام", "أكثر من نصف الأيام", "تقريبًا كل يوم"]
score_map = {"أبدًا": 0, "عدة أيام": 1, "أكثر من نصف الأيام": 2, "تقريبًا كل يوم": 3}

# ====================== عرض الأسئلة ======================

answers = []

if scale_type == "استبيان القلق العالمي (GAD-7)":
    for i, q in enumerate(gad7_questions, start=1):
        st.markdown(f"<div class='question'>{i}. {q}</div>", unsafe_allow_html=True)
        ans = st.radio(
            label=f"gad_q{i}",
            options=options,
            index=0,
            horizontal=True,
            label_visibility="collapsed",
            key=f"gad_q{i}"
        )
        answers.append(ans)
else:
    for i, q in enumerate(phq9_questions, start=1):
        st.markdown(f"<div class='question'>{i}. {q}</div>", unsafe_allow_html=True)
        ans = st.radio(
            label=f"phq_q{i}",
            options=options,
            index=0,
            horizontal=True,
            label_visibility="collapsed",
            key=f"phq_q{i}"
        )
        answers.append(ans)

score = sum(score_map[a] for a in answers)

st.write("---")

# ====================== حساب النتيجة وعرض فيديو مناسب ======================

if st.button("عرض النتيجة 🎯"):
    st.write("## نتيجتك:")

    # ======== نتائج القلق GAD-7 ========
    if scale_type == "استبيان القلق العالمي (GAD-7)":

        if score <= 4:
            st.success(f"مستوى القلق لديك منخفض (الدرجة: {score}/21).")
            autoplay_youtube(ANXIETY_POSITIVE)

        elif 5 <= score <= 9:
            st.info(f"قلق بسيط (الدرجة: {score}/21).")
            autoplay_youtube(ANXIETY_POSITIVE)

        elif 10 <= score <= 14:
            st.warning(f"قلق متوسط (الدرجة: {score}/21).")
            autoplay_youtube(ANXIETY_NEGATIVE)

        else:
            st.error(f"قلق شديد (الدرجة: {score}/21).")
            autoplay_youtube(ANXIETY_NEGATIVE)

    # ======== نتائج الاكتئاب PHQ-9 ========
    else:

        if score <= 4:
            st.success(f"أعراض اكتئاب منخفضة (الدرجة: {score}/27).")
            autoplay_youtube(DEPRESSION_POSITIVE)

        elif 5 <= score <= 9:
            st.info(f"اكتئاب خفيف (الدرجة: {score}/27).")
            autoplay_youtube(DEPRESSION_POSITIVE)

        elif 10 <= score <= 14:
            st.warning(f"اكتئاب متوسط (الدرجة: {score}/27).")
            autoplay_youtube(DEPRESSION_NEGATIVE)

        elif 15 <= score <= 19:
            st.error(f"اكتئاب متوسط إلى شديد (الدرجة: {score}/27).")
            autoplay_youtube(DEPRESSION_NEGATIVE)

        else:
            st.error(f"أعراض اكتئاب شديدة جدًا (الدرجة: {score}/27).")
            autoplay_youtube(DEPRESSION_NEGATIVE)

    st.info("⚕️ هذه الأداة تقييم أولي ولا تُغني عن زيارة مختص نفسي عند الحاجة.")
