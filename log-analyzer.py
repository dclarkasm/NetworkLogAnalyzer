import os
import re
import urllib
import json

#---------------------------------------
# Created by: Devon Clark
# 11/22/2015
#---------------------------------------

http_codetype = {
	"1":"with Information",
	"2":"and was Successful",
	"3":"and Redirected",
	"4":"and encountered a Client Error",
	"5":"and encountered a Server Error"
}

http_code = {
#1xx Informational
	"100":"Continue",
	"101":"Switching Protocols",
	"102":"Processing (WebDAV)",

#2xx Success
	"200":"OK",
	"201":"Created",
	"202":"Accepted",
	"203":"Non-Authoritative Information",
	"204":"No Content",
	"205":"Reset Content",
	"206":"Partial Content",
	"207":"Multi-Status (WebDAV)",
	"208":"Already Reported (WebDAV)",
	"226":"IM Used",

#3xx Redirection
	"300":"Multiple Choices",
	"301":"Moved Permanently",
	"302":"Found",
	"303":"See Other",
	"304":"Not Modified",
	"305":"Use Proxy",
	"306":"(Unused)",
	"307":"Temporary Redirect",
	"308":"Permanent Redirect (experiemental)",

#4xx Client Error
	"400":"Bad Request",
	"401":"Unauthorized",
	"402":"Payment Required",
	"403":"Forbidden",
	"404":"Not Found",
	"405":"Method Not Allowed",
	"406":"Not Acceptable",
	"407":"Proxy Authentication Required",
	"408":"Request Timeout",
	"409":"Conflict",
	"410":"Gone",
	"411":"Length Required",
	"412":"Precondition Failed",
	"413":"Request Entity Too Large",
	"414":"Request-URI Too Long",
	"415":"Unsupported Media Type",
	"416":"Requested Range Not Satisfiable",
	"417":"Expectation Failed",
	"418":"I'm a teapot (RFC 2324)",
	"420":"Enhance Your Calm (Twitter)",
	"422":"Unprocessable Entity (WebDAV)",
	"423":"Locked (WebDAV)",
	"424":"Failed Dependency (WebDAV)",
	"425":"Reserved for WebDAV",
	"426":"Upgrade Required",
	"428":"Precondition Required",
	"429":"Too Many Requests",
	"431":"Request Header Fields Too Large",
	"444":"No Response (Nginx)",
	"449":"Retry With (Microsoft)",
	"450":"Blocked by Windows Parental Controls (Microsoft)",
	"499":"Client Closed Request (Nginx)",

#5xx Server Error
	"500":"Internal Server Error",
	"501":"Not Implemented",
	"502":"Bad Gateway",
	"503":"Service Unavailable",
	"504":"Gateway Timeout",
	"505":"HTTP Version Not Supported",
	"506":"Variant Also Negotiates (Experimental)",
	"507":"Insufficient Storage (WebDAV)",
	"508":"Loop Detected (WebDAV)",
	"509":"Bandwidth Limit Exceeded (Apache)",
	"510":"Not Extended",
	"511":"Network Authentication Required",
	"598":"Network read timeout error",
	"599":"Network connect timeout error"
}

ftp_code = {
	#100 Series	The requested action is being initiated, expect another reply before proceeding with a new command.
	"110":"Restart marker replay",
	"120":"Service ready in nnn minutes",
	"125":"Data connection already open",
	"150":"File status okay",
	#200 Series	
	"200":"Completed successfuly",
	"202":"Command not implemented",
	"211":"System status",
	"212":"Directory status",
	"213":"File status",
	"214":"Help message",
	"215":"NAME system type",
	"220":"Service ready for new user",
	"221":"Service closing control connection",
	"225":"Data connection open",
	"226":"Closing data connection",
	"227":"Entering Passive Mode",
	"228":"Entering Long Passive Mode",
	"229":"Entering Extended Passive Mode",
	"230":"User logged in, proceed",
	"231":"User logged out",
	"232":"Logout command noted",
	"234":"Server accepts the authentication mechanism",
	"250":"Requested file action completed",
	"257":"pathname was created",								##*****
	#300 Series	The command has been accepted, but the requested action is on hold, pending receipt of further information.
	"331":"User name okay, need password",
	"332":"Need account for login",
	"350":"Requested file action pending further information",
	#400 Series	The command was not accepted and the requested action did not take place, but the error condition is temporary and the action may be requested again.
	"421":"Service not available, closing control connection",
	"425":"Can't open data connection",
	"426":"Connection closed",
	"430":"Invalid username or password",
	"434":"Requested host unavailable",
	"450":"Requested file action not taken",
	"451":"Requested action aborted",
	"452":"Requested action not taken",
	#500 Series	
	"500":"Syntax error",
	"501":"Syntax error in parameters or arguments",
	"502":"Command not implemented",
	"503":"Bad sequence of commands",
	"504":"Command not implemented for that parameter",
	"530":"Not logged in",
	"532":"Need account for storing files",
	"550":"file unavailable",									##*****
	"551":"Page type unknown",
	"552":"Exceeded storage allocation",
	"553":"file name not allowed",								##*****
	#600 Series	Replies regarding confidentiality and integrity
	"631":"Integrity protected reply",
	"632":"Confidentiality and integrity protected reply",
	"633":"Confidentiality protected reply",
	#10000 Series	Common Winsock Error Codes
	"10054":"Connection reset by peer",
	"10060":"Cannot connect to remote server",
	"10061":"The connection is actively refused by the server",
	"10066":"directory not empty",								##*****
	"10068":"Server is full.",
}

