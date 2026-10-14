import random
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="두더지 잡기 게임", page_icon="🐹")

BASE_DIR = Path(__file__).parent
HOLE_IMAGE = BASE_DIR / "hole.png"
MOLE_IMAGE = BASE_DIR / "img.png"

if "mole_hole" not in st.session_state:
    st.session_state.mole_hole = random.randrange(9)
if "mole_round" not in st.session_state:
    st.session_state.mole_round = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "caught_mole" not in st.session_state:
    st.session_state.caught_mole = False


def handle_hole_click(hole_number, mole_round):
    if hole_number != st.session_state.mole_hole:
        return
    if mole_round != st.session_state.mole_round:
        return

    st.session_state.score += 10
    st.session_state.caught_mole = True
    choices = [number for number in range(9) if number != hole_number]
    st.session_state.mole_hole = random.choice(choices)
    st.session_state.mole_round += 1


st.title("두더지 잡기 게임")
st.write("두더지를 클릭해 보세요!")
st.metric("현재 점수", f"{st.session_state.score}점")

for row_start in range(0, 9, 3):
    columns = st.columns(3)
    for column_number, column in enumerate(columns):
        hole_number = row_start + column_number
        has_mole = hole_number == st.session_state.mole_hole

        with column:
            image = MOLE_IMAGE if has_mole else HOLE_IMAGE
            st.image(str(image), use_container_width=True)

            button_label = "두더지 잡기" if has_mole else "빈 구멍"
            st.button(
                button_label,
                key=f"hole-{hole_number}",
                use_container_width=True,
                on_click=handle_hole_click,
                args=(hole_number, st.session_state.mole_round),
            )

if st.session_state.caught_mole:
    st.success("두더지를 잡았습니다!")
