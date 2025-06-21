from tools import *

parser = LogParser("test_app.log")
analyzer = LogAnalyzer(parser)


get_stat_to_json("stats.json", parser)
lines_bet_8_9 = analyzer.filter_by_time_range("2023-10-05 08:00:00", "2023-10-05 09:00:00")
print(lines_bet_8_9)