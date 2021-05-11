FROM python:3.7-slim as builder
COPY requirements.txt .

# install dependencies
RUN pip install --user -r requirements.txt

FROM python:3.7-slim
WORKDIR /fast_ner

# copy required dependencies and source files
COPY --from=builder /root/.local /root/.local
COPY . .

# update PATH env variable
ENV PATH=/root/.local:$PATH

# expose port to query
EXPOSE 5000

# startup script
CMD python server.py