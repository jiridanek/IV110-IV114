package view

import (
	"text/template"
)

var ResultsTmpl = template.Must(template.New("results").Parse(
`<h1>Gene {{.ID}}</h1>
<h3>regulates</h3>
<p>{{range .Regulates}}{{.}}, {{else}}no records{{end}}</p>
<h3>and is regulated by</h3>
<p>{{range .RegulatedBy}}{{.}}, {{else}}no records{{end}}</p>`))
