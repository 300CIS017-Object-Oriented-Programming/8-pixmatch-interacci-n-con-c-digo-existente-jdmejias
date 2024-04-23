import streamlit as st
import os
import time as tm
import random
import base64
import json
from PIL import Image
from streamlit_autorefresh import st_autorefresh

# Configuración de la página, aqui se establece el ancho, el titulo, etc.
st.set_page_config(
    page_title="PixMatch",
    page_icon="🕹️",
    layout="wide",
    initial_sidebar_state="expanded"
)

v_drive = os.path.splitdrive(os.getcwd())[0]
locate_current_folder = "./"

# Definición de estilos CSS y emojis HTML para usar en la interfaz
big_emoji = """
              <span style='font-size: 140px;
              border-radius: 7px;
              text-align: center;
              display: inline;
              padding: 3px 0.4em;'> 
              |fill_variable|
              </span>"""
#el 3 se refiere al top y buttom y el 0,4m al left and right.
pressed_emoji = """
                  <span style='font-size: 24px;
                  border-radius: 7px;
                  text-align: center;
                  display: inline;
                  padding: 3px 0.2em;'> 
                  |fill_variable|
                  </span>"""
#el 3 se refiere al top y buttom y el 0,2m al left and right.
horizontal_line = """
                    <hr style='margin-top: 0; 
                     margin-bottom: 0; 
                     height: 1px; 
                     border: 1px solid #635985;
                     '><br>"""  # thin divider line

purple_button_color = """
                    <style>
                        div.stButton > button:first-child {background-color: #4b0082; color:#ffffff;}
                        div.stButton > button:hover {background-color: RGB(0,112,192); color:#ffffff;}
                        div.stButton > button:focus {background-color: RGB(47,117,181); color:#ffffff;}
                    </style>
                    """
# Inicialización de variables de estado de la sesión
mystate = st.session_state
if "expired_cells" not in mystate: mystate.expired_cells = []
if "myscore" not in mystate: mystate.myscore = 0
if "plyrbtns" not in mystate: mystate.plyrbtns = {}
if "sidebar_emoji" not in mystate: mystate.sidebar_emoji = ''
if "emoji_bank" not in mystate: mystate.emoji_bank = []
if "GameDetails" not in mystate: mystate.GameDetails = ['Medium', 6, 7,'']  # difficulty level, sec interval for autogen, total_cells_per_row_or_col, player name

# common functions

def reduce_gap_from_page_top(wch_section='main page'):
    """
    Qué hace: educe el espacio en blanco en la parte superior de la página.
    Parámetros: wch_section (str): La sección de la página para la cual se desea reducir el espacio en blanco.
    Retorna: None
    """
    if wch_section == 'main page':
        st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", True)  # main area
    elif wch_section == 'sidebar':
        st.markdown(" <style> div[class^='st-emotion-cache-10oheav'] { padding-top: 0rem; } </style> ", True)  # sidebar
    elif wch_section == 'all':
        st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", True)  # main area
        st.markdown(" <style> div[class^='st-emotion-cache-10oheav'] { padding-top: 0rem; } </style> ", True)  # sidebar


