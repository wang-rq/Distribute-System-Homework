FROM golang
MAINTAINER wangruoqi "wangrq29@mail2.sysu.edu.cn"
WORKDIR /hw2
ADD . /hw2
RUN go build hello-world.go
ENTRYPOINT ["./hello-world"]