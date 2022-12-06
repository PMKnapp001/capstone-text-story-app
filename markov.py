"""Generate Markov text."""

from random import choice


def open_and_read_file(file):
    """Returns string from contents of file in file_path."""

    content = ""

    file_text = open(file)
    content = content + file_text.read()
    file_text.close()

    return content


def make_chains(text_string):
    """Return markov chain dicitionary from text.

    The keys in the dictionary are tuples with words_list[i] and
    words_list[i + 1] and the values are a list of words that can
    follow each specific key.
    """

    words_list = text_string.split()
    chains = {}

    for i in range(len(words_list) - 2):
        chain = (words_list[i], words_list[i + 1])
        link = words_list[i + 2]

        if chain not in chains:
            chains[chain] = []

        chains[chain].append(link)

    return chains


def make_text(chains):
    """Returns text from markov chain dictionary."""

    chain_keys = list(chains.keys())
    chain_key = choice(chain_keys)

    text = [chain_key[0], chain_key[1]]
    while chain_key in chains:
        word = choice(chains[chain_key])
        text.append(word)
        chain_key = (chain_key[1], word)

    return ' '.join(text)


def make_new_story(file):
    """Returns new story as a string from file using markov chain funcitons."""
    
    new_story_file = open_and_read_file(file)
    new_story_markov = make_chains(new_story_file)
    new_story = make_text(new_story_markov)

    return new_story