def leaderboard(what_to_do):
    """
    Qué hace:Esta función gestiona la funcionalidad del marcador de posición, incluida la creación, escritura y lectura.
    Parámetros: what_to_do (str): La acción que se debe realizar en el marcador de posición.
    Retorna: None
    """
    if what_to_do == 'create':
        if mystate.GameDetails[3] != '':
            if os.path.isfile(locate_current_folder + 'leaderboard.json') == False:
                tmpdict = {}
                json.dump(tmpdict, open(locate_current_folder + 'leaderboard.json', 'w'))  # write file

    elif what_to_do == 'write':
        if mystate.GameDetails[3] != '':  # record in leaderboard only if player name is provided
            if os.path.isfile(locate_current_folder + 'leaderboard.json'):
                leaderboard = json.load(open(locate_current_folder + 'leaderboard.json'))  # read file
                leaderboard_dict_lngth = len(leaderboard)

                leaderboard[str(leaderboard_dict_lngth + 1)] = {'NameCountry': mystate.GameDetails[3],
                                                                'HighestScore': mystate.myscore}
                leaderboard = dict(sorted(leaderboard.items(), key=lambda item: item[1]['HighestScore'], reverse=True))  # sort desc
                if len(leaderboard) > 4:
                    for i in range(len(leaderboard) - 4): leaderboard.popitem()  # rmv last kdict ey

                json.dump(leaderboard, open(locate_current_folder + 'leaderboard.json', 'w'))  # write file

    elif what_to_do == 'read':
        if mystate.GameDetails[3] != '':  # record in leaderboard only if player name is provided
            if os.path.isfile(locate_current_folder + 'leaderboard.json'):
                leaderboard = json.load(open(locate_current_folder + 'leaderboard.json'))  # read file
                leaderboard = dict(sorted(leaderboard.items(), key=lambda item: item[1]['HighestScore'], reverse=True))  # sort desc

                sc0, sc1, sc2, sc3, column_four = st.columns((2, 3, 3, 3, 3))
                rknt = 0
                for vkey in leaderboard.keys():
                    if leaderboard[vkey]['NameCountry'] != '':
                        rknt += 1
                        if rknt == 1:
                            sc0.write('🏆 Past Winners:')
                            sc1.write(f"🥇 | {leaderboard[vkey]['NameCountry']}: :red[{leaderboard[vkey]['HighestScore']}]")
                        elif rknt == 2:
                            sc2.write(f"🥈 | {leaderboard[vkey]['NameCountry']}: :red[{leaderboard[vkey]['HighestScore']}]")
                        elif rknt == 3:
                            sc3.write(f"🥉 | {leaderboard[vkey]['NameCountry']}: :red[{leaderboard[vkey]['HighestScore']}]")
                        elif rknt == 4:
                            #aladir una columna más para el cuarto jugador
                            column_four.write(f"🏅 | {leaderboard[vkey]['NameCountry']}: :red[{leaderboard[vkey]['HighestScore']}]")


def initial_page():
    # funcion para incializar la pagina, tambien las intrucciones y imagenes.
    with st.sidebar:
        st.subheader("🖼️ Pix Match:")
        st.markdown(horizontal_line, True)

        # sidebarlogo = Image.open('sidebarlogo.jpg').resize((300, 420))
        side_bar_logo = Image.open('sidebarlogo.jpg').resize((300, 390))
        st.image(side_bar_logo, use_column_width='auto')

    # ViewHelp
    hlp_dtl = f"""<span style="font-size: 26px;">
    <ol>
    <li style="font-size:15px";>Game play opens with (a) a sidebar picture and (b) a N x N grid of picture buttons, where N=6:Easy, N=7:Medium, N=8:Hard.</li>
    <li style="font-size:15px";>You need to match the sidebar picture with a grid picture button, by pressing the (matching) button (as quickly as possible).</li>
    <li style="font-size:15px";>Each correct picture match will earn you <strong>+N</strong> points (where N=5:Easy, N=3:Medium, N=1:Hard); each incorrect picture match will earn you <strong>-1</strong> point.</li>
    <li style="font-size:15px";>The sidebar picture and the grid pictures will dynamically regenerate after a fixed seconds interval (Easy=8, Medium=6, Hard=5). Each regeneration will have a penalty of <strong>-1</strong> point</li>
    <li style="font-size:15px";>Each of the grid buttons can only be pressed once during the entire game.</li>
    <li style="font-size:15px";>The game completes when all the grid buttons are pressed.</li>
    <li style="font-size:15px";>At the end of the game, if you have a positive score, you will have <strong>won</strong>; otherwise, you will have <strong>lost</strong>.</li>
    </ol></span>"""

    sc1, sc2 = st.columns(2)
    random.seed()
    GameHelpImg = locate_current_folder + random.choice(["MainImg1.jpg", "MainImg2.jpg", "MainImg3.jpg", "MainImg4.jpg"])
    GameHelpImg = Image.open(GameHelpImg).resize((550, 550))
    sc2.image(GameHelpImg, use_column_width='auto')

    sc1.subheader('Rules | Playing Instructions:')
    sc1.markdown(horizontal_line, True)
    sc1.markdown(hlp_dtl, unsafe_allow_html=True)
    st.markdown(horizontal_line, True)

    author_dtl = "<strong>Happy Playing: 😎 Shawn Pereira: shawnpereira1969@gmail.com</strong>"
    st.markdown(author_dtl, unsafe_allow_html=True)

