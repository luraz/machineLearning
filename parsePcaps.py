import os
import dpkt #de instalat
import ntpath
import sys


class pcapParser:
	def __init__(self, pcapPath, dstFolder):
		self.pcapPath = pcapPath
		self.dstFolder = dstFolder

	def parsePcap(self):
		pairs = []
		dataStreams = {}
		i = 0
		f = open(self.pcapPath, "rb")
		if True:
			pcap = dpkt.pcap.Reader(f)

			for ts, buf in pcap:
				eth = dpkt.ethernet.Ethernet(buf)
				ip = eth.data
				tcp = ip.data

				if b"GET" in tcp.data or b"POST" in tcp.data:
					print ("yes")
					pair = [ip.src, ip.dst]
					if pair not in pairs:
						pairs.append(pair)
					print (pairs)
					continue

				if b"HTTP/1.0 200 OK" in tcp.data:
					continue 

				print(len(ip.src))

				for index, pair in enumerate(pairs):
					ipsrc, ipdest = pair
					if len(tcp.data) > 0 and ip.src == ipdest and ip.dst == ipsrc:
						if index not in  dataStreams:
							dataStreams[index] = []
						dataStreams[index].append(str(tcp.data))

			# print (dataStreams)
			f.close()
			for key in dataStreams:
				srcFilename = "%s%04d.txt" % (os.path.splitext(ntpath.basename(self.pcapPath))[0], i)
				i += 1
				pathSrcFile = os.path.join(self.dstFolder, srcFilename)
				f = open(pathSrcFile, "w")
				f.write("".join(dataStreams[key]))
				f.close()

def main(argv):
	pcapPath = "/home/laura/work/workdir/pcap/scenarii/infected/mal/mal_Trojan.JS.Redirector.UZ_0187be7dd118578190b2a2777afed196.aaa.zip.pcap"
	dstFolder = "/home/laura/games/pcaps"
	if len(argv) > 1:
		pcapPath = argv[1]
	if len(argv) == 3:
		dstFolder = argv[2]
	parser = pcapParser(pcapPath, dstFolder)
	parser.parsePcap()


if __name__ == '__main__':
	main(sys,argv)