ftp_method = {
	"ABOR":"Active file transfer abortion",
	"ACCT":"Account information",
	"ALLO":"Allocate sufficient disk space to receive a file",
	"APPE":"Append",
	"AUTH":"Authentication/Security Mechanism",
	"CCC":"Clear Command Channel",
	"CDUP":"Change to Parent Directory",
	"CHANGEPASSWORD":"Change password",
	"CLIENTCERT":"Client SSL certificate was rejected",
	"CLOSED":"End FTP session",
	"COMB":"Combines file segments into a single file on EFT Server",
	"CREATED":"File was created (uploaded)",
	"CWD":"Change working directory",
	"DELE":"Delete file",
	"EPRT":"Specifies an extended address and port to which the server should connect",
	"EPSV":"Enter extended passive mode",
	"FEAT":"Get the feature list implemented by the server",
	"HELP":"Display a list of all available FTP commands",
	"KICK":"Client connection was closed by administrator.",
	"LIST":"Returns information of a file or directory if specified, else information of the current working directory is returned",
	"MDTM":"Return the last-modified time of a specified file",
	"MKD":"Make directory",
	"MLSD":"Lists the contents of a directory if a directory is named",
	"MLST":"Provides data about exactly the object named on its command line, and no others",
	"MODE":"Sets the transfer mode (Stream, Block, or Compressed)",
	"NLIST":"Returns a list of file names in a specified directory",
	"NOOP":"No operation (dummy packet; used mostly on keepalives)",
	"OPTS":"Select options for a feature",
	"PASS":"Authentication password",
	"PASV":"Enter passive mode",
	"PBSZ":"Protection Buffer Size",
	"PORT":"Specifies the port to which the server should connect",
	"PROT":"Data Channel Protection Level",
	"PWD":"Print working directory Returns the current directory of the host",
	"QUIT":"Disconnect",
	"REIN":"Re initializes the connection",
	"REST":"Restart transfer from the specified point",
	"RETR":"Transfer a copy of the file",
	"RMD":"Remove a directory",
	"RNFR":"Rename from",
	"RNTO":"Rename to",
	"SENT":"File was sent (downloaded).",
	"SITE":"Sends site specific commands to remote server",
	"SIZE":"Return the size of a file",
	"SMNT":"Mount file structure",
	"SSCN":"Set secured client negotiation",
	"SSH_DISCONNECT":"SFTP (SSH) client connection was closed (reason is provided in the log entry).",
	"STAT":"Returns the status",
	"STOR":"Accept the data and to store the data as a file at the server site",
	"STOU":"Store file uniquely",
	"STRU":"Set file transfer structure",
	"SYST":"Return system type",
	"TYPE":"Sets the transfer mode",
	"USER":"Authentication username",
	"WEBSERVICE":"Web Service was invoked.",
	"XCRC":"Compute CRC32 checksum on specified file",
}


def uasParse(uas):
	response = urllib.urlopen("http://www.useragentstring.com/?uas=" + uas + "&getJSON=all")
	data = json.load(response)
	s = ""
	#data["agent_name"] + " Ver. " + data["agent_version"] + " " + data["agent_type"] + " on " + data["os_name"] + " OS" + 
	if data["agent_name"] != "unknown":
		s = s + data["agent_name"]
	if data["agent_version"] != "" and data["agent_version"] != "--":
		s = s + " Ver. " + data["agent_version"]
	if data["agent_type"] != "unknown":
		s = s + " " + data["agent_type"]
	if data["os_name"] != "unknown":
		s = s + " on " + data["os_name"] + " OS"

	if s == "":
		s = "an unrecognized method: " + uas
	return s

def getDTIdx(date, time):
	#format: 04-18-2007, 04:14:48
	i = 0
	tP = time.split(":")
	dP = date.split("-")
	return (int(tP[2]) + (int(tP[1]) * pow(10, 2)) + (int(tP[0]) * pow(10, 4)) + 
		(int(dP[1]) * pow(10, 6)) + (int(dP[0]) * pow(10, 8)) + (int(dP[2]) * pow(10, 10)))

log_dir = "Logs/"
anl_dir = "AnalyzedLogs/"
analyzed = open(anl_dir + "ANALYZED-LOG-TIMELINE.txt", "w+")
analyzed.write("")
analyzed.close()
analyzed = open(anl_dir + "ANALYZED-LOG-TIMELINE.txt", "a+")
toSort = []
lineCnt = 0


files = os.listdir(log_dir)
if ".DS_Store" in files:
	files.remove(".DS_Store")
