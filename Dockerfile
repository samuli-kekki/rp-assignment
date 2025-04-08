
# This Flux-dev handler should work with this base image on A40.
FROM runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04

ARG HF_BUILD_TOKEN
ENV HF_BUILD_TOKEN=${HF_BUILD_TOKEN}

WORKDIR /app

# This first version of the Dockerfile copies all files
# and does no cleanup afterwards.
COPY . .

RUN echo "Installing requirements"
RUN pip install -r requirements.txt

RUN echo "Preloading model"
RUN python model_loader.py

RUN echo "Done with setup"

CMD ["python", "-u", "handler.py"]
