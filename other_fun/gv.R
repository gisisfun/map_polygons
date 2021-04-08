library(DiagrammeR)
mermaid("
graph LR
    PDF[PDF Files]-->|Extract Text| Certs((Certificates))
    HTML[HTML File]-->|Scrape| Courses_s((Scraped Courses))  
    HTML-->|Scrape| Tracks_s((Scraped Tracks))
    HTML-->|Scrape| Topics((Scraped Topics))
    Courses_s--> |fuzzy| Courses((Courses Certs))
    Certs-->|clean| Courses
    Tracks_s(Scraped Tracks)--> Tracks((Tracks Certs))
    Certs-->|Fix missing letters| Tracks 
    Tracks--> Excel[Excel]
    Courses-->|filter| Excel
    Topics--> Excel
    Tracks-->|reshape| Chart[Chart]
    Courses-->|reshape| Chart
    Tracks-->|TODO| Document[Word or PDF Document] 
    Courses-->|TODO| Document
    Chart-->|TODO| Document 
    Tracks-->|TODO| Dataset[Data set for BI Tool]
    Courses-->|TODO| Dataset
    ")
