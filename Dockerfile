FROM public.ecr.aws/lambda/python:3.9

# Copy function code
COPY functions ${LAMBDA_TASK_ROOT}/functions

# Avoid cache purge by adding requirements first
COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip install --no-cache-dir -r requirements.txt

ARG IEX_TOKEN
ARG DATABASE_HOST
ARG DATABASE_USER
ARG DATABASE_PASSWORD
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION

ENV IEX_TOKEN $IEX_TOKEN
ENV DATABASE_HOST $DATABASE_HOST
ENV DATABASE_USER $DATABASE_USER
ENV DATABASE_PASSWORD $DATABASE_PASSWORD
ENV AWS_ACCESS_KEY_ID $AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY $AWS_SECRET_ACCESS_KEY
ENV AWS_DEFAULT_REGION $AWS_DEFAULT_REGION

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "functions.get_us_symbols_news.handler" ]
