## Day 3 Install Instructions

## Install Docker  
  
1. Install `Docker Desktop`. Use one of the links below to download the proper Docker application depending on your operating system. Create a DockerHub account if asked.  
* For macOS, follow this [link](https://docs.docker.com/docker-for-mac/install/).  
* For Linux, follow this [link](https://docs.docker.com/install/linux/docker-ce/ubuntu/).  
* For Windows 10 64-bit (Pro, Enterprise, or Education), follow this [link](https://docs.docker.com/docker-for-windows/install/).  
* For Windows 10 64-bit Home:
	1. Excecute the files "first.bat" and "second.bat" in order, as administrator.
	2. Restart your computer.
	3. Excecute the following commands in terminal, as administrator.
	
			REG ADD "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /f /v EditionID /t REG_SZ /d "Professional"
			REG ADD "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /f /v ProductName /t REG_SZ /d "Windows 10 Pro"
	4. Follow this [link](https://docs.docker.com/docker-for-windows/install/) to install Docker.
	5.	Restart your computer, do not log out.
	6.	Excecute the following commands in terminal, as administrator.
	
			REG ADD "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /v EditionID /t REG_SZ /d "Core"
			REG ADD "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /v ProductName /t REG_SZ /d "Windows 10 Home"
  
Open a Terminal window and type  `docker run hello-world`  to make sure Docker is installed  properly . 
	It should appear the following message:
	
	`` Hello from Docker!``  
	``This message shows that your installation appears to be working correctly.``
	
Finally, in the Terminal window excecute ``docker pull tensorflow/tensorflow:2.1.0-py3-jupyter``.

## Install Anaconda  
  
Follow the instructions for your operating system.  
* For macOS, follow this [link](https://docs.anaconda.com/anaconda/install/mac-os/).  
* For Windows, follow this [link](https://docs.anaconda.com/anaconda/install/windows/).  
* For Linux, follow this [link](https://docs.anaconda.com/anaconda/install/linux/).  
  
## Install Sublime (optional)
Follow the [instructions](https://www.sublimetext.com/3) for your operating system.  
If you already have a prefered text editor, skip this step.  
  
  
## Clone the github repository  
  
Clone or download [this repository](https://github.com/Harvard-IACS/2021-ComputeFest/).
