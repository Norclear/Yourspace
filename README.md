Hello this is the source code for the website https://yourspace.space

I made this as a pet project during my spare time using angular 14, typescript, html and css with certain ui modules taken from ng-bootstrap. 
Thus this project does not represent any of my personal ui skills (i suck at UI and UX) but rather full stack development i.e. Front-end, back-end and networking.

The backend is created in python using the fast-API library. The yourspace API can be directly accessed without the UI via http://api.yourspace.space .

I am running this on a Rockpi 5b and a linux ubuntu 20.04 Server LTS. This means I configured all networking on my own, i.e. Firewall rules, webserver (nginx btw),
port forwarding, domain name configuration (and the api sub domain aswell), the SSL certificate (thank you cert bot), server administration and other networking configurations and concepts.

This application uses a SQL database, Specifically MySQL and some some-what advanced SQL queries aswell as efficient database querying using connection pooling.

The api could defintely be more efficient through the use of data caching but will not be implemented into this app.

Thus the full-stack for this website looks like the following;

Angular 14 -> Nginx -> Python and FastAPI -> MySQL

I do apologies in advanced to anybody trying to read this code if it is difficult becuase at this time there its very minimal documentation cuz I had no idea what I was doing when I made this.

This website is hosted from my house, thus this means it uses my home network. Thus it is far from reliable and may be down at anytime, the backend does not automatically start because I forgot to configure that.
If it is not currently up at the time of reading please email me at yesqwertynoqwerty@gmail.com or for any other enquiries.

fyi, front end is found in the /src folder and backend in the /backend folder
