import ast

stopwords = "a about above after again against all am an and any are aren't as at " + \
"be because been before being below between both but by can't cannot could couldn't " + \
"did didn't do does doesn't doing don't down during each few for from further " + \
"had hadn't has hasn't have haven't having he he'd he'll he's her here here's hers " + \
"herself him himself his how how's i i'd i'll i'm i've if in into is isn't it it's " + \
"its itself let's me more most mustn't my myself no nor not of off on once only or " + \
"other ought our ours ourselves out over own same shan't she she'd she'll she's should " + \
"shouldn't so some such than that that's the their theirs them themselves then there " + \
"there's these they they'd they'll they're they've this those through to too under " + \
"until up very was wasn't we we'd we'll we're we've were weren't what what's when " + \
"when's where where's which while who who's whom why why's with won't would wouldn't " + \
"you you'd you'll you're you've your yours yourself yourselves".split()

def maxWordFrequencies():
    try:
        # Read word frequencies file
        with open("freq.txt", "r") as f:
            data = f.read()
            freq = ast.literal_eval(data)
        
        count = 0 # A counter for number of words outputted

        # Output the 50 most common words not including stop words into a file
        with open("commonwords.txt", "w") as out:
            for k in sorted(freq, key=lambda x : -freq[x]):
                if k not in stopwords:
                    count += 1
                    out.write(k + "\n")
                if count >= 50:
                    break

    except OSError:
        print("Failed to open a file")