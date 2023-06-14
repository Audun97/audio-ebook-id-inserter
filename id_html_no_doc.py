from bs4 import BeautifulSoup, NavigableString
import re

def add_ids_to_spans(html_file):
    outputfile = html_file.rsplit(".", 1)[0] + "_processed.xhtml"
    
    with open(html_file, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "lxml")

    p_elements = soup.find_all("p")

    id_counter = 1

    for p in p_elements:
        
        children = list(p.descendants)
        
        current_span = None
        
        for child in children:
            
            if isinstance(child, NavigableString):
                continue
            
            elif child.string is None:
                continue
            
            elif child.string is not None:
                if not re.search(r'[:;!,?.]', child.string) and re.search(r'\w', child.string):
                    if child.parent.parent.name == 'span' and child.parent.parent.get(f"f{str(id_counter).zfill(3)}") != 'true':
                        continue
                    if current_span is None:
                        current_span = soup.new_tag("span")
                        current_span["id"] = f"f{str(id_counter).zfill(3)}"
                        id_counter += 1
                    child.wrap(current_span)
                    print("no comma \n")
                    
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
                        
    with open(outputfile, "w", encoding="utf-8") as file:
        file.write(soup.decode(formatter=None))

add_ids_to_spans(r"part0000_split_009.html")
print("process has completed successfully")