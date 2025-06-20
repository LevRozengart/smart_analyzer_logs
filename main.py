from tools import *

parser = LogParser("test_app.log")
analyzer = LogAnalyzer(parser)
print(analyzer.get_statistics_by_level())
