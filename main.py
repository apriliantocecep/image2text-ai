from vision import image2text, save_uploaded_file
import streamlit as st

if __name__ == "__main__":
    st.write("""
        # Image to Text 🛠️
        Extract information from image using AI ✨
    """)

    uploaded_file = st.file_uploader("Choose an image...", ['png', 'jpeg', 'gif', 'webp'])
    if uploaded_file is not None:
        with st.spinner("Processing 🚧..."):
            # Save the uploaded file to a temporary location
            temp_location = save_uploaded_file(uploaded_file)

            info = image2text(temp_location)

            st.subheader("Result 💾")
            st.write(info)

            st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
