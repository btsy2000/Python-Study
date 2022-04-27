# from queue import Queue
# import threading
# import time
#
# exitFlag = 0
#
#
# class MyThread (threading.Thread):
#    def __init__(self, threadID, name, q):
#       threading.Thread.__init__(self)
#       self.threadID = threadID
#       self.name = name
#       self.q = q
#    def run(self):
#       print ("Starting " + self.name)
#       process_data(self.name, self.q)
#       print ("Exiting " + self.name)
#
#
# def process_data(threadName, q):
#    while not exitFlag:
#       queueLock.acquire()
#       if not workQueue.empty():
#          data = q.get()
#          queueLock.release()
#          print ("%s processing %s" % (threadName, data))
#       else:
#          queueLock.release()
#       time.sleep(1)
#
#
# threadList = ["Thread-1", "Thread-2", "Thread-3"]
# nameList = ["One", "Two", "Three", "Four", "Five"]
# queueLock = threading.Lock()
# workQueue = Queue(10)
# threadID = 1
# threads = []
#
# # Create new threads
# for tName in threadList:
#     thread = MyThread(threadID, tName, workQueue)
#     thread.start()
#     threads.append(thread)
#     threadID += 1
#
# # Fill the queue
# queueLock.acquire()
# for word in nameList:
#    workQueue.put(word)
# queueLock.release()
#
# # Wait for queue to empty
# while not workQueue.empty():
#    pass
#
# # Notify threads it's time to exit
# exitFlag = 1
#
# # Wait for all threads to complete
# for t in threads:
#    t.join()
# print ("Exiting Main Thread")


import logging
import threading
import time
import concurrent.futures




def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name)
#
#
# if __name__ == "__main__":
#     format = "%(asctime)s: %(message)s"
#     logging.basicConfig(format=format, level=logging.INFO,
#                         datefmt="%H:%M:%S")
#
#     logging.info("Main    : before creating thread")
#     x = threading.Thread(target=thread_function, args=(1,)
#                          # , daemon=True
#                          )
#     logging.info("Main    : before running thread")
#     x.start()
#     logging.info("Main    : wait for the thread to finish")
#     # x.join()
#     logging.info("Main    : all done")


# class FakeDatabase:
#    def __init__(self):
#       self.value = 0
#       self._lock = threading.Lock()
#
#    def locked_update(self, name):
#       logging.info("Thread %s: starting update", name)
#       logging.debug("Thread %s about to lock", name)
#       with self._lock:
#          logging.debug("Thread %s has lock", name)
#          local_copy = self.value
#          local_copy += 1
#          time.sleep(0.1)
#          self.value = local_copy
#          logging.debug("Thread %s about to release lock", name)
#       logging.debug("Thread %s after release", name)
#       logging.info("Thread %s: finishing update", name)
#
#
# if __name__ == "__main__":
#     format = "%(asctime)s: %(message)s"
#     logging.basicConfig(format=format, level=logging.INFO,
#                         datefmt="%H:%M:%S")
#     logging.getLogger().setLevel(logging.DEBUG)
#     database = FakeDatabase()
#     logging.info("Testing update. Starting value is %d.", database.value)
#     with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
#         for index in range(2):
#             executor.submit(database.locked_update, index)
#     logging.info("Testing update. Ending value is %d.", database.value)


import random
import queue


class Pipeline(queue.Queue):
    def __init__(self):
        super().__init__(maxsize=10)

    def get_message(self, name):
        logging.debug("%s:about to get from queue", name)
        value = self.get()
        logging.debug("%s:got %d from queue", name, value)
        return value

    def set_message(self, value, name):
        logging.debug("%s:about to add %d to queue", name, value)
        self.put(value)
        logging.debug("%s:added %d to queue", name, value)


def producer(pipeline, event):
   """Pretend we're getting a number from the network."""
   while not event.is_set():
      message = random.randint(1, 101)
      logging.info("Producer got message: %s", message)
      pipeline.set_message(message, "Producer")

   logging.info("Producer received EXIT event. Exiting")


def consumer(pipeline, event):
   """Pretend we're saving a number in the database."""
   while not event.is_set() or not pipeline.empty():
      message = pipeline.get_message("Consumer")
      logging.info(
         "Consumer storing message: %s  (queue size=%s)",
         message,
         pipeline.qsize(),
      )

   logging.info("Consumer received EXIT event. Exiting")


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    # logging.getLogger().setLevel(logging.DEBUG)

    pipeline = Pipeline()
    event = threading.Event()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline, event)
        executor.submit(consumer, pipeline, event)

        time.sleep(0.001)
        logging.info("Main: about to set event")
        event.set()