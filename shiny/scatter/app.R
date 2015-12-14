
library(shiny)
library(DBI)
library(RMySQL)
library(ggplot2)

drv = dbDriver("MySQL")
db = dbConnect(drv, user="metamusic", password="m00zikz!", dbname="metamusic", host="localhost")

fields <- list("songYear", "peakPosition", "billboardYear", 
               "artistHotttness", "songHotttness", "tempo", 
               "duration", "loudness", "timeSignature")

ui <- fluidPage(
  selectInput("xVar", "X Variable", fields, selected="peakPosition"),
  selectInput("yVar", "Y Variable", fields, selected="songHotttness"),
#  textOutput("query"),
  textOutput("label"),
  plotOutput("plot")
)

server <- function(input, output) {
  query = reactive({
    paste("SELECT ", input$xVar, ", ", input$yVar, " FROM song WHERE ", input$xVar, 
          " IS NOT NULL AND ", input$yVar, " IS NOT NULL;", sep="")
  })
  
  data = reactive({
    rs <- dbSendQuery(db, query())
    fetch(rs, n=-1)
    })
  
  output$query <- renderText({query()})
  
  output$label <- renderText({paste(input$xVar, "vs", input$yVar)})
  
   output$plot <- renderPlot({
     ggplot(data=data(), aes_string(x=input$xVar, y=input$yVar)) +
       geom_point() +
       geom_smooth(method=lm)
   })
}

shinyApp(ui = ui, server = server)
