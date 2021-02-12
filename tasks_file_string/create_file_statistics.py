import random
def creator_file(count_line = 100):
    """Function for generating a fake log of site activity"""
    ip = ("213.27.152.15","190.93.176.11","37.59.115.136","89.191.131.243","190.117.115.150","5.197.231.174","180.247.131.229")
    week_day = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday","sunday")
    for line in range(count_line):
        hour = random.choice(range(24))
        minute = random.choice(range(60))
        seconds = random.choice(range(60))
        log_line =f"{random.choice(ip)} | {hour}:{minute}:{seconds} | {random.choice(week_day)}"
        print(log_line)
        with open ("task_4_statistics.txt",mode = 'a', encoding="UTF8") as file:
            file.write(log_line + "\n")


if __name__ == '__main__':
    creator_file()