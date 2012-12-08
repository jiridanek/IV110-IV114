package view

import (
	"text/template"
)

var address = `<a href="?q=NC_000913:{{.Start}}..{{.End}}&enable=DNA" target=_self>{{.ID}}</a>`
var ResultsTmpl = template.Must(template.New("results").Parse(
`<h1>Gene {{.ID}}</h1>
<h3>regulates</h3>
<p>{{range .Regulates}}` + address + `, {{else}}no records{{end}}</p>
<h3>and is regulated by</h3>
<p>{{range .RegulatedBy}}` + address + `, {{else}}no records{{end}}</p>`))
