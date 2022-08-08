FROM python:3.6
COPY ./requirements.txt /requirements.txt
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /requirements.txt
COPY . /bioinformatics-analysis/
WORKDIR /bioinformatics-analysis
RUN rm -rf /requirements.txt; \
    sed -i 's/\r//' ./start.sh; \
    chmod +x ./start.sh
CMD ["sh", "./start.sh"]
