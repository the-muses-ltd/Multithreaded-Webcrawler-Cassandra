# Multithreaded Webcrawler for Cassandra Database
## Why Multithread?
Due to the sheer number of recourses we need to iterate through on the platforms we explore, we use concurrent processing to significantly reduce the time and computational resources needed to populate our database.

## Want to learn more about multithreading?
There are tons of resources online for this topic, but this gives a good overview for a beginner: https://www.techbeamers.com/python-multithreading-concepts/

## Running this application
1. Make sure you have docker installed on your local machine.
2. Then run the following code in your terminal to start your docker container:

`docker build -f Dockerfile -t multi-webcrawler:latest .`

Finally, you can run the application by executing this code in your terminal and the crawlers will start crawling:

`docker run -p 5001:5000 multi-webcrawler`


![Docker](https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.cleanpng.com%2Fpng-docker-application-software-asp-net-core-microserv-6858151%2F&psig=AOvVaw2uycPlOZJ0U2o5OqG6UdLQ&ust=1603023731873000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCNDZkvPOu-wCFQAAAAAdAAAAABAS)

## Docker Containerized Application
# Why docker?
Docker allows us to calaborate easier by containerizing our application and having a strict set of rules of how your Virtual Machine will build the environment for the application. This reduces time spent on setting up your work environment and reduces the risk of inconsistencies in the way we setup our local machines. Essentially, it unifies the way we all work on a single application.

Learn more about docker here: https://www.docker.com/