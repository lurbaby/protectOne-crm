# Layer 1
FROM ubuntu

# Layer 2
RUN echo "start"



# Layer 3
RUN apt-get update && \
    apt-get install -y python3  && \
    apt-get install -y python3-pip

# Layer 4
RUN apt-get install -y git

# Layer 5
RUN git clone https://github.com/lurbaby/schedule_bot.git

