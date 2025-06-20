from datetime import datetime
class LogInformation:
    def __init__(self, log_line):
        """Example level_with_logging_info - 'INFO: Server started on port 8080'"""
        current_list_info = log_line.split()
        current_list_info[2] = current_list_info[2][:-1]
        self.dt = datetime.strptime(current_list_info[0] + " " + current_list_info[1], "%Y-%m-%d %H:%M:%S")
        self.level = current_list_info[2]
        self.log_info = " ".join(current_list_info[3:])