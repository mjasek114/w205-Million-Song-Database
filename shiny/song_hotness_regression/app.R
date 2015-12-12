library(DBI)
library(RMySQL)
library(shiny)

drv = dbDriver("MySQL")
db = dbConnect(drv, user="metamusic", password="m00zikz!", dbname="metamusic", host="localhost")
dbListTables(db, metamusic)
dbListFields(db, "song")
query = paste("SELECT loudness, artistHotttness, timeSignature, duration, tempo, songKey, songHotttness, peakPosition, songYear, billboardYear, mode FROM song")
rs = dbSendQuery(db, query)
df = fetch(rs, n=-1)
df$songKey = as.factor(df$songKey)
df$songKey = factor(df$songKey,levels(df$songKey)[c(2,1,4,3,5,6,7,9,8,10,11,12)])

ui <- fluidPage(
  checkboxGroupInput(inputId = "vars", 
              label = "Choose the Variables for Regression for Song Hotttness", 
              c("artistHotttness", "duration", "tempo", "songKey", "loudness", "timeSignature", "peakPosition", "songYear", "billboardYear", "mode"), selected = "artistHotttness"),
  verbatimTextOutput("text1")
)

server <- function(input, output) {
  output$text1 <- renderPrint({
    if (is.null(input$vars)){
      return("Please select some variables")
    } else {
      terms = ""
      for (var in input$vars) {
        if (terms!="") {
          terms=paste(c(terms, var), collapse="+")
        } else {
          terms=var
        }
      }
      model = lm(as.formula(paste("songHotttness ~", terms)), data=df)    
      summary(model)
    }
  })
}

shinyApp(ui = ui, server = server)