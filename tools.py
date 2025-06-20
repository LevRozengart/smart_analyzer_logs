from datetime import datetime


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
            for line in file:
                yield LogInformation(line)


class LogAnalyzer:
    def __init__(self, iterator_lines: LogParser):
        self.parser = iterator_lines

    def get_statistics_by_level(self):
        iterator_of_lines = self.parser.get_iterator()
        statistic_of_levels = {}
        for line in iterator_of_lines:
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
        iterator_of_lines = self.parser.get_iterator()

        dict_dates = {}
        for line in iterator_of_lines:
            dict_dates.setdefault(line.dt.date(), {
                "night": 0,  # 00:00 - 06:00
                "morning": 0,  # 06:00 - 12:00
                "afternoon": 0,  # 12:00 - 18:00
                "evening": 0  # 18:00 - 24:00
            })
            dict_dates[line.dt.date()][self.give_time_cells(line.dt)] += 1
        return dict_dates
