from pytest import raises
from unittest.mock import patch
import project

def test_get_contest_ID():
    assert project.get_contest_ID("https://codeforces.com/contest/2246") == "2246"
    assert project.get_contest_ID("https://codeforces.com/group/vtfsyP8jkN/contest/591913") == "591913"
    assert project.get_contest_ID("http://www.codeforces.com/contest/private/183") == "183"
    with raises(SystemExit):
        project.get_contest_ID("https://codeforces/contest/2246")
    with raises(SystemExit):
        project.get_contest_ID("http://amazon.com/product/9222")
    with raises(SystemExit):
        project.get_contest_ID("https://codeforces.com/contest2246")

@patch("project.requests.get")
def test_get_problem_names(mocked):
    mocked.return_value.json.return_value = {
        "status": "OK",
        "result":{
            "problems":[
                {"name": "Bing", "index": "A"},
                {"name": "SHAWARMA", "index": "B"}
                ]
            }
    }
    returned = project.get_problem_names(911)
    assert returned == [
                {"name": "Bing", "index": "A"},
                {"name": "SHAWARMA", "index": "B"}
                ]
    mocked.assert_called_once_with("https://codeforces.com/api/contest.standings?contestId=911")
    mocked.return_value.json.return_value = {
        "status": "NONE",
        "result":{
            "problem":[
                {"name": "Bing", "index": "A"},
                {"name": "SHAWARMA", "index": "B"}
                ]
            }
    }
    with raises(SystemExit):
        project.get_problem_names(122)

def test_create_lang_files_names():
    names = ["Bingo", "Shawarma", "Peps peps"]
    assert project.create_lang_files_names(names, "CPP") == ["Bingo.cpp", "Shawarma.cpp", "Peps_peps.cpp"]
    assert project.create_lang_files_names(names, "  pY") == ["Bingo.py", "Shawarma.py", "Peps_peps.py"]
    with raises(SystemExit):
        project.create_lang_files_names(names, "js")
    
@patch("project.os.mkdir")
def test_open_directory(mocked):
    project.open_directory("Ahmed")
    mocked.assert_called_once_with("../Ahmed")
    mocked.side_effect = FileExistsError
    with raises(SystemExit):
        project.open_directory("Hamada")
