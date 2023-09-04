import os
from bs4 import BeautifulSoup, NavigableString
import re

def add_ids_to_spans(html_file):
    # Open the input file in read mode with UTF-8 encoding
    with open(html_file, "r", encoding="utf-8") as file:
        # Use BeautifulSoup to parse the file
        soup = BeautifulSoup(file, "lxml")

    # Initialize a counter for the "id" values
    id_counter = 1
    
    # Find all the h elements in the file
    h_elements = soup.find_all("h1") + soup.find_all("h2") + soup.find_all("h3") + soup.find_all("h4") + soup.find_all("h5") + soup.find_all("h6")
    
    # If h_elements is non-empty
    if h_elements:
    # Loop through each h element and add a span with "id" attribute
        for h in h_elements:
            # If there are not tags inside tag
            if isinstance(h.string, NavigableString):
                # if sentence does not contain comma, punctuation etc 
                if not re.search(r'[:;!,?.]', h.string) and re.search(r'\w', h.string):
                    current_span = soup.new_tag("span")
                    current_span["id"] = f"f{str(id_counter).zfill(3)}"
                    id_counter += 1
                    h.string.wrap(current_span)
                    print("no comma \n")
                # if sentence contains comma, punctuation etc   
                elif re.search(r'\w', h.string):
                    current_span = None
                    sentences = re.split(r'(?<=[.?!;:,])\s+(?=\w)', h.string)
                    h.clear()
                    for sentence in sentences:
                        span = soup.new_tag("span")
                        span["id"] = f"f{str(id_counter).zfill(3)}"
                        span.string = sentence + " "
                        h.append(span)
                        id_counter += 1
                        print("with comma \n")
                else:
                    print("this was caught" + str(h.string))
                continue
            
            # Get all the descendants of the current "h" element. Not feeding it directly into the next loop to prevent an endless loop
            children = list(h.descendants)
            
            # Initialize a span for the case that multiple child.strings will share a span
            current_span = None
            
            # Loop through each child of the "h" element
            for child in children:
                    # Skip if the child is a NavigableString
                    if isinstance(child, NavigableString):
                        continue
                    
                    # Skip if the child has no string value. I.e. the child has multiple children of its own
                    elif child.string is None:
                        continue
                    
                    elif child.string is not None:
                        # if sentence does not contain comma, punctuation etc 
                        if not re.search(r'[:;!,?.]', child.string) and re.search(r'\w', child.string):
                            # If parent tag is the tag added by script then do not wrap it again
                            if child.parent.parent.name == 'span' and child.parent.parent.get(f"f{str(id_counter).zfill(3)}") != 'true':
                                continue
                            #If the current span is None, create a new span
                            if current_span is None:
                                current_span = soup.new_tag("span")
                                current_span["id"] = f"f{str(id_counter).zfill(3)}"
                                id_counter += 1
                            child.wrap(current_span)
                            print("no comma \n")
                        # if sentence contains comma, punctuation etc   
                        elif re.search(r'\w', child.string):
                            current_span = None
                            sentences = re.split(r'(?<=[.?!;:,])\s+(?=\w)', child.string)
                            child.clear()
                            for sentence in sentences:
                                span = soup.new_tag("span")
                                span["id"] = f"f{str(id_counter).zfill(3)}"
                                span.string = sentence + " "
                                child.append(span)
                                id_counter += 1
                                print("with comma \n")
                        else:
                            print("this was caught" + str(child.string))
                            
    # Get all the p elements in the file
    p_elements = soup.find_all("p")

    # Loop through each p element
    for p in p_elements:
        # If there are no tags inside tag
        if isinstance(p.string, NavigableString):
            # if sentence does not contain comma, punctuation etc 
            if not re.search(r'[:;!,?.]', p.string) and re.search(r'\w', p.string):
                current_span = soup.new_tag("span")
                current_span["id"] = f"f{str(id_counter).zfill(3)}"
                id_counter += 1
                p.wrap(current_span)
                print("no comma \n")
            # if sentence contains comma, punctuation etc   
            elif re.search(r'\w', p.string):
                current_span = None
                sentences = re.split(r'(?<=[.?!;:,])\s+(?=\w)', p.string)
                p.clear()
                for sentence in sentences:
                    span = soup.new_tag("span")
                    span["id"] = f"f{str(id_counter).zfill(3)}"
                    span.string = sentence + " "
                    p.append(span)
                    id_counter += 1
                    print("with comma \n")
            else:
                print("this was caught" + str(p.string))
            continue
        
        # Get all the descendants of the current "p" element. Not feeding it directly into the next loop to prevent an endless loop
        children = list(p.descendants)
        
        # Initialize a span for the case that multiple child.strings will share a span
        current_span = None
        
        # Loop through each child of the "p" element
        for child in children:
            
            # Skip if the child is a NavigableString
            if isinstance(child, NavigableString):
                continue
            
            # Skip if the child has no string value. I.e. the child has multiple children of its own
            elif child.string is None:
                continue
            
            elif child.string is not None:
                # if sentence does not contain comma, punctuation etc 
                if not re.search(r'[:;!,?.]', child.string) and re.search(r'\w', child.string):
                    # If parent tag is the tag added by script then do not wrap it again
                    if child.parent.parent.name == 'span' and child.parent.parent.get(f"f{str(id_counter).zfill(3)}") != 'true':
                        continue
                    #If the current span is None, create a new span
                    if current_span is None:
                        current_span = soup.new_tag("span")
                        current_span["id"] = f"f{str(id_counter).zfill(3)}"
                        id_counter += 1
                    child.wrap(current_span)
                    print("no comma \n")
                # if sentence contains comma, punctuation etc   
                elif re.search(r'\w', child.string):
                    current_span = None
                    sentences = re.split(r'(?<=[.?!;:,])\s+(?=\w)', child.string)
                    child.clear()
                    for sentence in sentences:
                        span = soup.new_tag("span")
                        span["id"] = f"f{str(id_counter).zfill(3)}"
                        span.string = sentence + " "
                        child.append(span)
                        id_counter += 1
                        print("with comma \n")
                else:
                    print("this was caught" + str(child.string))
                        
    with open(html_file, "w", encoding="utf-8") as file:
        # Write the processed soup object to the output file with no extra formatting
        file.write(soup.decode(formatter="minimal"))

# Function to add a link to the css file to the head of the html file
def add_link_to_css(html_file):
    # Open the html file
# Open the input file in read mode with UTF-8 encoding
    with open(html_file, "r", encoding="utf-8") as file:
        # Use BeautifulSoup to parse the file
        soup = BeautifulSoup(file, "lxml")
        
        # Create a link tag
        link_tag = soup.new_tag("link")
        
        # Add the attributes to the link tag
        link_tag["rel"] = "stylesheet"
        link_tag["type"] = "text/css"
        link_tag["href"] = "../styles/style.css"
        
        # Add the link tag to the head of the html file
        soup.head.append(link_tag)
        
    with open(html_file, "w", encoding="utf-8") as file:
        # Write the processed soup object to the output file with no extra formatting
        file.write(soup.decode(formatter="minimal"))
        
directory = "test_book\\EPUB\\sync_text"

file_count = 0

for filename in os.listdir(directory):
    if filename.endswith('.xhtml') or filename.endswith('.html'):
        file_path = os.path.join(directory, filename)
        add_ids_to_spans(file_path)
        add_link_to_css(file_path)
        file_count += 1
        print("File number " + str(file_count) + " complete: "  + filename + "\n")