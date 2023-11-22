FROM alpine:3.17.3

# Configure Go
ENV GOROOT /usr/lib/go
ENV GOPATH /go
ENV PATH /go/bin:$PATH

RUN apk update &&\
    apk upgrade &&\
    apk add --no-cache build-base ansible python3 py3-pip python3-dev git openssh docker musl-dev go curl jq &&\
    apk add --no-cache terraform --repository=https://dl-cdn.alpinelinux.org/alpine/latest-stable/community &&\
    mkdir -p ${GOPATH}/src ${GOPATH}/bin &&\
    go install github.com/passbolt/go-passbolt-cli@latest

RUN mkdir -p /work
RUN mkdir -p ~/.ssh
WORKDIR /work
