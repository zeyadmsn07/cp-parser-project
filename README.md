# CP Parser

#### Video Demo: https://youtu.be/u70oEHAkTlY?si=qIT0T8h2Ql0qeQAl

#### Description:

CP Parser is a command line tool that automates the file setup required before a Codeforces contest. Rather than manually creating a folder, copying a template into a new file for each problem, and renaming the solve function every time, the tool handles all of this from a single command with the contest link. What previously took a few minutes of repetitive setup now takes a few seconds, which matters more than it might seem once the contest clock has already started.

## What It Does

Given a Codeforces contest URL, a target language, and an optional folder name, CP Parser:

1. Extracts the contest ID from the URL
2. Fetches the list of problems in that contest through the Codeforces API
3. Creates a new directory for the contest
4. Generates one source file per problem, each pre-loaded with the configured template and a solve function named after the corresponding problem

## Usage

```
python project.py -l https://codeforces.com/contest/2246 -L cpp -d Round1
```

This creates a `Round1` folder alongside the project directory, containing a `.cpp` file for every problem in the contest, each one ready to code in immediately.

## Project Structure

### `Parse.py`
Defines the `Parser` class, a subclass of `ArgumentParser`, which registers the three flags the tool accepts: `-L` for language, `-l` for the contest link, and `-d` for the directory name. Argument parsing was kept in a separate file from `project.py` so the CLI definition would not become tangled with the program's core logic, and so the logic functions could be imported and tested in isolation without pulling in argument parsing each time.

### `project.py`
This is where the core logic lives.

- **`get_contest_ID(link)`** extracts the numeric contest ID from the URL using a regular expression rather than simple string splitting. Regex was chosen specifically because Codeforces URLs are not all shaped the same way. Group contests and private contests both introduce additional path segments before the contest ID, so a plain `split("/")` approach would fail on those cases. The regex accounts for the standard format along with these variants in a single pass, and if the link does not match at all, the function exits with a clear error message instead of surfacing a raw traceback.
- **`get_problem_names(ID)`** queries the Codeforces API and returns the problem list for the given contest. It checks the `status` field in the response and exits with a descriptive message if the API does not return `OK`, rather than allowing a failed or malformed request to fail silently further down the program.
- **`create_lang_files_names(names, lang)`** converts problem names into valid filenames for the selected language. The language argument is normalized with `.lower().strip()` so the tool is not sensitive to input casing, since typing `CPP` instead of `cpp` should not be the difference between the tool working and exiting with an error.
- **`open_prob_files` / `open_directory`** handle file and directory creation, including the placeholder substitution that replaces `FileName` in each template with the actual problem name.

### `Templates/`
Contains one plain text template per supported language: C++, C, Java, and Python. These were deliberately kept as separate `.txt` files rather than hardcoded strings inside `project.py`. Hardcoding them would have meant one less file to manage, but it would also mean the actual competitive programming boilerplate lives buried inside escaped Python strings, which is difficult to read and maintain. Keeping them as standalone files allows the templates to be updated independently of the program's logic, and keeps them readable as what they actually are: real C++, C, Java, and Python source files.

### `test_project.py`
Covers the three functions that do not depend on external side effects: `get_contest_ID`, `get_problem_names`, and `create_lang_files_names`. `unittest.mock.patch` is used to mock `requests.get` and `os.mkdir`, so the test suite runs instantly, does not depend on Codeforces being online, and does not touch the real filesystem. The file writing functions were intentionally excluded from automated testing, since testing them meaningfully would require either touching real disk state or mocking so much of the function that the test would no longer verify anything useful.

### `requirements.txt`
Lists the two external dependencies: `requests` for API calls and `pytest` for the test suite.

## Design Decisions

**Why four separate languages instead of one generic template system?**
Each language requires substantially different boilerplate. C++ needs fast IO pragmas and STL includes, Java needs an entire class wrapper with a scanner utility, and Python needs neither. Forcing all of this through a single generic template would have degraded the quality of the templates for every language in exchange for a modest reduction in code, so the languages were kept fully separate instead.

**Why exit on errors instead of raising exceptions up the stack?**
This is a command line tool run directly before a contest, not a library intended to be imported elsewhere. If the link is invalid or the API call fails, the priority is a short, readable message describing exactly what went wrong, so it can be corrected and the command rerun immediately, rather than a stack trace to parse under time pressure.

**Why mock the network and filesystem calls in testing instead of testing end to end?**
The goal was a test suite that behaves identically on every run, regardless of internet connectivity or whether a folder with a given name already exists on disk. Mocking those two boundaries allows the actual decision making logic in each function to be tested without the results depending on anything outside the code itself.

This was a small project in scope, but it is one that continues to see regular use every contest, which is what made building it worthwhile.
