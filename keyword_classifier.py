import streamlit as st
import pandas as pd

st.title("Sodium Battery Keyword Classifier")

categories = {
    "Basics & Technology": ["what is", "how does", "technology", "composition", "made of", "principle", "working", "definition"],
    "Performance & Safety": ["energy density", "cycle life", "safety", "explosion", "thermal runaway", "performance", "temperature", "life expectancy"],
    "Manufacturers & Brands": ["company", "companies", "manufacturer", "brand", "top", "yadea", "tiamat", "catl", "byd", "zebra", "yichen", "yiwei", "yuji", "zodiac", "zoolnasm"],
    "Applications": ["use", "application", "ev", "electric vehicle", "solar", "storage", "leisure battery"],
    "Market & Investment": ["stock", "investment", "market", "prices", "shares"],
    "Comparisons & Alternatives": ["compare", "difference", "vs", "versus", "better than", "downside"],
    "FAQs & Troubleshooting": ["faq", "problem", "issue", "troubleshoot", "repair", "maintenance", "how to", "tips", "guide"]
}

def categorize_keyword(keyword):
    keyword_lower = keyword.lower()
    matched_categories = []
    for cat, triggers in categories.items():
        if any(trig in keyword_lower for trig in triggers):
            matched_categories.append(cat)
    if not matched_categories:
        return "Uncategorized"
    elif len(matched_categories) == 1:
        return matched_categories[0]
    else:
        return "; ".join(matched_categories)

uploaded_file = st.file_uploader("Upload Excel file (.xlsx) with keywords", type=['xlsx'])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.write("Uploaded Data Preview:")
        st.dataframe(df.head())

        first_col = df.columns[0]
        keywords = df[first_col].dropna().astype(str).tolist()

        st.write(f"Classifying {len(keywords)} keywords...")

        categories_result = [categorize_keyword(kw) for kw in keywords]

        df_result = pd.DataFrame({
            "Keyword": keywords,
            "Category": categories_result
        })

        st.write("Classification Result:")
        st.dataframe(df_result)

        def to_excel(df):
            import io
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Classification')
            processed_data = output.getvalue()
            return processed_data

        excel_data = to_excel(df_result)

        st.download_button(
            label="Download Classified Keywords as Excel",
            data=excel_data,
            file_name='classified_keywords.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    except Exception as e:
        st.error(f"Error reading the Excel file: {e}")
else:
    st.info("Please upload an Excel file containing your keywords.")