def read_picture_file(wch_fl):
    """
    Qué hace: Lee un archivo de imagen y lo convierte en una cadena codificada en base64.
    Parámetros:
    - wch_fl (str): La ruta del archivo de imagen que se desea leer.
    Retorna:
    - str: Una cadena codificada en base64 que representa la imagen.
    """
    try:
        pxfl = f"{locate_current_folder}{wch_fl}"
        return base64.b64encode(open(pxfl, 'rb').read()).decode()

    except:
        return ""

def pressed_check(vcell):
    """
    Qué hace: Verifica si un botón ha sido presionado y actualiza el puntaje del juego.
    Parámetros:
    - vcell (str): La celda del botón que se está verificando.
    Retorna: None
    """
    if mystate.plyrbtns[vcell]['isPressed'] == False:
        mystate.plyrbtns[vcell]['isPressed'] = True
        mystate.expired_cells.append(vcell)

        if mystate.plyrbtns[vcell]['eMoji'] == mystate.sidebar_emoji:
            mystate.plyrbtns[vcell]['isTrueFalse'] = True
            mystate.myscore += 5

            if mystate.GameDetails[0] == 'Easy':
                mystate.myscore += 5
            elif mystate.GameDetails[0] == 'Medium':
                mystate.myscore += 3
            elif mystate.GameDetails[0] == 'Hard':
                mystate.myscore += 1

        else:
            mystate.plyrbtns[vcell]['isTrueFalse'] = False
            mystate.myscore -= 1


def reset_board():
    # funcion para restablecer el tablero del juego y elige un emoji de la barra lateral aleatoriamente.
    total_cells_per_row_or_col = mystate.GameDetails[2]

    sidebar_emoji_no = random.randint(1, len(mystate.emoji_bank)) - 1
    mystate.sidebar_emoji = mystate.emoji_bank[sidebar_emoji_no]

    sidebar_emoji_in_list = False
    for vcell in range(1, ((total_cells_per_row_or_col ** 2) + 1)):
        rndm_no = random.randint(1, len(mystate.emoji_bank)) - 1
        if mystate.plyrbtns[vcell]['isPressed'] == False:
            vemoji = mystate.emoji_bank[rndm_no]
            mystate.plyrbtns[vcell]['eMoji'] = vemoji
            if vemoji == mystate.sidebar_emoji: sidebar_emoji_in_list = True

    if sidebar_emoji_in_list == False:  # sidebar pix is not on any button; add pix randomly
        tlst = [x for x in range(1, ((total_cells_per_row_or_col ** 2) + 1))]
        flst = [x for x in tlst if x not in mystate.expired_cells]
        if len(flst) > 0:
            lptr = random.randint(0, (len(flst) - 1))
            lptr = flst[lptr]
            mystate.plyrbtns[lptr]['eMoji'] = mystate.sidebar_emoji


