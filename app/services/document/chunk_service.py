from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_chunks(text):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200
    )

    return splitter.split_text(text)