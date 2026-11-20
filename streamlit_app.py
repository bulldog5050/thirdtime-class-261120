import math
import random
import time

import streamlit as st


st.set_page_config(
    page_title="대칭 도형 스피드 게임",
    page_icon="🔷",
    layout="centered",
)

ANSWERS = ["선대칭도형", "점대칭도형", "둘 다 해당", "해당 없음"]

QUESTIONS = [
    {
        "type": "picture",
        "title": "동그란 원",
        "prompt": "이 도형은 어떤 대칭 도형일까요?",
        "answer": "둘 다 해당",
        "explanation": "원을 반으로 접으면 어느 방향이든 겹치고, 중심을 기준으로 180° 돌려도 겹쳐요.",
        "svg": (
            '<svg viewBox="0 0 280 190" role="img" aria-label="파란색 원">'
            '<circle cx="140" cy="95" r="63" fill="#60a5fa" stroke="#1d4ed8" stroke-width="5"/>'
            '<circle cx="140" cy="95" r="5" fill="#1e3a8a"/>'
            "</svg>"
        ),
    },
    {
        "type": "hint",
        "title": "힌트를 읽어 보세요",
        "prompt": "대칭축은 없지만, 도형의 한가운데를 중심으로 180° 돌리면 처음 모양과 정확히 겹쳐요.",
        "answer": "점대칭도형",
        "explanation": "점대칭도형은 대칭의 중심을 기준으로 180° 회전했을 때 처음 모양과 겹쳐요.",
    },
    {
        "type": "grid",
        "title": "모눈종이 도형",
        "prompt": "이 도형을 살펴보고 대칭의 종류를 골라 보세요.",
        "answer": "점대칭도형",
        "explanation": "평행사변형은 두 대각선이 만나는 점을 중심으로 180° 돌리면 겹쳐요. 일반적인 평행사변형에는 대칭축이 없어요.",
        "points": "75,90 165,65 205,125 115,150",
    },
    {
        "type": "picture",
        "title": "정삼각형",
        "prompt": "세 변의 길이가 모두 같은 정삼각형이에요.",
        "answer": "선대칭도형",
        "explanation": "정삼각형은 대칭축이 3개 있지만, 180° 돌렸을 때는 원래 모양과 겹치지 않아요.",
        "svg": (
            '<svg viewBox="0 0 280 190" role="img" aria-label="초록색 정삼각형">'
            '<polygon points="140,28 65,158 215,158" fill="#86efac" stroke="#15803d" stroke-width="5" stroke-linejoin="round"/>'
            "</svg>"
        ),
    },
    {
        "type": "grid",
        "title": "모눈종이 도형",
        "prompt": "대칭축과 180° 회전 여부를 생각해 보세요.",
        "answer": "둘 다 해당",
        "explanation": "이 정사각형은 가운데를 지나는 대칭축이 있고, 중심을 기준으로 180° 돌려도 겹쳐요.",
        "points": "80,55 180,55 180,155 80,155",
    },
    {
        "type": "hint",
        "title": "힌트를 읽어 보세요",
        "prompt": "대칭축은 1개이고, 대칭의 중심은 없어요. 180° 돌리면 처음 모양과 겹치지 않아요.",
        "answer": "선대칭도형",
        "explanation": "대칭축이 한 개 있으므로 선대칭도형이에요. 180° 회전으로 겹치지 않아 점대칭은 아니에요.",
    },
    {
        "type": "picture",
        "title": "기울어진 사각형",
        "prompt": "마주 보는 변이 서로 평행한 평행사변형이에요.",
        "answer": "점대칭도형",
        "explanation": "평행사변형은 대각선의 교점을 중심으로 180° 돌리면 겹치지만, 보통 대칭축은 없어요.",
        "svg": (
            '<svg viewBox="0 0 280 190" role="img" aria-label="주황색 평행사변형">'
            '<polygon points="90,40 220,40 190,150 60,150" fill="#fdba74" stroke="#c2410c" stroke-width="5" stroke-linejoin="round"/>'
            "</svg>"
        ),
    },
    {
        "type": "grid",
        "title": "모눈종이 도형",
        "prompt": "이 도형은 접었을 때 겹칠까요? 180° 돌렸을 때는 어떨까요?",
        "answer": "해당 없음",
        "explanation": "이 모양은 대칭축이 없고, 가운데를 중심으로 180° 돌려도 처음 모양과 겹치지 않아요.",
        "points": "75,65 175,65 175,105 125,105 125,155 75,155",
    },
    {
        "type": "picture",
        "title": "나뭇잎",
        "prompt": "잎맥을 가운데에 둔 낙엽 그림이에요. 어떤 대칭일까요?",
        "answer": "선대칭도형",
        "explanation": "이 나뭇잎 그림은 가운데 잎맥을 기준으로 좌우가 같아 선대칭이에요. 180° 돌리면 잎의 뾰족한 끝과 줄기 쪽이 바뀌어 겹치지 않아요.",
        "svg": (
            '<svg viewBox="0 0 280 190" role="img" aria-label="가운데 잎맥이 있는 초록색 낙엽">'
            '<path d="M140 160 C70 130 55 65 140 35 C225 65 210 130 140 160 Z" fill="#86efac" stroke="#15803d" stroke-width="5"/>'
            '<path d="M140 153 L140 46 M140 120 L101 91 M140 120 L179 91 M140 95 L112 70 M140 95 L168 70" fill="none" stroke="#15803d" stroke-width="3" stroke-linecap="round"/>'
            "</svg>"
        ),
    },
    {
        "type": "picture",
        "title": "네모난 창문",
        "prompt": "가운데 창틀이 있는 창문이에요. 창틀까지 포함해서 살펴보세요.",
        "answer": "둘 다 해당",
        "explanation": "창틀과 네 개의 유리창이 가운데를 기준으로 좌우·위아래가 같아요. 가운데를 중심으로 180° 돌려도 겹쳐요.",
        "svg": (
            '<svg viewBox="0 0 280 190" role="img" aria-label="네 개의 유리창으로 된 대칭 창문">'
            '<rect x="61" y="24" width="158" height="132" rx="5" fill="#dbeafe" stroke="#475569" stroke-width="8"/>'
            '<path d="M140 27 V153 M65 90 H215" stroke="#475569" stroke-width="8"/>'
            '<path d="M76 40 H127 V79 H76 Z M153 40 H204 V79 H153 Z M76 101 H127 V140 H76 Z M153 101 H204 V140 H153 Z" fill="#93c5fd"/>'
            '<path d="M47 160 H233" stroke="#64748b" stroke-width="8" stroke-linecap="round"/>'
            "</svg>"
        ),
    },
    {
        "type": "picture",
        "title": "손잡이가 있는 문",
        "prompt": "문에 달린 손잡이의 위치까지 살펴보세요.",
        "answer": "해당 없음",
        "explanation": "문짝만 보면 대칭처럼 보이지만 손잡이가 한쪽에 있어 대칭축이 없어요. 180° 돌리면 손잡이가 반대쪽으로 가서 겹치지 않아요.",
        "svg": (
            '<svg viewBox="0 0 280 190" role="img" aria-label="오른쪽에 손잡이가 달린 갈색 문">'
            '<rect x="77" y="18" width="126" height="156" rx="4" fill="#c08457" stroke="#78350f" stroke-width="6"/>'
            '<rect x="92" y="34" width="96" height="54" rx="3" fill="#d6a77a" stroke="#8b5e3c" stroke-width="4"/>'
            '<rect x="92" y="99" width="96" height="60" rx="3" fill="#d6a77a" stroke="#8b5e3c" stroke-width="4"/>'
            '<circle cx="181" cy="99" r="7" fill="#facc15" stroke="#854d0e" stroke-width="3"/>'
            "</svg>"
        ),
    },
    {
        "type": "picture",
        "title": "정면에서 본 건물",
        "prompt": "지붕과 창문이 있는 건물의 정면 그림이에요.",
        "answer": "선대칭도형",
        "explanation": "건물은 가운데를 지나는 세로선을 기준으로 좌우가 같아요. 하지만 지붕이 위에 있고 바닥이 아래에 있어 180° 돌리면 겹치지 않아요.",
        "svg": (
            '<svg viewBox="0 0 280 190" role="img" aria-label="대칭 지붕과 창문이 있는 집">'
            '<path d="M48 82 L140 24 L232 82 Z" fill="#fca5a5" stroke="#b91c1c" stroke-width="5" stroke-linejoin="round"/>'
            '<rect x="65" y="80" width="150" height="92" fill="#fde68a" stroke="#92400e" stroke-width="5"/>'
            '<rect x="82" y="97" width="40" height="34" fill="#bfdbfe" stroke="#475569" stroke-width="4"/>'
            '<path d="M102 98 V130 M84 114 H120" stroke="#475569" stroke-width="3"/>'
            '<rect x="158" y="97" width="40" height="34" fill="#bfdbfe" stroke="#475569" stroke-width="4"/>'
            '<path d="M178 98 V130 M160 114 H196" stroke="#475569" stroke-width="3"/>'
            '<rect x="123" y="132" width="34" height="40" fill="#c08457" stroke="#78350f" stroke-width="4"/>'
            "</svg>"
        ),
    },
    {
        "type": "picture",
        "title": "나비",
        "prompt": "양쪽 날개 모양과 무늬를 비교해 보세요.",
        "answer": "선대칭도형",
        "explanation": "나비의 몸을 지나는 세로선을 기준으로 양쪽 날개와 무늬가 같아 선대칭이에요. 위아래가 바뀌는 180° 회전으로는 겹치지 않아요.",
        "svg": (
            '<svg viewBox="0 0 280 190" role="img" aria-label="좌우 날개가 대칭인 보라색 나비">'
            '<g fill="#c4b5fd" stroke="#6d28d9" stroke-width="4" stroke-linejoin="round">'
            '<path d="M138 88 C112 36 48 44 51 94 C53 124 98 133 138 108 Z"/>'
            '<path d="M138 108 C109 101 69 119 78 151 C86 176 119 160 138 126 Z"/>'
            '<g transform="translate(280 0) scale(-1 1)">'
            '<path d="M138 88 C112 36 48 44 51 94 C53 124 98 133 138 108 Z"/>'
            '<path d="M138 108 C109 101 69 119 78 151 C86 176 119 160 138 126 Z"/>'
            "</g></g>"
            '<path d="M140 80 C130 58 119 57 112 55 M140 80 C150 58 161 57 168 55" fill="none" stroke="#4c1d95" stroke-width="3" stroke-linecap="round"/>'
            '<ellipse cx="140" cy="119" rx="7" ry="39" fill="#7c3aed"/>'
            '<circle cx="95" cy="91" r="7" fill="#fef3c7"/><circle cx="185" cy="91" r="7" fill="#fef3c7"/>'
            '<circle cx="107" cy="140" r="6" fill="#fef3c7"/><circle cx="173" cy="140" r="6" fill="#fef3c7"/>'
            "</svg>"
        ),
    },
    {
        "type": "picture",
        "title": "대칭 로고 배지",
        "prompt": "가운데 별 모양이 있는 둥근 로고예요.",
        "answer": "둘 다 해당",
        "explanation": "원 테두리와 가운데 별은 여러 대칭축을 가지고, 중심을 기준으로 180° 돌려도 같은 모양이에요.",
        "svg": (
            '<svg viewBox="0 0 280 190" role="img" aria-label="대칭인 별 모양이 있는 파란색 원형 로고">'
            '<circle cx="140" cy="95" r="70" fill="#2563eb" stroke="#1e3a8a" stroke-width="6"/>'
            '<path d="M140 43 L153 78 L190 79 L161 102 L171 139 L140 118 L109 139 L119 102 L90 79 L127 78 Z" fill="#fde047" stroke="#fef3c7" stroke-width="4" stroke-linejoin="round"/>'
            '<circle cx="140" cy="94" r="7" fill="#1e3a8a"/>'
            "</svg>"
        ),
    },
]


