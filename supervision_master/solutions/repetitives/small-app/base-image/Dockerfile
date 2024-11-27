FROM ubuntu:18.04

# install c compiler and other tools
RUN apt-get update \ 
	&& apt-get install build-essential -y \ 
	&& apt-get install make \ 
	&& apt-get install nano -y



### --------------------------------------------------------------
# FROM alpine as build-env
# RUN apk add --no-cache build-base
# RUN apk add --no-cache clang
# WORKDIR /app

# # COPY . . # hw
# # Compile the binaries
# # RUN gcc -o hello helloworld.c # hw

# # COPY ./fib .
# # RUN make

# COPY ./bubble .
# RUN gcc -o bubble bubble.c

# FROM alpine
# # COPY --from=build-env /app/hello /app/hello # hw
# # COPY --from=build-env /app/fib /app/fib
# COPY --from=build-env /app/bubble /app/bubble
# WORKDIR /app
# # CMD ["/app/hello"]