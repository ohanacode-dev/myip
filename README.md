# myip
Service to keep track of devices IP address.

## Purpose of this service
Sometimes I build various devices that I need to access remotely. 
For this I need to know the IP address of a device. 
This is a service to provide a simple way to keep track of devices IP address 
and it is free for anyone to use. It is like a Dynamic DNS service, 
but you can host this anywhere, even within your local network. 
Keep in mind that if you do host this service on your own network, 
the IP address reported will not be external, but a local one. 
To get an external address this must be hosted on an external server.

I do not employ a domain name registrar, nor do I provide a hosting service, 
so I can not provide you with an domain that your devices would use directly, 
but just a text based record of an updated IP address.

## How it works
To keep things simple, there is no login, no registration. 
Every device using this service must have it's own unique id. 
We will refer to this as [device_id]. You can generate the id yourself. 
Choose any set of characters. I am using a private ssh key, 
but you can use anything else you are sure is unique. 
Lets refer to the address of the computer running this service as [server_url]. 

On the device whose IP address you wish to keep track of make an http get request 
(or manually using your web browser) to:

    [server_url]/set/[device_id]

On your computer, from which you wish to find devices IP address, 
open a web browser and go to:

    [server_url]/get/[device_id]

This will return just your devices IP address. If your device provides a web server 
and you need a page to bookmark, you can use:

    [server_url]/redirect/[device_id]

This will provide a page redirecting to your devices IP address.

##Administration
Here are a few more things you need to know.
This solution uses an SQLITE database to record all the IP addresses, device ID's and timestamps.
There is also a TITLE field. If you look at the start of the python file, you will find a variable 
called ADMIN_ID. Change the value to anything you like. Lets refer to it as [admin_pass].
If you now go to:

    [server_url]/get/[admin_pass]
    
You will get a list of all recorded IP addresses with device ID, timestamp and title. 
At this point the title is not set. To set the title of each device, you can go to:

    [server_url]/title/[device_id]/[some_html_safe_device_title]
    
This will not alter the IP address recorded for the device ID, only the title, so it can be 
requested from any other IP address.

## Running the service
This is a Python Flask based application, so install Flask and run:
 
    Python3 application.py  

Take a look at the start of the file for basic parameters. 

## Licence
You are free to do with this code as you like, but I would appreciate it if you mention me somewhere.

