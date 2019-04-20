
from enum import Enum


ChunkType = Enum("ChunkType", "book chapter verse sentence paragraph pericope")
TokenType = Enum("TokenType", "text form lemma")

chunk_data_filename = {
    ChunkType.book: "books.txt",
    ChunkType.chapter: "chapters.txt",
    ChunkType.verse: "verses.txt",
    ChunkType.sentence: "sentences.txt",
    ChunkType.paragraph: "paragraphs.txt",
    ChunkType.pericope: "pericopes.txt",
}


chunk_data = {}  # (chunk_type, chunk_id) -> (token_start, token_end)

def load_chunk_data():
    for chunk_type, filename in chunk_data_filename.items():
        with open(filename) as f:
            for line in f:
                chunk_id, token_start, token_end = line.strip().split()
                chunk_data[(chunk_type, chunk_id)] = (
                    int(token_start), int(token_end)
                )


token_data = {}  # token_type -> [tokens]

def load_tokens():
    for token_type in TokenType:
        token_data[token_type] = []

    with open("tokens.txt") as f:
        for line in f:
            token_id, text, form, pos, tag1, tag2, lemma = line.strip().split()

            # assume token_ids are sequential
            # token data is stored separately like this because all the
            # initial applications involve just wanting one particular type of
            # token at a time
            token_data[TokenType.text].append(text)
            token_data[TokenType.form].append(form)
            token_data[TokenType.lemma].append(lemma)


load_chunk_data()
load_tokens()


def get_tokens(token_type, chunk_type, chunk_id):
    """
    return a list of tokens of the given `token_type` from the chunk of type
    `chunk_type` with identifier `chunk_id`.

    e.g. `get_tokens(TokenType.lemma, ChunkType.verse, "640316")` means
    "get the lemma tokens from verse 640316"
    """

    start, end = chunk_data[(chunk_type, chunk_id)]

    # assume token_ids are sequential starting with 1
    return token_data[token_type][start - 1:end]


# for quick testing
if __name__ == "__main__":
    for token in get_tokens(TokenType.text, ChunkType.verse, "640316"):
        print(token)
