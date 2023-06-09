import re
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from nltk import word_tokenize

word_frequencies = {'hello':0}
subdomain_count = {'hello':0}
unique_urls = set()

def scraper(url, resp):
    links = extract_next_links(url, resp)
    returnList = [link for link in links if is_valid(link)]

    # check if current_url is a "ics.uci.edu" subdomain
    if 'ics.uci.edu' in str(url):
        # Update the number of unique pages for each subdomain
        parsed_url = urlparse(url)
        if parsed_url.hostname in subdomain_count:
            # Increment page count if subdomain is found in dictionary again
            subdomain_count[parsed_url.hostname] += len(returnList)
        else:
            # Initialize frequency if a undiscovered subdomain is found
            subdomain_count[parsed_url.hostname] = len(returnList)

    return returnList

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

    if resp.status != 200:
        return list()

    #Set to store links
    ret = set()

    #Create BeautifulSoup object so site can be scraped
    try:
        bs = BeautifulSoup(resp.raw_response.content, 'html.parser')
    except:
        return list()

    #Get all the words from the site
    words = word_tokenize(bs.get_text())  # Should be a list of words

    #Check if this page contains the most words
    with open('long.txt', 'r') as f:
        data = f.read().split()
    
    #Update text file if it contains the most words
    if len(words) > int(data[1]):
        with open('long.txt', 'w') as f:
            string = resp.url + " " + str(len(words))
            f.write(string)

    #Traverse through all the words to update the frequency map
    for word in words:
        if word.upper() in word_frequencies:
            #Increment frequncy is token is found in list again
            # Constant time 
            word_frequencies[word.upper()] += 1
        else:
            #Initialize frequency to 1 if a undiscovered token is found
            #Constant time
            word_frequencies[word.upper()] = 1
    
    #Find all the links
    for a in bs.findAll('a', href = True):
        curr_url = a['href'].split('#')[0]
        if not bool(urlparse(curr_url).netloc):
            curr_url = urljoin(url, curr_url, allow_fragments=False)
        if curr_url != url:
            ret.add(curr_url) #NEED TO RETURN ABSOLUTE LINKS
        #AND REMOVE ANYTHING AFTER '#' 
        # (i.e. http://www.ics.uci.edu#aaa should just be http://www.ics.uci.edu)

    unique_urls.append(ret)

    return ret

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)

        # If scheme is not "http" or "https", do not crawl
        if parsed.scheme not in set(["http", "https"]):
            return False
        
        BLACKLIST = ["https://www.ics.uci.edu/~eppstein/pix/", "calendar", "event", "events" "commit/", "blob/", "raw/", "blame/", "tree/", "/graphs/"]
        
        for domain in BLACKLIST:
            if domain in url:
                return False
            
        # Regex expression from https://support.archive-it.org/hc/en-us/articles/208332963-Modify-your-crawl-scope-with-a-Regular-Expression
        # To avoid common traps
        if(re.match(
            r"^.*?(/.+?/).*?\1.*$|^.*?/(.+?/)\2.*$"
            + r"^.*(/misc|/sites|/all|/themes|/modules|/profiles|/css|/field|/node|/theme){3}.*$"
            + r"^.*calendar.*$", parsed.netloc.lower())):
            return False
        
        if re.match(r".*(/calendar/|/blog/|mailto:).*", parsed.path.lower()):
            return False
        
        # If domain is not the following, do not crawl:
        #   *ics.uci.edu/*
        #   *cs.uci.edu/*
        #   *informatics.uci.edu/*
        #   *stat.uci.edu/*
        if not re.match(r".*(i?cs|informatics|stat)\.uci\.edu", parsed.hostname):
            return False
        
        # If url is a non-text file, do not crawl; otherwise crawl the url
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