def grid_svg(points: str) -> str:
    return (
        '<svg viewBox="0 0 280 210" role="img" aria-label="모눈종이 위의 도형">'
        "<defs><pattern id=\"grid\" width=\"25\" height=\"25\" patternUnits=\"userSpaceOnUse\">"
        '<path d="M 25 0 L 0 0 0 25" fill="none" stroke="#cbd5e1" stroke-width="1"/>'
        "</pattern></defs>"
        '<rect x="20" y="15" width="240" height="180" rx="8" fill="#f8fafc"/>'
        '<rect x="20" y="15" width="240" height="180" rx="8" fill="url(#grid)"/>'
        f'<polygon points="{points}" fill="#a5b4fc" fill-opacity="0.8" stroke="#4338ca" stroke-width="4" stroke-linejoin="round"/>'
        "</svg>"
    )


def start_game() -> None:
    duration = st.session_state.time_limit
    st.session_state.questions = random.sample(QUESTIONS, len(QUESTIONS))
    st.session_state.question_index = 0
    st.session_state.score = 0
    st.session_state.combo = 0
    st.session_state.best_combo = 0
    st.session_state.correct_count = 0
    st.session_state.answered = False
    st.session_state.feedback = None
    st.session_state.celebration_until = None
    st.session_state.game_duration = duration
    st.session_state.deadline = time.time() + duration
    st.session_state.game_status = "playing"


