# INTENTIONALLY INSECURE - Checkmarx One Containers demo only.
FROM golang:1.13 AS build
COPY . /src
RUN cd /src && go build -o /app
FROM alpine:3.7
COPY --from=build /app /app
RUN apk add --no-cache openssl=1.0.2n-r0 curl
ARG GITHUB_TOKEN=ghp_dockerBuildArgTokenExample1234567890
CMD ["/app"]
