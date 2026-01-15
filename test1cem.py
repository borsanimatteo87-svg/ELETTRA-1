import streamlit as st
from streamlit_option_menu import option_menu
from fpdf import FPDF
import base64
import os
from pypdf import PdfReader, PdfWriter

def solo_scarica_pdf(percorso_relativo, nome_materia):
    if os.path.exists(percorso_relativo):
        # Calcoliamo la dimensione solo per informazione dell'utente
        dimensione_mb = os.path.getsize(percorso_relativo) / (1024 * 1024)
        
        with open(percorso_relativo, "rb") as f:
            pdf_data = f.read()
        
        # Creiamo solo il pulsante di download
        st.download_button(
            label=f"📥 Scarica {nome_materia} ({dimensione_mb:.2f} MB)",
            data=pdf_data,
            file_name=os.path.basename(percorso_relativo),
            mime="application/pdf",
            key=percorso_relativo # La chiave deve essere unica per ogni file
        )
    else:
        st.error(f"⚠️ File non trovato: {percorso_relativo}")



#IMPOSTAZIONI PAGINA
st.set_page_config(page_title="Appunti",page_icon="🌆", layout="wide", initial_sidebar_state="expanded")
# FRONT CARATTERI
st.markdown(
    """
    <style>
    /* 1. Importazione Font */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

    /* 2. Applicazione Font Generale */
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, label {
        font-family: 'Montserrat', sans-serif !important;
    }

    /* 3. Personalizzazione Dimensioni e Colori */
    h1 {
        font-size: 45px !important;
        color: #FF4B4B !important;
    }
    h2 {
        font-size: 35px !important;
        color: #31333F !important;
    }
    h3 {
        font-size: 20px !important;
        font-weight: bold !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- FUNZIONE DI COMPRESSIONE ---
def comprimi_pdf_internamente(percorso_originale):
    """Crea una copia compressa del PDF per l'anteprima"""
    percorso_compresso = percorso_originale.replace(".pdf", "_compresso.pdf")
    
    # Se il file compresso esiste già, non rifacciamo il lavoro
    if os.path.exists(percorso_compresso):
        return percorso_compresso
    
    try:
        reader = PdfReader(percorso_originale)
        writer = PdfWriter()
        for page in reader.pages:
            page.compress_content_streams() # Comprime i dati interni
            writer.add_page(page)
        
        with open(percorso_compresso, "wb") as f:
            writer.write(f)
        return percorso_compresso
    except Exception:
        return percorso_originale # In caso di errore, usa l'originale

# AREA CENTRALE
with st.container(border=True):
                st.title(f"💥 Appunti Elettra ")
# --- FUNZIONE PER VISUALIZZARE E SCARICARE (AGGIORNATA) ---
                def mostra_pdf(percorso_relativo, nome_materia):
                            if os.path.exists(percorso_relativo):
                                # Proviamo a comprimerlo prima di caricarlo in memoria
                                percorso_da_usare = comprimi_pdf_internamente(percorso_relativo)
                                
                                dimensione_byte = os.path.getsize(percorso_da_usare)
                                dimensione_mb = dimensione_byte / (1024 * 1024)
                                
                                with open(percorso_da_usare, "rb") as f:
                                    pdf_data = f.read()
                                
                                # Pulsante di download
                                st.download_button(
                                    label=f"📥 Scarica {nome_materia} ({dimensione_mb:.1f} MB)",
                                    data=pdf_data,
                                    file_name=os.path.basename(percorso_relativo),
                                    mime="application/pdf",
                                    key=percorso_relativo # Chiave univoca
                                )

                                # Anteprima PDF
                                if dimensione_mb < 10:
                                    base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
                                    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
                                    st.markdown(pdf_display, unsafe_allow_html=True)
                                else:
                                    st.warning("⚠️ File molto grande. L'anteprima è disattivata per fluidità. Usa il tasto Scarica.")
                            else:
                                st.error(f"⚠️ File non trovato: {percorso_relativo}")                         
       
                with st.expander(f"🧮  ***MATEMATICA***"):
                        # MATERIA 2
                        with st.expander("📘  LE DERIVATE"):
                                with st.expander("🧾 ***TEORIA***"):
                                    mostra_pdf("APPUNTI/MATEMATICA/DERIVATE/DERIVATE_Teoria.pdf", "DERIVATE")
                                    mostra_pdf("APPUNTI/MATEMATICA/DERIVATE/Derivate - Teoremi.pdf", "DERIVATE")
                                with st.expander("🖋 ***ESERCIZI***"):
                                    solo_scarica_pdf("APPUNTI/MATEMATICA/DERIVATE/Esercizi derivate composte Svolti.pdf", "DERIVATE")
                                    solo_scarica_pdf("APPUNTI/MATEMATICA/DERIVATE/Esercizi derivate exp base var. Svolti.pdf", "DERIVATE")
                                with st.expander("📝 ***SINTESI & TABELLE***"):
                                    mostra_pdf("APPUNTI/MATEMATICA/DERIVATE/Derivate - TABELLA COMPOSTE.pdf", "DERIVATE")
                                    mostra_pdf("APPUNTI/MATEMATICA/DERIVATE/Derivate - TABELLA FONDAMENTALI.pdf", "DERIVATE")

                        # MATERIA 3
                        with st.expander("📘  STUDIO DI FUNZIONE"):
                                with st.expander("🧾 ***TEORIA***"):
                                    mostra_pdf("APPUNTI/MATEMATICA/STUDIO DI FUNZIONE/1_FUNZIONI.pdf", "STUDIO DI FUNZIONE")
                                    mostra_pdf("APPUNTI/MATEMATICA/STUDIO DI FUNZIONE/CLASSIFICARE UNA FUNZIONE.pdf", "STUDIO DI FUNZIONE")
                                with st.expander("🖋 ***ESERCIZI***"):
                                    mostra_pdf("APPUNTI/MATEMATICA/STUDIO DI FUNZIONE/ESERCIZI ESPONENZIALI.pdf", "ESPONENZIALI")
                                    mostra_pdf("APPUNTI/MATEMATICA/STUDIO DI FUNZIONE/ESERCIZI FRATTE.pdf", "FRATTE")
                                    mostra_pdf("APPUNTI/MATEMATICA/STUDIO DI FUNZIONE/ESERCIZI RADICALI 2.pdf", "RADICI 2")
                                    mostra_pdf("APPUNTI/MATEMATICA/STUDIO DI FUNZIONE/ESERCIZI STUDIO DI FUNZIONE.pdf", "ESERCIZI STUDIO DI FUNZIONE")

                                with st.expander("📝 ***SINTESI & TABELLE***"):
                                    mostra_pdf("APPUNTI/MATEMATICA/STUDIO DI FUNZIONE/Studio di funzione - mappa.pdf", "STUDIO DI FUNZIONE")


st.write(f"🕺  *Buono Studio... Il Prof*. 💫")                                          
             
