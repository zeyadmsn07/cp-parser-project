# CP Parser

#### Video Demo: <URL HERE>

#### Description:

CP Parser is a command line tool that automates the file setup I do before every Codeforces contest. Instead of manually creating a folder, copying my template into a new file for every problem, and renaming the solve function each time, I run one command with the contest link and it does all of that for me. What used to take a few minutes of copy pasting before a round now takes a few seconds, which matters more than it sounds like when the contest clock is already running.

## What It Does

Given a Codeforces contest URL, a target language, and an optional folder name, CP Parser:

1. Extracts the contest ID from the URL
2. Fetches the list of problems in that contest through the Codeforces API
3. Creates a new directory for the contest
4. Generates one source file per problem, each pre-loaded with my personal template and a solve function already named after that problem

## Usage

```
python project.py -l https://codeforces.com/contest/2246 -L cpp -d Round1
```

This creates a `Round1` folder one level up from the project directory, with a `.cpp` file for every problem in that contest, each one ready to code in immediately.

## Project Structure

### `Parse.py`
Defines the `Parser` class, a subclass of `ArgumentParser`, which registers the three flags the tool accepts: `-L` for language, `-l` for the contest link, and `-d` for the directory name. I kept argument parsing in its own file separate from `project.py` so the CLI definition and the actual logic do not end up tangled together, which also made it easier to import and test the logic functions in isolation without pulling in argument parsing every time.

### `project.py`
This is where the core logic lives.

- **`get_contest_ID(link)`** pulls the numeric contest ID out of the URL using a regex rather than simple string splitting. I chose regex specifically because Codeforces URLs are not all shaped the same way. Group contests and private contests both attach extra path segments before the contest ID, so a plain `split("/")` approach would break on those cases. The regex handles the standard format along with those variants in one pass, and if the link does not match at all, the function exits with a clear error instead of throwing a confusing traceback.
- **`get_problem_names(ID)`** calls the Codeforces API and returns the problem list for that contest. It checks the `status` field in the response and exits with a descriptive message if the API does not return `OK`, rather than letting a bad or malformed request fail silently somewhere downstream.
- **`create_lang_files_names(names, lang)`** converts problem names into valid filenames for the chosen language. I normalized the language argument with `.lower().strip()` so the tool is not picky about how the user types it in, since typing `CPP` versus `cpp` should not be the difference between it working and exiting with an error.
- **`open_prob_files` / `open_directory`** handle the actual file and directory creation, including the placeholder substitution that swaps `FileName` in each template for the real problem name.

### `Templates/`
Contains one plain text template per supported language: C++, C, Java, and Python. I deliberately kept these as separate `.txt` files instead of hardcoding them as strings inside `project.py`. This was a conscious tradeoff. Hardcoding them would mean one less file to manage, but it would also mean my actual competitive programming boilerplate lives buried inside escaped Python strings, which is painful to read and edit. Keeping them as standalone files means I can update my template whenever I want, without touching a single line of the program's logic, and the templates stay readable as what they actually are: real C++, C, Java, and Python files.

### `test_project.py`
Covers the three functions that do not depend on external side effects: `get_contest_ID`, `get_problem_names`, and `create_lang_files_names`. I used `unittest.mock.patch` to mock `requests.get` and `os.mkdir` so the test suite runs instantly, does not depend on Codeforces being online, and does not touch the real filesystem. I intentionally left the file writing functions out of the automated tests, since testing those meaningfully would mean either touching real disk state or mocking so much of the function that the test would stop verifying anything useful.

### `requirements.txt`
Lists the two external dependencies, `requests` for the API calls and `pytest` for the test suite.

## Design Decisions

**Why four separate languages instead of one generic template system?**
Each language needs genuinely different boilerplate. C++ needs fast IO pragmas and STL includes, Java needs an entire class wrapper with a scanner utility, and Python needs neither. Trying to force all of that through one generic template would have made the templates worse for every language just to save a small amount of code, so I kept them fully separate instead.

**Why exit on errors instead of raising exceptions up the stack?**
This is a command line tool that I run directly before a contest, not a library meant to be imported elsewhere. If the link is invalid or the API call fails, I want a short, readable message telling me exactly what went wrong so I can fix it and rerun the command immediately, not a stack trace to read through under time pressure.

**Why mock the network and filesystem calls in testing instead of testing end to end?**
I wanted the test suite to run the same way every time, regardless of internet connection or whether a folder with that name already happens to exist on disk. Mocking those two boundaries let me test the actual decision making logic in each function without the test results depending on anything outside the code itself.

This was a small project in scope, but it is one I plan to actually keep using every contest, which is what made building it worthwhile.
