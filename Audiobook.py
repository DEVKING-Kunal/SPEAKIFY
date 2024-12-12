import PyPDF2 as pdf
import pyttsx3 as x
import os

def audiobook(file, speed):
    # Check if the PDF file exists
    if not os.path.exists(file):
        print(f"Error: The file '{file}' does not exist.")
        return

    # Open the PDF
    try:
        book = open(file, "rb")
        reader = pdf.PdfReader(book)
    except Exception as e:
        print(f"Error reading the PDF file: {e}")
        return

    # Ask for the page number to read
    number = int(input("Please enter the page number you want to read (0-indexed): "))

    # Check if page number exists
    if len(reader.pages) <= number:
        print("The PDF does not have that many pages.")
        return  # Exit the function if page number is out of range

    # Extract text from the specified page
    text = reader.pages[number].extract_text()
    if not text.strip():
        print("The selected page is empty.")
        return

    # Remove line breaks and unnecessary spaces for smoother reading
    text = " ".join(text.split())

    # Initialize pyttsx3
    speak = x.init()
    voices = speak.getProperty("voices")

    # Display available voices with index numbers
    print("Available voices:")
    for idx, voice in enumerate(voices):
        try:
            language = voice.languages[0].decode("utf-8") if voice.languages else "Unknown"
        except Exception:
            language = "Unknown"
        print(f"{idx}: {voice.name} ({language})")

    # Let the user select a voice by number
    voice_index = int(input("Please enter the number of the voice you want to use: "))
    if 0 <= voice_index < len(voices):
        speak.setProperty("voice", voices[voice_index].id)
        print(f"Using voice: {voices[voice_index].name}")
    else:
        print("Invalid selection. Using the default voice.")

    # Set the speech rate
    speak.setProperty("rate", speed)  # Speed in words per minute

    # Speak the entire text of the page at once for smoother reading
    print(f"Reading page {number}...")
    speak.say(text)
    speak.runAndWait()
    book.close()

# Get user input for speed

speed = int(input("Enter the speed of audiobook (in words per minute): "))

# Call the function
audiobook(r"C:\Users\HP\Downloads\Notes 10 to 12.docx.pdf", speed)  # Adjust file path as needed