def pre_new_game():
    # funcion para inicializar el pre juego, es decir, los elementos necesarios que usaremos en el juego.
    total_cells_per_row_or_col = mystate.GameDetails[2]
    mystate.expired_cells = []
    mystate.myscore = 0

    foxes = ['😺', '😸', '😹', '😻', '😼', '😽', '🙀', '😿', '😾']
    emojis = ['😃', '😄', '😁', '😆', '😅', '😂', '🤣', '😊', '😇', '🙂', '🙃', '😉', '😌', '😍', '🥰', '😘', '😗', '😙', '😚', '😋', '😛',
              '😝', '😜', '🤪', '🤨', '🧐', '🤓', '😎', '🤩', '🥳', '😏', '😒', '😞', '😔', '😟', '😕', '🙁', '☹️', '😣', '😖', '😫', '😩',
              '🥺', '😢', '😠', '😳', '😥', '😓', '🤗', '🤔', '🤭', '🤫', '🤥', '😶', '😐', '😑', '😬', '🙄', '😯', '😧', '😮', '😲', '🥱',
              '😴', '🤤', '😪', '😵', '🤐', '🥴', '🤒']
    humans = ['👶', '👧', '🧒', '👦', '👩', '🧑', '👨', '👩‍🦱', '👨‍🦱', '👩‍🦰', '‍👨', '👱', '👩', '👱', '👩‍', '👨‍🦳', '👩‍🦲', '👵', '🧓',
              '👴', '👲', '👳']
    foods = ['🍏', '🍎', '🍐', '🍊', '🍋', '🍌', '🍉', '🍇', '🍓', '🍈', '🍒', '🍑', '🥭', '🍍', '🥥', '🥝', '🍅', '🍆', '🥑', '🥦', '🥬',
             '🥒', '🌽', '🥕', '🧄', '🧅', '🥔', '🍠', '🥐', '🥯', '🍞', '🥖', '🥨', '🧀', '🥚', '🍳', '🧈', '🥞', '🧇', '🥓', '🥩', '🍗',
             '🍖', '🦴', '🌭', '🍔', '🍟', '🍕']
    clocks = ['🕓', '🕒', '🕑', '🕘', '🕛', '🕚', '🕖', '🕙', '🕔', '🕤', '🕠', '🕕', '🕣', '🕞', '🕟', '🕜', '🕢', '🕦']
    hands = ['🤚', '🖐', '✋', '🖖', '👌', '🤏', '✌️', '🤞', '🤟', '🤘', '🤙', '👈', '👉', '👆', '🖕', '👇', '☝️', '👍', '👎', '✊', '👊',
             '🤛', '🤜', '👏', '🙌', '🤲', '🤝', '🤚🏻', '🖐🏻', '✋🏻', '🖖🏻', '👌🏻', '🤏🏻', '✌🏻', '🤞🏻', '🤟🏻', '🤘🏻', '🤙🏻', '👈🏻',
             '👉🏻', '👆🏻', '🖕🏻', '👇🏻', '☝🏻', '👍🏻', '👎🏻', '✊🏻', '👊🏻', '🤛🏻', '🤜🏻', '👏🏻', '🙌🏻', '🤚🏽', '🖐🏽', '✋🏽', '🖖🏽',
             '👌🏽', '🤏🏽', '✌🏽', '🤞🏽', '🤟🏽', '🤘🏽', '🤙🏽', '👈🏽', '👉🏽', '👆🏽', '🖕🏽', '👇🏽', '☝🏽', '👍🏽', '👎🏽', '✊🏽', '👊🏽',
             '🤛🏽', '🤜🏽', '👏🏽', '🙌🏽']
    animals = ['🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼', '🐨', '🐯', '🦁', '🐮', '🐷', '🐽', '🐸', '🐵', '🙈', '🙉', '🙊', '🐒', '🐔',
               '🐧', '🐦', '🐤', '🐣', '🐥', '🦆', '🦅', '🦉', '🦇', '🐺', '🐗', '🐴', '🦄', '🐝', '🐛', '🦋', '🐌', '🐞', '🐜', '🦟', '🦗',
               '🦂', '🐢', '🐍', '🦎', '🦖', '🦕', '🐙', '🦑', '🦐', '🦞', '🦀', '🐡', '🐠', '🐟', '🐬', '🐳', '🐋', '🦈', '🐊', '🐅', '🐆',
               '🦓', '🦍', '🦧', '🐘', '🦛', '🦏', '🐪', '🐫', '🦒', '🦘', '🐃', '🐂', '🐄', '🐎', '🐖', '🐏', '🐑', '🦙', '🐐', '🦌', '🐕',
               '🐩', '🦮', '🐕‍🦺', '🐈', '🐓', '🦃', '🦚', '🦜', '🦢', '🦩', '🐇', '🦝', '🦨', '🦦', '🦥', '🐁', '🐀', '🦔']
    vehicles = ['🚗', '🚕', '🚙', '🚌', '🚎', '🚓', '🚑', '🚒', '🚐', '🚚', '🚛', '🚜', '🦯', '🦽', '🦼', '🛴', '🚲', '🛵', '🛺', '🚔', '🚍',
                '🚘', '🚖', '🚡', '🚠', '🚟', '🚃', '🚋', '🚞', '🚝', '🚄', '🚅', '🚈', '🚂', '🚆', '🚇', '🚊', '🚉', '✈️', '🛫', '🛬',
                '💺', '🚀', '🛸', '🚁', '🛶', '⛵️', '🚤', '🛳', '⛴', '🚢']
    houses = ['🏠', '🏡', '🏘', '🏚', '🏗', '🏭', '🏢', '🏬', '🏣', '🏤', '🏥', '🏦', '🏨', '🏪', '🏫', '🏩', '💒', '🏛', '⛪️', '🕌', '🕍',
              '🛕']
    purple_signs = ['☮️', '✝️', '☪️', '☸️', '✡️', '🔯', '🕎', '☯️', '☦️', '🛐', '⛎', '♈️', '♉️', '♊️', '♋️', '♌️', '♍️',
                    '♎️', '♏️', '♐️', '♑️', '♒️', '♓️', '🆔', '🈳']
    red_signs = ['🈶', '🈚️', '🈸', '🈺', '🈷️', '✴️', '🉐', '㊙️', '㊗️', '🈴', '🈵', '🈹', '🈲', '🅰️', '🅱️', '🆎', '🆑', '🅾️', '🆘',
                 '🚼', '🛑', '⛔️', '📛', '🚫', '🚷', '🚯', '🚳', '🚱', '🔞', '📵', '🚭']
    blue_signs = ['🚾', '♿️', '🅿️', '🈂️', '🛂', '🛃', '🛄', '🛅', '🚹', '🚺', '🚻', '🚮', '🎦', '📶', '🈁', '🔣', '🔤', '🔡', '🔠', '🆖',
                  '🆗', '🆙', '🆒', '🆕', '🆓', '0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟',
                  '🔢', '⏏️', '▶️', '⏸', '⏯', '⏹', '⏺', '⏭', '⏮', '⏩', '⏪', '⏫', '⏬', '◀️', '🔼', '🔽', '➡️', '⬅️', '⬆️',
                  '⬇️', '↗️', '↘️', '↙️', '↖️', '↪️', '↩️', '⤴️', '⤵️', '🔀', '🔁', '🔂', '🔄', '🔃', '➿', '🔚', '🔙', '🔛',
                  '🔝', '🔜']
    moon = ['🌕', '🌔', '🌓', '🌗', '🌒', '🌖', '🌑', '🌜', '🌛', '🌙']

    random.seed()
    if mystate.GameDetails[0] == 'Easy':
        wch_bank = random.choice(['foods', 'moon', 'animals'])
        mystate.emoji_bank = locals()[wch_bank]

    elif mystate.GameDetails[0] == 'Medium':
        wch_bank = random.choice(
            ['foxes', 'emojis', 'humans', 'vehicles', 'houses', 'hands', 'purple_signs', 'red_signs', 'blue_signs'])
        mystate.emoji_bank = locals()[wch_bank]

    elif mystate.GameDetails[0] == 'Hard':
        wch_bank = random.choice(
            ['foxes', 'emojis', 'humans', 'foods', 'clocks', 'hands', 'animals', 'vehicles', 'houses', 'purple_signs',
             'red_signs', 'blue_signs', 'moon'])
        mystate.emoji_bank = locals()[wch_bank]

    mystate.plyrbtns = {}
    for vcell in range(1, ((total_cells_per_row_or_col ** 2) + 1)): mystate.plyrbtns[vcell] = {'isPressed': False,
                                                                                               'isTrueFalse': False,
                                                                                               'eMoji': ''}

