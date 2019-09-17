import sched
import time

sch = sched.scheduler(time.time, time.sleep)

times = []

def print_time():
    t = time.time()
    times.append(t)
    print("From print_time", t)

def print_results():
    print("DELAY: ", times[1] - times[0])

def print_some_times():
    print(time.time)
    # args: delay, priority, actions, arg
    sch.enter(2, 1, print_time, ())
    sch.enter(4, 1, print_time, ())
    sch.enter(4.1,1, print_results, ())
    sch.run()
    print(time.time())

print_some_times()

# https://docs.python.org/2/library/sched.html
# scheduler.enterabs(time, priority, action, argument) -> event
# scheduler.enter(delay, priority, action, argument) -> event
# scheduler.cancel(event)
# scheduler.empty() -> boolean
# scheduler.run()
# scheduler.queue : list of events
#
