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

On the device whose IP address you wish to keep track of make an http get request 
(or manually using your web browser) to:

    https://myip.ohanacode-dev.com/set/[device_id]

On your computer, from which you wish to find devices IP address, 
open a web browser and go to:

    https://myip.ohanacode-dev.com/get/[device_id]

This will return just your devices IP address. If your device provides a web server 
and you need a page to bookmark, you can use:

    https://myip.ohanacode-dev.com/redirect/[device_id]

This will provide a page redirecting to your devices IP address.

# Running the service

This is a Python Flask based application, so install Flask and run the py file 
using Python3. Take a look at the end of the python file for hint on selecting 
parameters for local or external server hosting. 
