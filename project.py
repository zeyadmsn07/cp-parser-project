from Parse import Parser
import re, requests, os, sys
from pathlib import Path

pathParent = Path(__file__).resolve().parent

def main():
    parser = Parser()
    args = parser.parse_args()

    ID = get_contest_ID(args.link)
    probs = get_problem_names(int(ID))
    pnames = [p["name"] for p in probs]
    
    name = re.sub(" ", "_", (args.directory).strip())
    open_directory(name)

    filenames = create_lang_files_names(pnames, args.language)
    open_prob_files(filenames, args.language, name)

    print(f"\n{name} folder created successfully in your main path. Happy solving!🤗\n")

def get_contest_ID(link):
    regex = r"^https?://(?:www.)?codeforces\.com(?:[A-Za-z_/.0-9-]+)?/contest(?:[A-Za-z_/.0-9-]+)?/(\d+)$"
    ID =  re.search(regex, link)
    try:
        return ID.group(1)
    except AttributeError:
        sys.exit("\nFLAG ERROR: Invalid contest link\n")

def get_problem_names(ID):
    data = requests.get(f"https://codeforces.com/api/contest.standings?contestId={ID}")
    json = data.json()
    if json["status"] == "OK":
        return json["result"]["problems"] 
    else:
        error = f"Unable to fetch data for contest {ID}: {json.get('comment')}"
        sys.exit(f"\nFLAG ERROR: {error}\n")

def create_lang_files_names(names, lang):
    newnames = map(lambda name: re.sub(r"[\s)(+=*^]", "_", name), names)
    lang = lang.lower().strip()

    if lang == "cpp":
        return [name + ".cpp" for name in newnames]
    elif lang == "py":
        return[name + ".py" for name in newnames]
    elif lang == "c":
        return[name + ".c" for name in newnames]
    elif lang == "java":
        return[name + ".java" for name in newnames]
    else:
        sys.exit(f"\nFLAG ERROR: {lang} is not a valid language.\n")
    
def open_prob_files(files, lang, direc):
    lang = lang.lower().strip()
    for file in files:
        try:
            with open(f"{pathParent.parent}/{direc}/{file}", "w") as code, open(f"{pathParent}/Templates/{lang}temp.txt", "r") as temp:
                lines = temp.read()
                nlines = re.sub("FileName", file.removesuffix(f".{lang}"), lines)
                code.write(nlines)
        except FileNotFoundError:
            sys.exit("\nFLAG ERROR: The file you're trying to access does not exist.\n")
            
def open_directory(direc):
    try:
        os.mkdir(f"{pathParent.parent}/{direc}")
    except FileExistsError:
        error = f"\nFLAG ERROR: {direc} ALREADY exists in this path (please use another folder name).\n"
        sys.exit(error)

if __name__ == "__main__":
    main()