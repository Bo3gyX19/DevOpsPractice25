package main

import "net/http"

func main() { http.ListenAndServe(":8080", http.FileServer(http.Dir("html"))) }

// This code creates a simple HTTP server that serves html files from the "html" directory on port 8080.
// To run this code, create a directory named "html" in the same location as this file and place some files in it.
// Then, run the code and open your web browser to http://localhost:8080 to see the files being served.
// The http.ListenAndServe function takes two arguments: the address to listen on (":8080" in this case) and the handler (http.FileServer(http.Dir("html"))).
// The http.FileServer function creates a handler that serves HTTP requests with the contents of the file system rooted at the directory specified by http.Dir("html").
// The http.Dir function converts the string "html" into a type that implements the http.FileSystem interface.
// The http.ListenAndServe function starts the server and listens for incoming requests on the specified address.
// The server will continue to run until it is stopped manually or an error occurs.
// To stop the server, you can use Ctrl+C in the terminal where the server is running.
