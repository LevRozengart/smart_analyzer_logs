from datetime import datetime
import json
from itertools import chain


class LogInformation:
    def __init__(self, log_line):
        """Example level_with_logging_info - 'ERROR INFO: Server started on port 8080'"""
        current_list_info = log_line.split()
        current_list_info[2] = current_list_info[2][:-1]
        self.dt = datetime.strptime(current_list_info[0] + " " + current_list_info[1], "%Y-%m-%d %H:%M:%S")
        self.level = current_list_info[2]
        self.log_info = " ".join(current_list_info[3:])


class LogParser:
    def __init__(self, file_path):
        self.file_path = file_path

    def get_iterator(self):
        """yield LogInformation object"""
        with open(self.file_path, "r") as file:
            for line_num, line in enumerate(file, 1):
                try:
                    yield LogInformation(line)
                except Exception as e:
                    print(f"Skip line {line_num}: {str(e)}")
                    continue


class LogAnalyzer:
    def __init__(self, parser: LogParser):
        self.parser = parser
        self.log_lines = self.parser.get_iterator()
        self.use_cache_iterator_to_list = False

    def enable_cache(self):
        self.use_cache_iterator_to_list = True

    def disable_cache(self):
        self.use_cache_iterator_to_list = False

    def check_is_empty_iter(self):
        try:
            a = next(self.log_lines)
            self.log_lines = chain([a], self.log_lines)
            return False
        except:
            return True

    def update_log_lines(self):
        flag = self.check_is_empty_iter()
        if flag:
            if self.use_cache_iterator_to_list:
                self.log_lines = list(self.parser.get_iterator())
            else:
                self.log_lines = self.parser.get_iterator()

    def get_statistics_by_level(self, by_dt: str = False):
        """examle by_dt: '2007-10-30 (year-month-day)'"""
        self.update_log_lines()
        statistic_of_levels = {}
        if by_dt:
            for line in self.log_lines:
                if line.dt.date() == datetime.strptime(by_dt, "%Y-%m-%d").date():
                    statistic_of_levels[line.level] = statistic_of_levels.get(line.level, 0) + 1
        else:
            for line in self.log_lines:
                statistic_of_levels[line.level] = statistic_of_levels.get(line.level, 0) + 1
        return statistic_of_levels

    def give_time_cells(self, time: datetime):
        if time.hour < 6:
            return "night"
        elif 6 <= time.hour < 12:
            return "morning"
        elif 12 <= time.hour < 18:
            return "afternoon"
        else:
            return "evening"

    def get_statistics_by_datetime(self):
        self.update_log_lines()

        dict_dates = {}
        for line in self.log_lines:
            dict_dates.setdefault(line.dt.date(), {
                "night": 0,  # 00:00 - 06:00
                "morning": 0,  # 06:00 - 12:00
                "afternoon": 0,  # 12:00 - 18:00
                "evening": 0  # 18:00 - 24:00
            })
            dict_dates[line.dt.date()][self.give_time_cells(line.dt)] += 1
        return dict_dates

    def get_most_ofter_error(self) -> tuple[str, int]:
        self.update_log_lines()
        md = {}
        for line in self.log_lines:
            md[line.log_info] = md.get(line.log_info, 0) + 1
        most_often = max(md.items(), key=lambda x: x[1])
        return most_often

    def to_str(self, line: LogInformation):
        return f"{line.dt} {line.level}: {line.log_info}"

    def filter_by_time_range(self, start: str, end: str, fn: str = None, to_file: bool = False):
        start = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
        td = end - start
        if td.seconds / (60 * 60) > 3:
            return "end - start should benn less than 3 hours"
        self.update_log_lines()
        needed_lines = [self.to_str(line) for line in self.log_lines if start <= line.dt <= end]
        if to_file:
            with open(fn, "w") as f:
                f.writelines(needed_lines)
            return "log was written to file"
        return needed_lines


def get_stat_to_json(fn: str, parser: LogParser, dt: str = None):
    analyzer_obj = LogAnalyzer(parser)
    stat_by_level = analyzer_obj.get_statistics_by_level(by_dt=dt)
    stats = analyzer_obj.get_statistics_by_datetime()
    with open(fn, "w") as f:
        json.dump(stat_by_level, f, indent=2)