def score_emoji():
    """
    Qué hace: Coloca un emoji dependiendo de la puntuación del juego.
    Parámetros: Ninguno
    Retorna: str: Un emoji correspondiente a la puntuación actual del juego.
    """
    if mystate.myscore == 0:
        return '😐'
    elif -5 <= mystate.myscore <= -1:
        return '😏'
    elif -10 <= mystate.myscore <= -6:
        return '☹️'
    elif mystate.myscore <= -11:
        return '😖'
    elif 1 <= mystate.myscore <= 5:
        return '🙂'
    elif 6 <= mystate.myscore <= 10:
        return '😊'
    elif mystate.myscore > 10:
        return '😁'


def new_game():
    # Funcion para iniciar un nuevo juego y mostrar la interfaz
    reset_board()
    total_cells_per_row_or_col = mystate.GameDetails[2]
    max_errors = (total_cells_per_row_or_col ** 2) // 2 + 1  # Calcular el número máximo de errores permitidos

    reduce_gap_from_page_top('sidebar')
    with st.sidebar:
        st.subheader(f"🖼️ Pix Match: {mystate.GameDetails[0]}")
        st.markdown(horizontal_line, True)

        st.markdown(big_emoji.replace('|fill_variable|', mystate.sidebar_emoji), True)

        aftimer = st_autorefresh(interval=(mystate.GameDetails[1] * 1000), key="aftmr")
        if aftimer > 0: mystate.myscore -= 1

        st.info(
            f"{score_emoji()} Score: {mystate.myscore} | Pending: {(total_cells_per_row_or_col ** 2) - len(mystate.expired_cells)}")

        st.markdown(horizontal_line, True)
        if st.button(f"🔙 Return to Main Page", use_container_width=True):
            mystate.runpage = main
            st.rerun()

    leaderboard('read')
    st.subheader("Picture Positions:")
    st.markdown(horizontal_line, True)

    # Set Board Dafaults
    st.markdown("<style> div[class^='css-1vbkxwb'] > p { font-size: 1.5rem; } </style> ",
                unsafe_allow_html=True)  # make button face big

    errors = 0  #inicializar en 0

    for i in range(1, (total_cells_per_row_or_col + 1)):
        tlst = ([1] * total_cells_per_row_or_col) + [2]  # 2 = rt side padding
        globals()['cols' + str(i)] = st.columns(tlst)

    for vcell in range(1, (total_cells_per_row_or_col ** 2) + 1):
        if 1 <= vcell <= (total_cells_per_row_or_col * 1):
            arr_ref = '1'
            mval = 0

        elif ((total_cells_per_row_or_col * 1) + 1) <= vcell <= (total_cells_per_row_or_col * 2):
            arr_ref = '2'
            mval = (total_cells_per_row_or_col * 1)

        elif ((total_cells_per_row_or_col * 2) + 1) <= vcell <= (total_cells_per_row_or_col * 3):
            arr_ref = '3'
            mval = (total_cells_per_row_or_col * 2)

        elif ((total_cells_per_row_or_col * 3) + 1) <= vcell <= (total_cells_per_row_or_col * 4):
            arr_ref = '4'
            mval = (total_cells_per_row_or_col * 3)

        elif ((total_cells_per_row_or_col * 4) + 1) <= vcell <= (total_cells_per_row_or_col * 5):
            arr_ref = '5'
            mval = (total_cells_per_row_or_col * 4)

        elif ((total_cells_per_row_or_col * 5) + 1) <= vcell <= (total_cells_per_row_or_col * 6):
            arr_ref = '6'
            mval = (total_cells_per_row_or_col * 5)

        elif ((total_cells_per_row_or_col * 6) + 1) <= vcell <= (total_cells_per_row_or_col * 7):
            arr_ref = '7'
            mval = (total_cells_per_row_or_col * 6)

        elif ((total_cells_per_row_or_col * 7) + 1) <= vcell <= (total_cells_per_row_or_col * 8):
            arr_ref = '8'
            mval = (total_cells_per_row_or_col * 7)

        elif ((total_cells_per_row_or_col * 8) + 1) <= vcell <= (total_cells_per_row_or_col * 9):
            arr_ref = '9'
            mval = (total_cells_per_row_or_col * 8)

        elif ((total_cells_per_row_or_col * 9) + 1) <= vcell <= (total_cells_per_row_or_col * 10):
            arr_ref = '10'
            mval = (total_cells_per_row_or_col * 9)

        globals()['cols' + arr_ref][vcell - mval] = globals()['cols' + arr_ref][vcell - mval].empty()
        if mystate.plyrbtns[vcell]['isPressed'] == True:
            if mystate.plyrbtns[vcell]['isTrueFalse'] == True:
                globals()['cols' + arr_ref][vcell - mval].markdown(pressed_emoji.replace('|fill_variable|', '✅️'), True)

            elif mystate.plyrbtns[vcell]['isTrueFalse'] == False:
                globals()['cols' + arr_ref][vcell - mval].markdown(pressed_emoji.replace('|fill_variable|', '❌'), True)
                errors += 1
        else:
            vemoji = mystate.plyrbtns[vcell]['eMoji']
            globals()['cols' + arr_ref][vcell - mval].button(vemoji, on_click=pressed_check, args=(vcell,),
                                                             key=f"B{vcell}")

    st.caption('')  # vertical filler
    st.markdown(horizontal_line, True)

    if len(mystate.expired_cells) == (total_cells_per_row_or_col ** 2) or errors >= max_errors:  # Verificar si el usuario ha perdido):
        leaderboard('write')
        if mystate.myscore > 0 and errors < max_errors:
            st.balloons()
        elif mystate.myscore <= 0 or errors >= max_errors:
            st.snow()
        tm.sleep(5)
        mystate.runpage = main
        st.rerun()


