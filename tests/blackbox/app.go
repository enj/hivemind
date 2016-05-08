package main

import (
	"errors"
	"flag"
	"io/ioutil"
	"time"
)

func validateFlags(flags ...*string) error {
	for _, flag := range flags {
		if flag == nil || *flag == "" {
			return errors.New("Invalid arguments")
		}
	}
	return nil
}

func main() {
	in := flag.String("in", "", "the input file")
	out := flag.String("out", "", "the output file")
	cat := flag.String("cat", "", "the string to cat")
	sleep := flag.Int("sleep", 0, "duration to sleep in ms")
	flag.Parse()

	// make sure all required flags given
	if err := validateFlags(out, cat); err != nil {
		panic(err)
	}

	var b []byte
	if in != nil && *in != "" {
		// read in the whole (small) input file
		tmp, err := ioutil.ReadFile(*in)
		if err != nil {
			panic(err)
		}
		b = tmp
	}

	// Add the cat to the input data
	full := append(b, []byte(*cat)...)

	// wait to simulate work
	time.Sleep(time.Duration(*sleep) * time.Millisecond)

	// write out all data to the output
	if err := ioutil.WriteFile(*out, full, 0644); err != nil {
		panic(err)
	}
}
