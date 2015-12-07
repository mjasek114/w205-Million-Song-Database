
library(shiny)
library(DBI)
library(RMySQL)
library(ggplot2)

drv = dbDriver("MySQL")
db = dbConnect(drv, user="metamusic", password="m00zikz!", dbname="metamusic", host="localhost")

ui <- fluidPage(
   "Keys for artist",
   textInput(inputId = "artist",
   			label="Artist Name:",
   			value="Vanilla Ice"),
   textOutput("artist"),
   textOutput("query"),
   plotOutput("plot")
)

server <- function(input, output) {
        output$query <- renderText({
                paste("SELECT songKey FROM song WHERE artist = '", input$artist, "'", sep="")
	})
        output$plot <- renderPlot({
		query <- paste("SELECT songKey FROM song WHERE artist = '", input$artist, "'", sep="")
		rs <- dbSendQuery(db, query)
		df <- fetch(rs, n=-1)
                if(nrow(df) == 0) return()
		p <- ggplot(data=df, aes(songKey), environment=environment()) 
                p <- p + geom_histogram(aes(y=..count..))
		print(p)
                })
        output$artist = renderText({input$artist})
}

shinyApp(ui = ui, server = server)
