package main

import (
    "fmt"
    "time"
)

func main() {
    const id = "6130116165"
    i := 1
    for {
        fmt.Printf("[%s] - %d\n", id, i)
        i += 1
        time.Sleep(time.Duration(1) * time.Second)
    }
}