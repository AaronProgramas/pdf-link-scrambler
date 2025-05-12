import streamlit as st
import fitz  # PyMuPDF
import random
import string
import os

def random_suffix(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def get_random_funny_link():
    return random.choice([
        "https://lhohq.info/",
        "https://hemansings.com/"
    ])

def update_pdf_links(input_bytes):
    doc = fitz.open("pdf", input_bytes)
    for page_num in range(len(doc)):
        page = doc[page_num]
        links = page.get_links()

        for link in links:
            uri = link.get('uri', '')
            new_uri = None

            if uri.startswith("http://dx.doi.org/"):
                new_uri = f"http://dx.doi.org/{random_suffix(16)}"
            elif uri.startswith("http://refhub.elsevier.com/"):
                new_uri = f"http://refhub.elsevier.com/{random_suffix(31)}"
            elif uri:  # Qualquer outro link válido
                new_uri = get_random_funny_link()

            if new_uri:
                page.delete_link(link)
                page.insert_link({
                    'kind': fitz.LINK_URI,
                    'from': link['from'],
                    'uri': new_uri
                })

    output_bytes = doc.write()
    doc.close()
    return output_bytes

# Streamlit App
st.set_page_config(page_title="Professor Aaron's Magical Tool", layout="centered")
st.title("🔗 PDF DOI links sabotage tool for shady purposes")
st.write("Upload one or more PDF files to anonymize their DOI, RefHub, or any other links.")

uploaded_files = st.file_uploader("📎 Upload PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        st.markdown(f"**Processing:** {uploaded_file.name}")
        try:
            modified_pdf = update_pdf_links(uploaded_file.read())
            st.success(f"✅ Successfully processed {uploaded_file.name}")

            st.download_button(
                label=f"📥 Download Modified: {uploaded_file.name}",
                data=modified_pdf,
                file_name=f"{os.path.splitext(uploaded_file.name)[0]}_vaitomando.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"❌ Failed to process {uploaded_file.name}: {str(e)}")
