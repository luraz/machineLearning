import os
from  threading import Event, Thread
import xml.etree.ElementTree as ET
from multiprocessing import Process, Queue, Lock
import copy
import subprocess
import multiprocessing
import time

def getRootXml(xmlPath):
	tree = ET.parse(xmlPath)
	root = tree.getroot()
	return root

def initQueue(queue, nb):
	zerolist = []
	for i in range(nb):
		zerolist.append(0)
	queue.put(zerolist)

def makeThreadsList(root):
	listThreads = []

	for child in root:
		params = []
		threadName = child.attrib["name"]
		threadId = child.attrib["id"]

		threadcmdlist = ["python", child.find("script").text]
		if len(threadcmdlist) == 1:
			print ("len is 0")
			continue
		for param in child.findall("param"):
			threadcmdlist.append(param.text)

		waitFor = []
		for idThread in child.findall("waitfor"):
			try:
				waitFor.append(int(idThread.text))
			except ValueError:
				pass

		thread = {"name" : threadName, "cmd" : threadcmdlist, "waitFor" : waitFor, "id" : int(threadId)}
		listThreads.append(thread)
	
	return listThreads

def manageThreads(listThreads, queue):
	lock = Lock()
	copyListThreads = copy.copy(listThreads)
	while True:
		if len(copyListThreads) == 0: 
			break
		lock.acquire()
		zerolist = queue.get()
		queue.put(zerolist)
		lock.release()
		# print "*" * 80
		for index, thread  in enumerate(listThreads):
			threadIswaitingFor = thread["waitFor"]
			wait = False
			for idThread in threadIswaitingFor:
				if zerolist[idThread] != 1:
					wait = True
			if not wait:
				if zerolist[thread["id"]] == 0:
					copyListThreads.remove(thread)
					p = multiprocessing.Process(target=startThread, args=(thread, queue, lock))
					p.start()
					time.sleep(3)
		

def startThread(thread, queue, lock ):
	print ("starting %s " % thread["name"])
	lock.acquire()
	zerolist = queue.get()
	zerolist[thread["id"]] = 2
	queue.put(zerolist)
	lock.release()

	threadChild = subprocess.Popen(" ".join(thread["cmd"]), shell=True)

	threadChild.wait()

	print ("here")

	lock.acquire()
	zerolist = queue.get()
	zerolist[thread["id"]] = 1
	queue.put(zerolist)
	lock.release()
	print ("thread %s finished " % thread["name"])

def run(xmlPath):
	queue = Queue()
	
	root = getRootXml(xmlPath)
	listThreads = makeThreadsList(root)
	initQueue(queue, len(listThreads))
	manageThreads(listThreads, queue)

def main():
	xmlPath = "threads.xml"
	if not os.path.isfile(xmlPath):
		print ("Not a valid xml path %s " % xmlPath)
	run(xmlPath)

if __name__ == '__main__':
	main()