def main():
    # funcion principal que ejecuta el proyecto
    st.markdown('<style>[data-testid="stSidebar"] > div:first-child {width: 310px;}</style>',
                unsafe_allow_html=True, )  # reduce sidebar width
    st.markdown(purple_button_color, unsafe_allow_html=True)

    initial_page()
    with st.sidebar:
        mystate.GameDetails[0] = st.radio('Difficulty Level:', options=('Easy', 'Medium', 'Hard'), index=1,
                                          horizontal=True, )
        mystate.GameDetails[3] = st.text_input("Player Name, Country", placeholder='Shawn Pereira, India',
                                               help='Optional input only for Leaderboard')

        if st.button(f"🕹️ New Game", use_container_width=True):

            if mystate.GameDetails[0] == 'Easy':
                mystate.GameDetails[1] = 8  # secs interval
                mystate.GameDetails[2] = 6  # total_cells_per_row_or_col

            elif mystate.GameDetails[0] == 'Medium':
                mystate.GameDetails[1] = 6  # secs interval
                mystate.GameDetails[2] = 7  # total_cells_per_row_or_col

            elif mystate.GameDetails[0] == 'Hard':
                mystate.GameDetails[1] = 5  # secs interval
                mystate.GameDetails[2] = 8  # total_cells_per_row_or_col

            leaderboard('create')

            pre_new_game()
            mystate.runpage = new_game
            st.rerun()

        st.markdown(horizontal_line, True)

# Verifica si la función 'runpage' no está definida en mystate y la define como 'main'
if 'runpage' not in mystate: mystate.runpage = main
mystate.runpage()