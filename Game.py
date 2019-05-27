import curses
from curses import textpad
import time
import random

menu = ['Instructions', 'Play', 'Exit', 'About the game']
playMenu = ['Easy', 'Medium', 'Hard']
exitMenu = ['Yes', 'No']
about_txt = 'Snake is the common name for a video game concept where the player maneuvers a line which grows in length, with the line itself being a primary obstacle. The concept originated in the 1976 arcade game Blockade, and the ease of implementing Snake has led to hundreds of versions (some of which have the word snake or worm in the title) for many platforms. After a variant was preloaded on Nokia mobile phones in 1998, there was a resurgence of interest in the snake concept as it found a larger audience. There are over 300 Snake-like games for iOS alone.'
instruction_txt = 'Initially length of your snake will be three. Once you eat a piece of food your length of your snake will increase by one. If the snake touches its own body or the boundary of the arena, game will be over.' 
f = 0
def print_menu(stdscr, idx, menu, heading):
    stdscr.clear()
    stdscr.addstr(0, 0, heading)
    h, w = stdscr.getmaxyx()
    for i, row in enumerate(menu):
        x = w//2 - len(row)//2
        y = h//2 - len(menu)//2 + i
        if i == idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
        stdscr.refresh()

def create_food(snake, arena):
    food = None
    while food is None:
        food = [random.randint(arena[0][0]+1, arena[1][0]-1), random.randint(arena[0][1]+1, arena[1][1]-1)]
        if food in snake:
            food = None
    return food

def print_score(stdscr, score):
    sh, sw = stdscr.getmaxyx()
    score_txt = 'Score = {}'.format(score)
    stdscr.addstr(0, sw//2-len(score_txt)//2, score_txt)
    stdscr.refresh()

def game(stdscr, level):
    curses.curs_set(0)
    stdscr.nodelay(1)
    if level == 0:
        stdscr.timeout(250)
    elif level == 1:
        stdscr.timeout(150)
    else:
        stdscr.timeout(50)
    
    sh, sw = stdscr.getmaxyx()
    arena = [[2, 2], [sh-2, sw-2]]
    textpad.rectangle(stdscr, arena[0][0], arena[0][1], arena[1][0], arena[1][1])
    
    snake = [[sh//2, sw//2+1], [sh//2, sw//2], [sh//2, sw//2-1]]
    direction = curses.KEY_RIGHT
    
    for y, x in snake:
        stdscr.addstr(y, x, '#')
    
    food = create_food(snake, arena)
    stdscr.addstr(food[0], food[1], '$')
    score = 0
    print_score(stdscr, score)
    
    while 1:
        k = stdscr.getch()
        if k in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_RIGHT, curses.KEY_LEFT]:
            direction = k
        
        head = snake[0]
        
        if direction == curses.KEY_RIGHT:
            new_head = [head[0], head[1]+1]
        elif direction == curses.KEY_LEFT:
            new_head = [head[0], head[1]-1]
        elif direction == curses.KEY_UP:
            new_head = [head[0]-1, head[1]]
        elif direction == curses.KEY_DOWN:
            new_head = [head[0]+1, head[1]]
            
        snake.insert(0, new_head)
        stdscr.addstr(new_head[0], new_head[1], '#')
        
        if snake[0] == food:
            food = create_food(snake, arena)
            stdscr.addstr(food[0], food[1], '$')
            score += 1
            print_score(stdscr, score)
        else:
            stdscr.addstr(snake[-1][0], snake[-1][1], ' ')
            snake.pop()
        
        if snake[0][0] in [arena[0][0], arena[1][0]] or snake[0][1] in [arena[0][1], arena[1][1]] or snake[0] in snake[1:]:
            msg = 'Game Over!'
            score_txt = 'Your Score = {}'.format(score)
            stdscr.clear()
            stdscr.addstr(sh//2, sw//2-len(msg)//2, msg)
            stdscr.addstr(sh//2+1, sw//2-len(msg)//2, score_txt)
            stdscr.refresh()
            time.sleep(4)
            break
        stdscr.refresh()
        
def main(stdscr, f):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    current_row_idx = 0
    print_menu(stdscr, current_row_idx, menu, 'Snakes Game')
    
    while 1:    
        key = stdscr.getch()
        stdscr.clear()
        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(menu) - 1:
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if menu[current_row_idx] == 'Instructions':
                stdscr.clear()
                stdscr.addstr(0, 0, instruction_txt)
                stdscr.refresh()
                time.sleep(5)
            elif menu[current_row_idx] == 'About the game':
                stdscr.clear()
                stdscr.addstr(0, 0, about_txt)
                stdscr.refresh()
                time.sleep(5)
            elif menu[current_row_idx] == 'Play':
                heading = 'Select Difficulty Level: '
                idx = 0
                print_menu(stdscr, idx, playMenu, heading)
                stdscr.refresh()
                while 1:
                    k = stdscr.getch()
                    stdscr.clear()
                    if k == curses.KEY_UP and idx > 0:
                        idx -= 1
                    elif k == curses.KEY_DOWN and idx < len(playMenu)-1:
                        idx += 1
                    elif k == curses.KEY_ENTER or k in [10, 13]:
                        curses.wrapper(game, idx)
                        f = 1
                        break
                    print_menu(stdscr, idx, playMenu, heading)
                    stdscr.refresh()
            elif menu[current_row_idx] == 'Exit':
                idx = 0
                print_menu(stdscr, idx, exitMenu, 'Do you want to exit?')
                stdscr.refresh()
                while 1:
                    k = stdscr.getch()
                    stdscr.clear()
                    if k == curses.KEY_UP and idx > 0:
                        idx -= 1
                    elif k == curses.KEY_DOWN and idx < len(exitMenu) - 1:
                        idx += 1
                    elif k == curses.KEY_ENTER or k in [10, 13]:
                        if exitMenu[idx] == 'No':
                            current_row_idx = 0
                            print_menu(stdscr, current_row_idx, menu, 'Snakes Game')
                            stdscr.refresh()
                            stdscr.getch()
                        else:
                            f = 2
                        break
                    print_menu(stdscr, idx, exitMenu, 'Do you want to exit?')
                    stdscr.refresh()
            stdscr.refresh()
            stdscr.getch()
        if f == 1:
            f = 0
            curses.wrapper(main, f)
            break
        elif f == 2:
            break
        print_menu(stdscr, current_row_idx, menu, 'Snakes Game')
        stdscr.refresh()
                
curses.wrapper(main, f)
