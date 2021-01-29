# Use the official Debian-hosted Python image
FROM python:3.8-slim-buster

ARG DEBIAN_PACKAGES="build-essential"

# Prevent apt from showing prompts
ENV DEBIAN_FRONTEND=noninteractive

# Ensure we have an up to date baseline, install dependencies 
# Create a user so we don't run the app as root
RUN set -ex; \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends $DEBIAN_PACKAGES && \
    apt-get install -y --no-install-recommends software-properties-common apt-transport-https ca-certificates gnupg2 gnupg-agent curl && \
    curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    curl -s https://download.docker.com/linux/debian/gpg | apt-key add - && \
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" && \
    echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | tee -a /etc/apt/sources.list.d/kubernetes.list && \
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - && \
    curl https://baltocdn.com/helm/signing.asc | apt-key add -&& \
    echo "deb https://baltocdn.com/helm/stable/debian/ all main" | tee /etc/apt/sources.list.d/helm-stable-debian.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends git kubectl helm google-cloud-sdk jq docker-ce && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir --upgrade pip && \
    pip install openshift ansible docker && \
    useradd -ms /bin/bash app -d /home/app -u 1000 -p "$(openssl passwd -1 passw0rd)" && \
    usermod -aG docker app && \
    mkdir -p /app && \
    chown app:app /app

# Switch to the new user (need ot run as root for docker build)
#USER app
WORKDIR /app

# Add the rest of the source code. This is done last so we don't invalidate all
# layers when we change a line of code.
ADD --chown=app:app . /app

# Install ansible dependencies
RUN set -ex; \
    ansible-galaxy collection install community.general community.kubernetes

# Entry point
ENTRYPOINT ["/bin/bash","./docker-entrypoint.sh"]
