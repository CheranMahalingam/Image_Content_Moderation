FROM public.ecr.aws/lambda/python:3.8

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambda_handler"]
