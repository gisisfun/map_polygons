library(DiagrammeR)
mermaid("
// DataCamp_Charts
digraph {
	node [rankdir=LR]
	rankdir=LR
	node [shape=ellipse]
	PDF [label="PDF Files" shape=box]
	Certs [label=Certificates shape=ellipse]
	HTML [label="HTML File" shape=box]
	Courses_s [label="Scraped
Courses" shape=ellipse]
	Topics [label="Scraped
Topics" shape=ellipse]
	Tracks_s [label="Scraped
Tracks" shape=ellipse]
	Tracks [label="Tracks
Certs" shape=ellipse]
	Courses [label="Courses
Certs" shape=ellipse]
	Excel [label=Excel shape=box]
	Chart [label=Chart shape=box]
	Document [label="Word or
PDF Document" shape=box]
	Dataset [label="Data set
for BI Tool" shape=box]
	PDF -> Certs [label="Extract Text"]
	HTML -> Courses_s [label=Scrape]
	HTML -> Tracks_s [label=Scrape]
	HTML -> Topics [label=Scrape]
	Courses_s -> Courses [label=fuzzy]
	Certs -> Courses [label=clean]
	Tracks_s -> Tracks [label=""]
	Certs -> Tracks [label="Fix missing letters"]
	Tracks -> Excel [label=""]
	Courses -> Excel [label=filter]
	Topics -> Excel [label=""]
	Tracks -> Chart [label=reshape]
	Courses -> Chart [label=reshape]
	Tracks -> Document [label=TODO]
	Courses -> Document [label=TODO]
	Chart -> Document [label=TODO]
	Tracks -> Dataset [label=TODO]
	Courses -> Dataset [label=TODO]
")
