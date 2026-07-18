from argparse import ArgumentParser

desc = "CLI program to organise all you CP problems in one folder.\nYou can choose between 4 different programming languages and build you own CP kingdom!"

class Parser(ArgumentParser):
    def __init__(self):
        super().__init__(description=desc)
        self.add_argument(
            "-L", "--language", default="cpp", help="Specifies the solution language (cpp, python, etc.).", type=str
        )
        self.add_argument(
            "-l", "--link", help="Specifies the CodeForces contest link.", type=str
        )
        self.add_argument(
            "-d", "--directory", help="Specify directory name (use terminal quoting for names with spaces!).", default="CP_directory", type=str
        )
        