def submit_answer(answer: str) -> None:
    question = st.session_state.questions[st.session_state.question_index]
    is_correct = answer == question["answer"]
    st.session_state.answered = True
    st.session_state.feedback = {
        "correct": is_correct,
        "explanation": question["explanation"],
    }

    if is_correct:
        st.session_state.score += 10
        st.session_state.celebration_until = time.time() + 2.5
        st.session_state.combo += 1
        st.session_state.best_combo = max(
            st.session_state.best_combo, st.session_state.combo
        )
        st.session_state.correct_count += 1
    else:
        st.session_state.combo = 0


def next_question() -> None:
    st.session_state.question_index += 1
    st.session_state.answered = False
    st.session_state.feedback = None
    st.session_state.celebration_until = None
    if st.session_state.question_index >= len(st.session_state.questions):
        st.session_state.game_status = "finished"


def show_question(question: dict) -> None:
    feedback = st.session_state.get("feedback")
    correct_class = " correct" if feedback and feedback["correct"] else ""

    if question["type"] == "hint":
        st.markdown(
            f'<div class="hint-card{correct_class}"><div class="hint-icon">💡</div>'
            f'<div>{question["prompt"]}</div></div>',
            unsafe_allow_html=True,
        )
    elif question["type"] == "grid":
        st.markdown(
            f'<div class="visual-card{correct_class}">{grid_svg(question["points"])}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<p class="prompt{correct_class}">{question["prompt"]}</p>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="visual-card{correct_class}">{question["svg"]}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<p class="prompt{correct_class}">{question["prompt"]}</p>',
            unsafe_allow_html=True,
        )


