class ProgressBar:
    def __init__(self, finish, text='progress'):
        self.counter = 0.0
        self.finish = finish 
        self.one_percent = finish / 100
        self.text = text

    def current_percentage(self):
        if self.counter >= self.finish:
            return 100
        return self.counter / self.one_percent

    def write_to_console(self):
        now = int(self.current_percentage())
        print("\r{}: {:3d}/100".format(self.text, now), end="")

    def set(self, current_amount):
        self.counter = current_amount
        self.write_to_console()

    def add(self, amount_to_increment):
        self.counter += amount_to_increment
        self.write_to_console()