def count_vowels(sentence: str) -> int:
    """
    Counts the number of vowels in a given sentence (case-insensitive).
    """
    vowels = {'a', 'e', 'i', 'o', 'u'}
    return sum(1 for char in sentence.lower() if char in vowels)

def main():
    """
    Main function to execute the vowel counting program.
    """
    try:
        sentence = input("Enter a sentence: ")
        count = count_vowels(sentence)
        print(f"The number of vowels in the sentence is {count}.")
    except EOFError:
        print("\nInput stream closed.")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")

if __name__ == "__main__":
    main()