from contextlib import contextmanager

import streamlit as st
import streamlit.components.v1 as components

class Modal:

    def __init__(self, key: str, title: str, content: callable, padding: int = 20, max_width: int = None):
        self.title = title
        self.padding = padding
        self.key = key
        if f'{self.key}-opened' not in st.session_state:
            print("not in session state")
            st.session_state[f'{self.key}-opened'] = False

        if max_width:
            self.max_width = str(max_width) + "px"
        else:
            self.max_width = 'unset'

        self.content = content

    def callback_modal_open(self):
        st.session_state[f'{self.key}-opened'] = not st.session_state[f'{self.key}-opened']

    def is_open(self):
        return st.session_state.get(f'{self.key}-opened')

    @contextmanager
    def container(self):
        if self.is_open():
            st.markdown(
                f"""
                <style>
                div[data-modal-container='true'][key='{self.key}'] {{
                    position: fixed;
                    width: 100vw !important;
                    left: 0;
                    z-index: 999992;
                }}
                div[data-modal-container='true'][key='{self.key}'] > div:first-child {{
                    margin: auto;
                }}
                div[data-modal-container='true'][key='{self.key}'] h1 a {{
                    display: none
                }}
                div[data-modal-container='true'][key='{self.key}']::before {{
                        position: fixed;
                        content: ' ';
                        left: 0;
                        right: 0;
                        top: 0;
                        bottom: 0;
                        z-index: 1000;
                        background-color: rgba(0, 0, 0, 0.5);
                }}
                div[data-modal-container='true'][key='{self.key}'] > div:first-child {{
                    max-width: {self.max_width};
                }}
                div[data-modal-container='true'][key='{self.key}'] > div:first-child > div:first-child {{
                    width: unset !important;
                    background-color: #fff;
                    padding: {self.padding}px;
                    margin-top: {2 * self.padding}px;
                    margin-left: -{self.padding}px;
                    margin-right: -{self.padding}px;
                    margin-bottom: -{2 * self.padding}px;
                    z-index: 1001;
                    border-radius: 5px;
                }}
                div[data-modal-container='true'][key='{self.key}'] > div > div:nth-child(2)  {{
                    z-index: 1003;
                    position: absolute;
                }}
                div[data-modal-container='true'][key='{self.key}'] > div > div:nth-child(2) > div {{
                    text-align: right;
                    padding-right: {self.padding}px;
                    max-width: {self.max_width};
                }}
                div[data-modal-container='true'][key='{self.key}'] > div > div:nth-child(2) > div > button {{
                    right: 0;
                    margin-top: {2 * self.padding + 14}px;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )
            countainer_outer = st.container()
            container_inner = countainer_outer.container()
            if self.title:
                container_inner.markdown(
                    f"<h2>{self.title}</h2>", unsafe_allow_html=True)

            countainer_outer.button('X', key=f'{self.key}-close', on_click=self.callback_modal_open)

            components.html(
                f"""
                <script>
                // STREAMLIT-MODAL-IFRAME-{self.key} <- Don't remove this comment. It's used to find our iframe
                const iframes = parent.document.body.getElementsByTagName('iframe');
                let container
                for(const iframe of iframes)
                {{
                if (iframe.srcdoc.indexOf("STREAMLIT-MODAL-IFRAME-{self.key}") !== -1) {{
                    container = iframe.parentNode.previousSibling;
                    container.setAttribute('data-modal-container', 'true');
                    container.setAttribute('key', '{self.key}');
                }}
                }}
                </script>
                """,
                height=0, width=0
            )

            with container_inner:
                self.content()
    
