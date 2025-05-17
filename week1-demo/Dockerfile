FROM golang as builder
WORKDIR /src
COPY src .
COPY go.mod .
RUN CGO_ENABLED=0 go build -o app

FROM scratch
ADD ./html /html
COPY --from=builder /src/app .
EXPOSE 8080
ENTRYPOINT ["/app"]