st.markdown(
    """
    <style>
    .block-container { max-width: 860px; padding-top: 2rem; }
    h1 { font-size: 2.45rem !important; color: #172554; }
    .subtitle { color: #475569; font-size: 1.15rem; margin-top: -0.5rem; }
    .visual-card {
        display: flex; justify-content: center; align-items: center;
        background: #f1f5f9; border: 2px solid #e2e8f0; border-radius: 22px;
        padding: 14px; margin: 12px 0;
    }
    .visual-card svg { width: min(100%, 430px); height: auto; }
    .visual-card.correct {
        background: #dcfce7; border-color: #22c55e;
        box-shadow: 0 0 0 5px rgba(34, 197, 94, 0.14);
    }
    .hint-card {
        min-height: 210px; display: flex; flex-direction: column;
        justify-content: center; align-items: center; gap: 12px;
        background: #fff7ed; border: 2px solid #fed7aa; border-radius: 22px;
        padding: 28px; text-align: center; font-size: 1.35rem; font-weight: 650;
        color: #7c2d12; margin: 12px 0;
    }
    .hint-icon { font-size: 2.8rem; }
    .prompt { text-align: center; font-size: 1.2rem; color: #334155; font-weight: 600; }
    .hint-card.correct {
        background: #dcfce7; border-color: #22c55e; color: #166534;
        box-shadow: 0 0 0 5px rgba(34, 197, 94, 0.14);
    }
    .prompt.correct { color: #15803d; }
    .celebration-curtain {
        position: fixed; inset: 0; z-index: 9999; pointer-events: none;
        display: flex; flex-wrap: wrap; align-content: space-around;
        justify-content: space-around; overflow: hidden; padding: 1rem;
        background: rgba(34, 197, 94, 0.12);
        font-size: clamp(2rem, 6vw, 4.5rem);
        animation: curtain-drop 2.5s ease-out both;
    }
    @keyframes curtain-drop {
        from { transform: translateY(-100%); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    div.stButton > button {
        min-height: 58px; border-radius: 14px; font-size: 1.08rem;
        font-weight: 700; border: 2px solid #cbd5e1;
    }
    div.stButton > button:hover { border-color: #4f46e5; color: #3730a3; }
    .result-card {
        padding: 24px; border-radius: 20px; background: #eff6ff;
        border: 2px solid #bfdbfe; text-align: center; margin: 16px 0;
    }
    .result-score { font-size: 2.7rem; font-weight: 800; color: #1d4ed8; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🔷 대칭 도형 스피드 게임")
st.markdown(
    '<p class="subtitle">그림과 힌트를 보고 대칭 도형의 종류를 빠르게 맞혀 보세요!</p>',
    unsafe_allow_html=True,
)

if "game_status" not in st.session_state:
    st.session_state.game_status = "ready"

if st.session_state.game_status == "ready":
    st.markdown("### 게임 준비")
    st.write("제한 시간 안에 문제를 풀어 점수를 모아 보세요. 정답은 10점!")
    st.selectbox("제한 시간", [15, 20, 30, 60], index=3, format_func=lambda value: f"{value}초", key="time_limit")
    st.button("게임 시작하기 🚀", type="primary", use_container_width=True, on_click=start_game)

elif st.session_state.game_status == "playing":

    @st.fragment(run_every="1s")
    def game_screen():
        if st.session_state.game_status != "playing":
            st.rerun()

        remaining = max(0, math.ceil(st.session_state.deadline - time.time()))
        if remaining == 0:
            st.session_state.game_status = "finished"
            st.rerun()

        total = st.session_state.game_duration
        st.progress(remaining / total, text=f"⏱️ 남은 시간: {remaining}초")

        question = st.session_state.questions[st.session_state.question_index]
        st.caption(
            f"문제 {st.session_state.question_index + 1} / {len(st.session_state.questions)}"
        )
        st.markdown(f"### {question['title']}")
        show_question(question)

        st.markdown("#### 정답을 골라 주세요")
        for row in (ANSWERS[:2], ANSWERS[2:]):
            columns = st.columns(2)
            for column, answer in zip(columns, row):
                with column:
                    st.button(
                        answer,
                        key=f"answer_{st.session_state.question_index}_{answer}",
                        use_container_width=True,
                        disabled=st.session_state.answered,
                        on_click=submit_answer,
                        args=(answer,),
                    )

        if st.session_state.answered:
            feedback = st.session_state.feedback
            if feedback["correct"]:
                st.success(f"정답이에요! 🎉  {feedback['explanation']}")
                if time.time() < st.session_state.celebration_until:
                    st.markdown(
                        '<div class="celebration-curtain" aria-hidden="true">'
                        + "🥳 🎉 ✨ 🎊 " * 32
                        + "</div>",
                        unsafe_allow_html=True,
                    )
            else:
                st.error(
                    f"아쉬워요! 정답은 **{question['answer']}**예요. "
                    f"{feedback['explanation']}"
                )
            st.button(
                "다음 문제 ➜",
                type="primary",
                use_container_width=True,
                on_click=next_question,
            )

        st.divider()
        score_col, combo_col = st.columns(2)
        score_col.metric("점수", f"{st.session_state.score}점")
        combo_col.metric("연속 정답", f"{st.session_state.combo} 🔥")

    game_screen()

else:
    total_questions = len(st.session_state.questions)
    accuracy = round(st.session_state.correct_count / total_questions * 100)
    st.markdown(
        f'<div class="result-card"><div>🏁 게임 끝!</div>'
        f'<div class="result-score">{st.session_state.score}점</div>'
        f'<div>정답 {st.session_state.correct_count} / {total_questions}문제 '
        f'· 정답률 {accuracy}%</div></div>',
        unsafe_allow_html=True,
    )
    result_col1, result_col2 = st.columns(2)
    result_col1.metric("맞힌 문제", f"{st.session_state.correct_count}개")
    result_col2.metric("최고 연속 정답", f"{st.session_state.best_combo}개")
    st.info("잘했어요! 틀린 문제의 해설을 다시 떠올리며 대칭의 성질을 복습해 보세요.")
    if st.button("다시 도전하기 🔁", type="primary", use_container_width=True):
        st.session_state.game_status = "ready"
        st.rerun()
