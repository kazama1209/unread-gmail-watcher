FROM amazonlinux:2

ARG PYTHON_VERSION=3.7.0

RUN yum update -y && yum install -y tar gzip make gcc openssl-devel bzip2-devel libffi-devel \
  && curl https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz | tar xz \
  && cd Python-${PYTHON_VERSION} && ./configure && make && make install \
  && cd - && rm -rf Python-${PYTHON_VERSION}

ADD entrypoint.sh /

RUN yum install -y zip \
  && mkdir /python \
  && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
