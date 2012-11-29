package view

import (
	"text/template"
)

var ErrorTmpl = template.Must(template.New("error").Parse(`
<h1>Gene {{.}} is not in the database</h1>`))