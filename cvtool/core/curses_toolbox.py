''' 
A list editor written in ncurses. 

*** Use of this program requires attribution. ***

Author: Daniel Ellis
github: @wolfiex
email:  curses_toolbox@danielellisresearch.com

Modification and Usage for CMIP granted by author: 
daniel.ellis@ext.esa.int
'''



import curses

def get_terminal_lines():
    stdscr = curses.initscr()
    num_lines, _ = stdscr.getmaxyx()
    curses.endwin()
    return num_lines


def reformat(items):
    if isinstance( items, dict ): items = items.items()
    if type(items) is type(dict().items()): items = [[*i] for i in items]
    if isinstance(items,list) and not isinstance(items[0],list) : items =  [[*i] for i in enumerate(items)]
    import pprint
    pprint.pprint(items)
    return items




class CursesEditor:
    def __init__(self, items, save_func=None, check=None):
        items=reformat(items)
        print(type(items),type(items[0]),items)
        self.items = reformat(items)
        self.historic = self.items.copy()

        self.save_func = save_func
        self.check = check
        self.selected_row = 0

    def display_items(self, stdscr):
        stdscr.clear()

        for i, row in enumerate(self.items):
            if i == self.selected_row:
                stdscr.addstr(i, 0, f"{row[0]} : {row[1]}", curses.color_pair(1))
            else:
                stdscr.addstr(i, 0, f"{row[0]} : {row[1]}")

        if self.selected_row == len(self.items):
            stdscr.addstr(len(self.items), 0, "Save", curses.color_pair(2) | curses.A_REVERSE)
        else:
            stdscr.addstr(len(self.items), 0, "Save", curses.color_pair(2))
        if self.selected_row == len(self.items) + 1:
            stdscr.addstr(len(self.items) + 1, 0, "Quit", curses.color_pair(2) | curses.A_REVERSE)
        else:
            stdscr.addstr(len(self.items) + 1, 0, "Quit", curses.color_pair(2))

        stdscr.refresh()

    def edit_value(self, stdscr):
        stdscr.move(self.selected_row, len(self.items[self.selected_row][0]) + 2)
        stdscr.clrtoeol()

        curses.echo()
        new_value = stdscr.getstr().decode()

        if not self.is_valid(self.items[self.selected_row][0] , new_value):
            stdscr.addstr(len(self.items) + 2, 0, "Invalid value!", curses.A_BOLD)
            stdscr.refresh()
            stdscr.getch()
        else:
            self.items[self.selected_row][1] = new_value
            curses.noecho()
            self.check_value(stdscr)

    def check_value(self, stdscr):
        value = self.items[self.selected_row][1]
        if value == 'invalid':
            stdscr.addstr(len(self.items) + 2, 0, "Invalid value!", curses.A_BOLD)
        else:
            stdscr.addstr(len(self.items) + 2, 0, "Value is valid.", curses.A_BOLD)
        stdscr.refresh()

    def save_items(self):
        if self.save_func is not None:
            return self.save_func(self.items)
        return False

    def is_valid(self,key, value):
        if self.check is None: return True
        else: 
            return self.check(value)

    def main(self, stdscr):
        curses.curs_set(0)
        stdscr.keypad(1)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

        while True:
            self.display_items(stdscr)
            key = stdscr.getch()

            if key == curses.KEY_UP and self.selected_row > 0:
                self.selected_row -= 1
            elif key == curses.KEY_DOWN and self.selected_row < len(self.items) + 1:
                self.selected_row += 1
            elif key == curses.KEY_ENTER or key in [10, 113, 115, 110,101,114]:
                #[ord('\n'), ord('q'), ord('s'), ord('n'), ord('e'),ord(r)]:
                
                if self.selected_row == len(self.items) or key == ord('s'):
                    return self.save_items()
                    break
                elif self.selected_row == len(self.items) + 1 or key == ord('q'):
                    return False
                    break
                elif key == ord('r'):
                    curses.echo()
                    self.items[self.selected_row][1] = ''+self.historic[self.selected_row][1]
                    curses.noecho()

                elif self.selected_row < len(self.items) or key == ord('e'):
                        self.edit_value(stdscr)

        ######
        # fix revert
        #######
        stdscr.clear()
        stdscr.refresh()



class CursesSelector:
    def __init__(self, items, title=''):
        self.items = reformat(items)
        self.selected_row = 0
        self.n = get_terminal_lines() - 6
        self.title = title
    
    def display_items(self, stdscr):
        stdscr.clear()
        start_index = self.selected_row - (self.selected_row % self.n)
        end_index = min(start_index + self.n, len(self.items))

        title = f" {self.title} "
        title_length = len(title)
        title_start = (stdscr.getmaxyx()[1] - title_length) // 2

        stdscr.attron(curses.color_pair(3))  # Apply the violet color pair
        stdscr.addstr(0, title_start, title)
        stdscr.attroff(curses.color_pair(3))  # Restore default color

        for i, row in enumerate(self.items[start_index:end_index], start=start_index):
            if i == self.selected_row:
                stdscr.addstr(i - start_index + 2, 0, f"{row[0]} : {row[1]}", curses.color_pair(1))
            else:
                stdscr.addstr(i - start_index + 2, 0, f"{row[0]} : {row[1]}")

        if self.selected_row >= len(self.items):
            stdscr.addstr(self.n + 2, 0, "Add New", curses.color_pair(2) | curses.A_REVERSE)
        else:
            stdscr.addstr(self.n + 2, 0, "Add New", curses.color_pair(2))

        if self.selected_row == len(self.items) + 1:
            stdscr.addstr(self.n + 3, 0, "Quit", curses.color_pair(2) | curses.A_REVERSE)
        else:
            stdscr.addstr(self.n + 3, 0, "Quit", curses.color_pair(2))

        counter_text = f"{start_index + 1} - {min(start_index + self.n, len(self.items))} items out of {len(self.items)}"
        stdscr.addstr(self.n + 4, 0, counter_text, curses.color_pair(2))

        stdscr.refresh()

    def select_value(self, stdscr):
        key = stdscr.getch()

        if key == curses.KEY_UP and self.selected_row > 0:
            self.selected_row -= 1
        elif key == curses.KEY_DOWN and self.selected_row < len(self.items) + 1:
            self.selected_row += 1
        elif key == curses.KEY_ENTER or key in [10,13,113, 115, 110]:
            if self.selected_row == len(self.items) or key == ord('n'):
                return 'new'
            elif self.selected_row == len(self.items) + 1 or key == ord('q'):
                return False
            else:
                value = list(self.items)[self.selected_row]
                return value

    def main(self, stdscr):
        curses.curs_set(0)
        stdscr.keypad(1)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

        while True:
            self.display_items(stdscr)
            result = self.select_value(stdscr)

            if result is not None:
                return result

        stdscr.clear()
        stdscr.refresh()

'''
# Example usage:
items = [
    ['Item 1', 'Value 1'],
    ['Item 2', 'Value 2'],
    ['Item 3', 'Value 3']
]


def valid(value):
        if value == 'invalid':
            return False
        return True


def save_items():
    # Custom save function
    print("Custom save function called.")

editor = CursesEditor(items, save_func=save_items,check = valid)
curses.wrapper(editor.main)

'''