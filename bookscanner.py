# Erstellt mit Hilfe des KI-Assistenten Github Copilot und Claude Sonnet 3.5 * 0.9x
import streamlit as st
from get_book_data_for_isbn import get_isbn_service

# Set the page title
st.title("Book ISBN Scanner")

# Initialize session state for storing ISBNs and book data if they don't exist
if 'isbn_list' not in st.session_state:
    st.session_state.isbn_list = []
if 'book_data' not in st.session_state:
    st.session_state.book_data = {}

# Initialize the ISBN service
isbn_service = get_isbn_service()

def submit_isbn():
    if st.session_state.isbn_input:
        isbn = st.session_state.isbn_input
        # Get book data from the service
        result = isbn_service.get_book_data(isbn)
        
        if result['status'] == 'success':
            st.session_state.isbn_list.append(isbn)
            st.session_state.book_data[isbn] = result['data']
        else:
            st.error(f"Error: {result['message']}")
        
        # Clear input field
        st.session_state.isbn_input = ""

# Create an input field for ISBN with submit callback
st.text_input("Enter ISBN:", key="isbn_input", on_change=submit_isbn)

# Display the table of ISBNs with their data
st.subheader("Scanned Books:")
if st.session_state.isbn_list:
    # Create a list of dictionaries for the table
    table_data = []
    for i, isbn in enumerate(st.session_state.isbn_list, 1):
        book_data = st.session_state.book_data.get(isbn, {})
        table_data.append({
            "ISBN": isbn,
            "Title": book_data.get('title', ''),
            "Authors": ', '.join(book_data.get('authors', [])),
            "Publisher": book_data.get('publisher', '')
        })
    st.table(table_data)
else:
    st.write("No ISBNs scanned yet.")
