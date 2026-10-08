import streamlit as st

from legalease.analysis import analyze_document, build_chunks
from legalease.config import load_config
from legalease.document_loader import extract_pdf_pages, extract_txt, pages_to_text
from legalease.models import PageText
from legalease.preprocessing import preprocess_document


st.set_page_config(page_title="LegalEase", layout="wide")


def render_list(title: str, values: list[str]) -> None:
    st.subheader(title)
    if not values:
        st.caption("Not specified in the document.")
        return
    for value in values:
        st.markdown(f"- {value}")


def read_input() -> tuple[str, list[PageText]]:
    uploaded = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])
    pasted_text = st.text_area("Or paste document text", height=220)

    if uploaded is None:
        return pasted_text, []

    if uploaded.name.lower().endswith(".pdf"):
        pages = extract_pdf_pages(uploaded)
        return pages_to_text(pages), pages

    return extract_txt(uploaded), []


def main() -> None:
    config = load_config()

    st.title("LegalEase")
    st.caption("AI Legal & Policy Simplifier")
    st.warning("LegalEase provides informational explanations only. It is not legal advice.")

    with st.sidebar:
        st.header("Context")
        user_type = st.selectbox(
            "I am a",
            ["Student", "Employee", "Customer", "Tenant", "Consumer", "Business owner", "General user", "Other"],
        )
        document_type = st.selectbox(
            "Document type",
            [
                "Auto Detect",
                "Privacy Policy",
                "Employment Contract",
                "Rental Agreement",
                "Terms & Conditions",
                "College/University Policy",
                "Government Policy",
                "Other",
            ],
        )
        specific_concern = st.text_area("Specific concern", placeholder="Example: termination, fees, data sharing")

    text, pages = read_input()
    analyze_clicked = st.button("Simplify Document", type="primary", use_container_width=True)

    if not analyze_clicked:
        return

    if not text.strip():
        st.error("Please upload a document or paste text first.")
        return

    with st.spinner("Processing document..."):
        processed = preprocess_document(text, pages=pages)
        chunks = build_chunks(processed, config)
        try:
            report = analyze_document(processed, user_type, document_type, specific_concern, config)
        except RuntimeError as exc:
            st.error(str(exc))
            st.info(
                "For your demo, either add API credits at OpenAI billing or temporarily remove "
                "LLM_API_KEY from your .env file to use LegalEase demo mode."
            )
            return

    stats = processed.stats
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Words", stats.word_count)
    col2.metric("Sentences", stats.sentence_count)
    col3.metric("Paragraphs", stats.paragraph_count)
    col4.metric("Chunks", len(chunks))

    st.divider()

    st.header("Simple Summary")
    st.write(report["short_summary"])

    st.header("What This Means For Me")
    st.write(report["what_this_means_for_me"])

    left, right = st.columns(2)
    with left:
        render_list("Important Obligations", report["important_obligations"])
        render_list("Deadlines", report["deadlines"])
        render_list("Potential Risks", report["potential_risks"])
    with right:
        render_list("User Rights", report["user_rights"])
        render_list("Fees and Penalties", report["fees_and_penalties"])
        render_list("Questions to Consider", report["questions_to_consider"])

    render_list("Important Clauses", report["important_clauses"])
    render_list("Source References", report["source_references"])

    st.info(report["disclaimer"])

    with st.expander("NLP preprocessing details"):
        st.write(
            {
                "character_count": stats.character_count,
                "average_sentence_length": stats.average_sentence_length,
                "page_count": len(pages),
                "chunk_count": len(chunks),
            }
        )
        st.text_area("Cleaned text preview", processed.cleaned_text[:3000], height=180)


if __name__ == "__main__":
    main()
