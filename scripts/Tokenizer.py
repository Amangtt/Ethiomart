import pandas as pd
PUNCTUATIONS = '''!()-[]{}'"...?~፠።፣፤፥፦፧፨🗣👉🎁🌟📞📍🌼🧒>'''

def remove_punctuation(text):
    # Use a translation table to remove punctuation characters
    return text.translate(str.maketrans('', '', PUNCTUATIONS))

def tokenize(input_excel, output_txt):
    # Read the Excel file into a DataFrame
    df = pd.read_excel(input_excel)

    # Check if the "Message" column exists
    if 'Message' not in df.columns:
        raise ValueError("The 'Message' column is missing in the Excel file.")

    # Open the output text file for writing
    with open(output_txt, 'w', encoding='utf-8') as outfile:
        for message in df['Message'].dropna():  # Drop NaN values
            # Remove punctuation from the message
            cleaned_message = remove_punctuation(message)
            # Split the cleaned message by spaces and write each token on a new line
            tokens = cleaned_message.split()
            for token in tokens:
                outfile.write(token + '\n')

# Example usage
input_file = 'Untitled spreadsheet (1).xlsx'  
output_file = 'output_tokens.txt'    
tokenize(input_file, output_file)