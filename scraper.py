import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import json
import ast

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content

    urls = ('ics.uci.edu', 'cs.uci.edu', 'informatics.uci.edu', 'stat.uci.edu')
    ret = set()

    try:
        bs = BeautifulSoup(resp.raw_response.content, 'html.parser')
    except:
        return list()
    
    #Load map with word frequencies
    with open('freq.txt', 'r+') as f:
        data = f.read()

    map = ast.literal_eval(data)

    words = bs.get_text().split()

    #Check if this page contains the most words
    with open('long.txt', 'r') as f:
        data = f.read().split()
    if len(words) > int(data[1]):
        with open('long.txt', 'w') as f:
            string = resp.url + " " + str(len(words))
            f.write(string)

    #Traverse through all the words, and update the frequency map
    for word in words:
        if word.upper() in map:
            #Increment frequncy is token is found in list again
            # Constant time 
            map[word.upper()] += 1
        else:
            #Initialize frequency to 1 if a undiscovered token is found
            #Constant time
             map[word.upper()] = 1
    
    #Sort map
    map = {k: v for k, v in sorted(map.items(), key=lambda item: item[1], reverse = True)}

    #Write to file
    with open('freq.txt', 'w') as f:
        f.write(str(map))

    #Find all the links
    for a in bs.findAll('a', href = True):
        link = a['href'].split('#')
        for b in link:
            for u in urls:
                if(u in b):
                    #Add https to link
                    if(b[0] == '/'):
                        b = 'https:' + b
                    ret.add(b)
                    break
    return ret

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
