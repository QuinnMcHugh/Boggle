def compute_score(solvedWords):
	sum = 0
	for word in solvedWords:
		sum += single_word_score(word)
	return sum

def single_word_score(word):
	if len(word) < 3:
		return 0
	elif len(word) <= 4:
		return 1
	elif len(word) == 5:
		return 2
	elif len(word) == 6:
		return 3
	elif len(word) == 7:
		return 5
	else:
		return 11

# Only retain the userWords which also exist in validWords.
# Prevents malicious players from sending payloads of words 
# which didn't exist in the board. 
def filter_valid_words(userWords, validWords):
	return list(set(userWords) & set(validWords))

