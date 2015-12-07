
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
   plotOutput("plot")
)

server <- function(input, output) {
	output$plot <- renderPlot(
		query <- paste("SELECT songKey FROM song WHERE artist = '", input$artist, "'")
		rs <- dbSendQuery(db, query)
		df <- fetch(rs, n=-1)
		ggplot(data=df, aes(songKey)) + geom_histogram(aes(y=..count..))
		)
}

shinyApp(ui = ui, server = server)
