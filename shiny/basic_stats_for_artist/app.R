
library(shiny)
library(DBI)
library(RMySQL)
library(ggplot2)

drv = dbDriver("MySQL")
db = dbConnect(drv, user="metamusic", password="m00zikz!", dbname="metamusic", host="ec2-52-91-187-124.compute-1.amazonaws.com")



ui <- fluidPage(
   textInput(inputId = "artist",
   			label="Artist Name:",
   			value="Vanilla Ice"),
   plotOutput("keys"),
#   plotOutput("danceability"),
   plotOutput("tempo"),
   plotOutput("duration"),
   plotOutput("loudness"),
   plotOutput("timeSignature"),
   tableOutput("table")
)

server <- function(input, output) {
  data = reactive({
    query <- paste("SELECT title, songKey, danceability, tempo, duration, loudness, timeSignature FROM song WHERE artist = '", input$artist, "'", sep="")
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

  output$tempo <- renderPlot({
    if(nrow(data()) == 0) return()
    
    p <- ggplot(data=data(), aes(tempo), environment=environment()) +
      geom_histogram(aes(y=..count..)) +
      ggtitle("Distribution of song tempo")
    print(p)
  })
  
  output$duration <- renderPlot({
    if(nrow(data()) == 0) return()
    
    p <- ggplot(data=data(), aes(duration), environment=environment()) +
      geom_histogram(aes(y=..count..)) +
      ggtitle("Distribution of song duration")
    print(p)
  })
  
  output$loudness <- renderPlot({
    if(nrow(data()) == 0) return()
    
    p <- ggplot(data=data(), aes(loudness), environment=environment()) +
      geom_histogram(aes(y=..count..)) +
      ggtitle("Distribution of song loudness")
    print(p)
  })
  
  output$timeSignature <- renderPlot({
    if(nrow(data()) == 0) return()
    
    p <- ggplot(data=data(), aes(timeSignature), environment=environment()) +
      geom_histogram(aes(y=..count..)) +
      ggtitle("Distribution of song time signature")
    print(p)
  })
  
  output$table <- renderTable({data()})
}

shinyApp(ui = ui, server = server)