print("Analyzing...")

for f in files:
	log = open(log_dir + f, "r")

	lines = log.readlines()
	lineCnt = lineCnt + len(lines)
	print f + ", # of lines = " + str(len(lines)) 

	#state 4 in header, skip: 3, 8
	#A *6* request was made by *2* to the server on port *5* for *7* on *0* at *1*. The request was made using *10-lookup* and was *9-lookup*
	fields = {}
	ftpDate = ""
	for l in lines:
		l = l.strip('\r\n')	#get rid of leading/trailing whitespace
		s = ""
		d = ""
		dtIdx = 0
		if l[0:7] == "#Fields":		#process the fields
			#print l
			pFields = l.split(" ")
			for i in range(1, len(pFields), 1):
				fields[pFields[i]] = i-1
				#print pFields[i]
			#print fields
		elif l[0] == "#":	#process headers
			#analyzed.write(l[1:] + "\n")
			#print l
			if l[0:5] == "#Date" and f[:3] == "FTP":
				ftpDate = l.split(" ")[1]
		elif l[0] == "[":	#process the urlScan logs
			if l[len(l)-1] != "-":	#if this is not a header or trailer message
				p = l.strip("[")
				parsed = p.split("]")
				dtP = parsed[0].split(" - ")
				d = dtP[0].split("-")[2] + "-" + dtP[0].split("-")[0] + "-" + dtP[0].split("-")[1]
				dtIdx = getDTIdx(d, dtP[1])
				s = l
				#print l
				#analyzed.write(l + "\n")
		else:		#process main data from Web and FTP logs
			parsed = l.split(" ")
			if f[:3] != "FTP":	#for a Web log
				d = parsed[fields["date"]]
				dtIdx = getDTIdx(d, parsed[fields["time"]])
			else:	#for a FTP log
				d = ftpDate
				dtIdx = getDTIdx(ftpDate, parsed[fields["time"]])
			
			if "cs-method" in fields:
				if f[:3] == "FTP":
					mthd = parsed[fields["cs-method"]].split("]")[1].upper()
					s = s + "A " + ftp_method[mthd] + " command "
				else:
					s = s + "A " + parsed[fields["cs-method"]] + " request "
			if "c-ip" in fields:
				s = s + "was made by " + parsed[fields["c-ip"]] + " to the server "
			if "s-port" in fields:
				s = s + "on port " + parsed[fields["s-port"]] + " "
			if "cs-uri-stem" in fields:
				s = s + "for " + "'" + parsed[fields["cs-uri-stem"]] + "' "
			if "date" in fields:
				s = s + "on " + parsed[fields["date"]] + " "
			if "time" in fields:
				s = s + "at " + parsed[fields["time"]] + ". "
			if "cs(User-Agent)" in fields:
				s = s + "The request was made using " + uasParse(parsed[fields["cs(User-Agent)"]]) + " "
			if "sc-status" in fields:
				if f[:3] == "FTP":
					if parsed[fields["sc-status"]] in ["257", "550", "553", "10066"]:
						s = s + "'" + parsed[fields["cs-uri-stem"]] + "' " + ftp_code[parsed[fields["sc-status"]]]
					else:
						s = s + ftp_code[parsed[fields["sc-status"]]]
				else:
					s = s + http_codetype[parsed[fields["sc-status"]][0]] + " (" + http_code[parsed[fields["sc-status"]]] + ")"
			if s == "":
				s = "unknown log entry"
		
		#print (s)
		if s != "":
			toSort.append([dtIdx, d, s])
			#analyzed.write(s)	
	log.close()

toSort.sort()
curDay = ""
for l in toSort:
	if l[1] != curDay:
		s = ("\n--------------------------------------------------------------------------------------------------------------------\n" + 
			"--------------------------------------------------------------------------------------------------------------------\n" +
			"--------------------------------------------- New Day: " + l[1] + " -----------------------------------------------\n" +
			"--------------------------------------------------------------------------------------------------------------------\n" +
			"--------------------------------------------------------------------------------------------------------------------\n")
		print s
		analyzed.write(s)
	print l[2]
	analyzed.write(l[2] + "\n")
	curDay = l[1]

analyzed.close()
print "total line count = " + str(lineCnt)
print("Finished.")


'''
print "-------------- Experiment ---------------"
rand = [[4, "jsdv", "baof"], [2, "njnllmx", "ioobsicb"], [9, "jjjb", "kjnlsn"], [6, "jknb", "kjnu"], [3, "ppoj", "ytvkjj"]]
print "unsorted:"
print rand
print "sorted:"
rand.sort()
print rand
'''

'''
{
	"agent_type":"Browser",
	"agent_name":"Internet Explorer",
	"agent_version":"7.0",
	"os_type":"Windows",
	"os_name":"Windows Vista",
	"os_versionName":"",
	"os_versionNumber":"",
	"os_producer":"",
	"os_producerURL":"",
	"linux_distibution":"Null",
	"agent_language":"",
	"agent_languageTag":""
}
'''








