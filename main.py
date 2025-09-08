# main.py
import os
import textwrap
from processing.file_loader import load_documents
from processing.chunker import chunk_text
from processing.embedder import embed_chunks
from retrieval.vector_store import VectorStore
from models.model_loader import ask_model

from colorama import Fore, Style, init
init(autoreset=True)

import warnings
warnings.filterwarnings("ignore")


ASSISTANT_NAME = "Snaxi"


def main():

    print(Fore.YELLOW +
          f"\n\n😋 Hey!I'm your goofy explainer buddy! {ASSISTANT_NAME}\n\n" + Style.RESET_ALL)
    print(Fore.CYAN + "Ask me anything you want: a joke, explain technical terms, or dig into your docs.\n\n" + Style.RESET_ALL)

    # Load and process docs
    docs = load_documents("docs")
    if not docs:
        print(Fore.RED +
              f"{ASSISTANT_NAME}: Hmm, no docs found in /docs. Add some PDFs, DOCX, or TXT files!" + Style.RESET_ALL)
        return

    chunks = chunk_text(docs)
    embeddings = embed_chunks(chunks)

    store = VectorStore("data/chroma")
    store.clear()  # clear existing data
    file_count = len(os.listdir("docs"))  # count loaded file in docs folder
    print(Fore.GREEN +
          f"📂 Loaded {file_count} file(s) and split into {len(chunks)} chunks for Snaxi's brain." + Style.RESET_ALL)

    store.add_documents(embeddings)

    # Conversation history (list of {"role": ..., "content": ...})
    history = []

    # Chat loop
    last_answer = None  # remember last answer
    last_question = None  # remember last question
    while True:
        query = input(
            Fore.YELLOW + f"\nAsk {ASSISTANT_NAME} (or type 'exit'): \n")
        if query.lower() == "exit":
            print(Fore.GREEN +
                  f"{ASSISTANT_NAME}: Byeee 👋 Don’t forget to snack on knowledge every day!")
            break

        # save feature
        if query.lower().startswith("save "):
            if not last_question or not last_answer:
                print(
                    Fore.RED + f"\nOops, nothing for {ASSISTANT_NAME} to save yet! Ask me something first." + Style.RESET_ALL)
                continue

            title = query[5:].strip() or "Untitle"
            # make sure notes directory exists
            os.makedirs("notes", exist_ok=True)
            # save to notes into the folder
            with open("notes/save_notes.txt", "a", encoding="utf-8") as f:
                f.write(
                    f"\n** {title} ** \nQ: {last_question}\nA: {last_answer}\n")
            print(Fore.MAGENTA +
                  f"📌 Note saved in notes folder under '{title}' in notes/saved_notes.txt" + Style.RESET_ALL)
            continue

        # --- CHAT MODE ---
        if any(word in query.lower() for word in ["feel", "overwhelmed", "stress", "chat", "talk", "name", "lonely", "good at"]):
            playful_prompt = f"""
            You are Snaxi, a goofy onboarding buddy. 
            The user is asking for comfort or casual chat, not legal info.
            Respond in a short, funny, supportive way (max 5 sentences).
            Use humor (silly metaphors, snacks, superheroes, emojis) to make the user feel better.
            Do NOT cite documents or page numbers in this mode.
            Do NOT over talking

            User said\n\n: {query}
            """
            answer = ask_model(playful_prompt, [], history)

        # --- JOKE MODE (new) ---
        elif "joke" in query.lower():
            joke_prompt = f"""
            You are Snaxi, a goofy onboarding buddy.
            Tell ONE short, funny joke in a single sentence.
            Do not explain the joke or add extra text.
            """
            answer = ask_model(joke_prompt, [], history)

        # --- FUNNY/EXAMPLE MODE ---
        elif any(word in query.lower() for word in ["funny", "example", "story"]):
            if last_answer:
                funny_prompt = f"""
                Re-explain the following answer in a FUNNY way, like telling a silly story or superhero example.
                Keep it under 5 sentences. Do NOT add unrelated content.
                Preserve all legal terms and numbers exactly.

                Answer to re-explain:
                {last_answer}
                """
                answer = ask_model(funny_prompt, [], history)
            else:
                answer = f"{ASSISTANT_NAME}: Heh, I need something to make funny first! Ask me a question."


        # --- REPHRASE/SIMPLIFY MODE ---
        elif any(word in query.lower() for word in ["simplify", "rephrase", "concise", "shorter", "in 3 sentences"]):
            if last_answer:
                strict_prompt = f"""
                Rephrase the following answer in EXACTLY 3 sentences, no more, no less.
                Do not add new details. Preserve all numbers and key terms (like 'would' vs 'could').

                Answer to rephrase:
                {last_answer}
                """
                answer = ask_model(strict_prompt, [], history)
            else:
                answer = f"{ASSISTANT_NAME}: Oops, nothing to rephrase yet! Ask me something first."

        
        # --- NORMAL DOC MODE ---
        else:
            results = store.retrieve(query, top_k=5)
            history.append({"role": "user", "content": query})

            doc_prompt = f"""
            You are Snaxi, a goofy but helpful onboarding buddy.
            The user is asking a factual question based on documents.

            Rules for your answer:
            - Use short sentences OR at most 3 bullet points.
            - Always cite the source and page when possible, except when chatting casually.
            - At the end, give a fun "snack-sized takeaway" line with an emoji (🍪, 🎉, 📘, etc.).
            - Keep tone light and funny but accurate (avoid sounding like a government clerk, boring and sleepy).
            - Do not repeat or over-explain — be clear and concise.

            Question: {query}
            """

            answer = ask_model(doc_prompt, results, history)
            history.append({"role": "assistant", "content": answer})

        # --- FORMATTED OUTPUT ---
        wrapped_answer = textwrap.fill(
            answer, width=80, subsequent_indent="   ")
        print("\n" + "-"*80)
        print(Fore.CYAN + f"{ASSISTANT_NAME}:" + Style.RESET_ALL)
        print("   " + Fore.WHITE + wrapped_answer + Style.RESET_ALL)
        print("-"*80 + "\n")

        last_answer = answer  # remember the last answer
        last_question = query


if __name__ == "__main__":
    main()
