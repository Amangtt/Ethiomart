import pandas as pd

def process_text_file(input_txt, output_txt):
    """Process the input text file and output each token with 'O' label in a new line."""
    # Open the input text file for reading
    with open(input_txt, 'r', encoding='utf-8') as infile:
        # Open the output text file for writing
        with open(output_txt, 'w', encoding='utf-8') as outfile:
            for line in infile:
                # Split the line into tokens (assuming each line is already a token)
                tokens = line.strip().split()  # Remove any extra whitespace and split
                for token in tokens:
                    if token =='አድራሻ':
                        outfile.write(f"{token} B-LOC\n")
                    elif token == 'ጉርድ' or token == 'ሾላ' or token == 'ፒያሳ' or token == 'ጀሞ' or token == 'ገርጂ':
                        outfile.write(f"{token} I-LOC\n")
                    #PRODUCT   
                    elif token == 'የሪሞት' or  token =='ተገጣጣሚ' or token == '4D' or token == 'Rc' or token == 'Hero':
                        outfile.write(f"{token} B-PRODUCT\n")  

                    elif token == 'ማቅለሚያ' or token == 'መኪኖች' or token == 'ኮንትሮል' or token == 'HUMAN' or token == 'Human' or token == 'ANATOMY' or token == 'Anatomy' or token == 'Head' or token == 'Heart' or token == 'Ear' or token == 'ታብሌት' or token == 'ሩቢክስ' or token == 'ኪዩብ' or token == 'Bee' or token == 'Doll' or token == 'car' or token == 'excavator'or token == 'መርከብ' or token == 'animal-Puppy' or token == 'animal-Rooster' or token == 'ነብሩን' or token == 'Spiderman':
                        outfile.write(f"{token} I-PRODUCT\n")  
                    #PRICE
                    elif token == 'ዋጋ':
                        outfile.write(f"{token} B-PRICE\n")

                    elif token == '1400' or token =='12000' or token =='4000' or token == '3000' or token == '3500' or token == '1800' or token == '20000' or token == '8500' or token == '2300' or token == '300' or token == '1200' or token =='1500':
                        outfile.write(f"{token} I-PRICE\n")
                    else:
                        outfile.write(f"{token} O\n")  # Write token with 'O' label
                 

# Example usage
input_file = 'output_tokens.txt'  # Replace with your input file path
output_file = 'labeled_entities.txt'  # Replace with your desired output file path
process_text_file(input_file, output_file)