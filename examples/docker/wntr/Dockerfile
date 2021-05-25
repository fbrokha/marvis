FROM openjdk:8u242-jdk

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]

COPY filetransfer/* /filetransfer/
WORKDIR /filetransfer/


