RUN git clone https://github.com/beastzx18/Tron.git /root/userbot

WORKDIR /root/userbot

RUN pip3 install --no-cache-dir requirements.txt

ENV PATH="/home/userbot/bin:$PATH"

CMD ["python3","-m","tronx"]
