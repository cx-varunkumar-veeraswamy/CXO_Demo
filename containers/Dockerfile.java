# INTENTIONALLY INSECURE - Checkmarx One Containers demo only.
FROM tomcat:8.0.20-jre7
COPY target/app.war /usr/local/tomcat/webapps/
ENV JAVA_OPTS="-Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false"
RUN chmod -R 777 /usr/local/tomcat
EXPOSE 8080 8000 9010
