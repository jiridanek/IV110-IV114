package main

import (
	"encoding/json"
	"io"
	"log"
//	"net"
	"net/http"
	"net/http/fcgi"
	"os"
	"strings"
)

import (
	"./view"
)

type Gene struct {
	ID string
	Start string
	End string
}

type RegulatedGene struct {
	ID string
	Regulates []Gene
	RegulatedBy []Gene
}

func main () {
	log.SetPrefix("gpopup ")
	log.Println("STARTED")
	
	genes := make(map[string]RegulatedGene)
	
	file, err := os.Open("generegulation.json")
	if err != nil {
		log.Fatal(err)
	}
	decoder := json.NewDecoder(file)
	
	for {
		var g RegulatedGene
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
		
		// e.g. Note:ID=G6474
		pgene := r.Form.Get("gene")
		log.Println(pgene)
		index := strings.LastIndex(pgene,"=")
		if index != -1 {
			pgene = pgene[index+1:]
		}
		
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

 
