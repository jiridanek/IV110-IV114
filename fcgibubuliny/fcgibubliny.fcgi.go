package main

import (
	"encoding/json"
	"io"
	"log"
//	"net"
	"net/http"
	"net/http/fcgi"
	"os"
)

import (
	"./view"
)

type Gene struct {
	ID string
	Regulates []string
	RegulatedBy []string
}

func main () {
	log.SetPrefix("gpopup ")
	log.Println("STARTED")
	
	genes := make(map[string]Gene)
	
	file, err := os.Open("genes.json")
	if err != nil {
		log.Fatal(err)
	}
	decoder := json.NewDecoder(file)
	
	for {
		var g Gene
		if err := decoder.Decode(&g); err == io.EOF {
			break
		} else if err != nil {
			log.Fatal(err)
		}
		genes[g.ID] = g
	}
	
	//listener := net.ListenUnix("unix", {Name "/dev/stdin"Net  string})
	
	err = fcgi.Serve(nil, http.HandlerFunc ( func (w http.ResponseWriter, r *http.Request) {
		log.Println("Got request")
		r.ParseForm()
		pgene := r.Form.Get("gene")
		log.Println(pgene)
		
		gene,found := genes[pgene]
		if !found {
			view.ErrorTmpl.Execute(w, pgene)
			return
		}
		view.ResultsTmpl.Execute(w, gene)
	}))
	if err != nil {
		log.Fatal(err)
	}
	log.Println("EXITED")
}

 
