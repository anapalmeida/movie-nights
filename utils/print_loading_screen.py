import sys
import time
import threading

def spinning_cursor(stop_event, text="Loading"):
    while not stop_event.is_set():
        for cursor in '|/-\\':
            if stop_event.is_set():
                break
            sys.stdout.write(f'\r{text} {cursor}')
            sys.stdout.flush()
            time.sleep(0.1)

def print_loading_animation(text="Loading"):
    stop_event = threading.Event()
    animation_thread = threading.Thread(target=spinning_cursor, args=(stop_event, text))
    animation_thread.start()
    return stop_event