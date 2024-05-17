ARG BASE_IMAGE
FROM ${BASE_IMAGE}

# Install pip and requirements
COPY . .
RUN pip install --user -r requirements.txt

RUN python build_vectorestore.py

CMD ["python", "app.py"]