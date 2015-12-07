
library(shiny)
library(DBI)
library(RMySQL)
library(ggplot2)

drv = dbDriver("MySQL")
db = dbConnect(drv, user="metamusic", password="m00zikz!", dbname="metamusic", host="ec2-52-90-191-184.compute-1.amazonaws.com")



ui <- fluidPage(
   textInput(inputId = "artist",
   			label="Artist Name:",
   			value="Vanilla Ice"),
   plotOutput("keys"),
   plotOutput("danceability")
)

server <- function(input, output) {
  data = reactive({
    query <- paste("SELECT songKey, danceability, tempo, duration, loudness, timeSignature FROM song WHERE artist = '", input$artist, "'", sep="")
    rs <- dbSendQuery(db, query)
    fetch(rs, n=-1)
    })

  output$keys <- renderPlot({
    if(nrow(data()) == 0) return()
		
    p <- ggplot(data=data(), aes(songKey), environment=environment()) +
      geom_histogram(aes(y=..count..)) +
      ggtitle("Distribution of song keys")
		print(p)
    })

  output$danceability <- renderPlot({
    if(nrow(data()) == 0) return()
    
    p <- ggplot(data=data(), aes(danceability), environment=environment()) +
      geom_histogram(aes(y=..count..)) +
      ggtitle("Distribution of song danceability")
    print(p)
    })
}

shinyApp(ui = ui, server = server)
