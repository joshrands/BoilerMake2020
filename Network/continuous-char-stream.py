import time
import curses

ENTER_KEY = (curses.KEY_ENTER, ord('\n'), ord('\r'))

def run(win, timeout=3): # timeout in seconds
    curses.echo()
    win.timeout(0) # Non-block read.

    line = 0
    while True:
        win.addstr(line, 0, "Enter something: ")
        s = []
        start = time.time()
        run = True
        while run:
            c = win.getch()
            time_taken = time.time() - start

            if c < 0:
                pass
            elif c in ENTER_KEY:
                break
            else:
                s.append(chr(c))

            if time_taken >= timeout:
                # Out of time.
                s.append(-1)
                run = False

        if len(s) == 0:
            break
        if s[-1] == -1:
            s.pop()
        answer = ''.join(s)
        win.addstr(line + 1, 0, "Your input was: %s" % answer)
        line += 2

curses.wrapper(run)

