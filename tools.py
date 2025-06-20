from datetime import datetime
class LogInformation:
    def __init__(self, log_line):
        """Example level_with_logging_info - 'INFO: Server started on port 8080'"""
        current_list_info = log_line.split()
        current_list_info[2] = current_list_info[2][:-1]
        self.dt = datetime.strptime(current_list_info[0] + " " + current_list_info[1], "%Y-%m-%d %H:%M:%S")
        self.level = current_list_info[2]
        self.log_info = " ".join(current_list_info[3:])


class LogParser:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_file(self):
        with open(self.file_path, "r") as file:
            for line in file:
                yield LogInformation(line)
