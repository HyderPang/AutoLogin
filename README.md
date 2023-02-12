# AutoLogin
An automatic tiny application with a GUI, that can log into networks requiring authentication by simulating browsers such as Firefox and Chrome when the system is offline. It supports customized XPATHs for adapting to multiple "username&amp;password" based login pages.

## Dependencies
* **Selenium**, an automated web browser interacter for Python :
```
pip install selenium
```
* **requests**, a widely used HTTP library:
```
pip install requests
```

## Run
To run the application, simply type
```
python main.py
```
Then put your username and configure the settings. The setting options:
* **Retry times** & **Listen interval**: Try to check the connect every "Listen interval" seconds. if the connection losts, the program will try to reconnect for "retry times".
* **url**: url of login page.
* **Xpath of ...**: customized xpath of username, password and login button. Use F12 in your page to find and copy the XPATH.
* **Browser**: browser simulated by Selenium. Make sure the releated webdriver.exe files are in system \$PATH.


Then, press the button. The application will continuely check connection and make reconnections.

## Build
A .bat script to build an .exe executable programme is provided. To run it, **pyinstaller** need to installed.
```
pyinstaller -i icon.ico -F -w main.py -n "Auto Login.exe"
```
