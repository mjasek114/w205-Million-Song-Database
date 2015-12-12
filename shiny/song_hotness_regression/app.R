library(DBI)
library(RMySQL)
library(shiny)

drv = dbDriver("MySQL")
db = dbConnect(drv, user="metamusic", password="m00zikz!", dbname="metamusic", host="localhost")
dbListTables(db, metamusic)
dbListFields(db, "song")
query = paste("SELECT loudness, artistHotttness, timeSignature, duration, tempo, songKey, songHotttness FROM song")
rs = dbSendQuery(db, query)
df = fetch(rs, n=-1)
df$songKey = as.factor(df$songKey)
df$songKey = factor(df$songKey,levels(df$songKey)[c(2,1,4,3,5,6,7,9,8,10,11,12)])

ui <- fluidPage(
  checkboxGroupInput(inputId = "vars", 
              label = "Choose the Variables for Regression for Song Hotttness", 
              c("artistHotttness", "duration", "tempo", "songKey", "loudness", "timeSignature"), selected = "artistHotttness"),
  verbatimTextOutput("text1")
)

server <- function(input, output) {
  output$text1 <- renderPrint({
    if(is.null(input$vars)) {
      return("Please select some variables")
    }
    terms=""
    if (!is.na(input$vars[1])) {
      var1 = input$vars[1]
      terms=var1
    }
    if (!is.na(input$vars[2])) {
      var2 = input$vars[2]
      if (terms!="") {
        terms=paste(c(terms, var2), collapse="+")
      } else {
        terms=var2
      }
    }
    if (!is.na(input$vars[3])) {
      var3 = input$vars[3]
      if (terms!="") {
        terms=paste(c(terms, var3), collapse="+")
      } else {
        terms=var3
      }
    }
    if (!is.na(input$vars[4])) {
      var4 = input$vars[4]
      if (terms!="") {
        terms=paste(c(terms, var4), collapse="+")
      } else {
        terms=var4
      }
    }
    if (!is.na(input$vars[5])) {
      var5 = input$vars[5]
      if (terms!="") {
        terms=paste(c(terms, var5), collapse="+")
      } else {
        terms=var5
      }
    }
    if (!is.na(input$vars[6])) {
      var6 = input$vars[6]
      if (terms!="") {
        terms=paste(c(terms, var6), collapse="+")
      } else {
        terms=var6
      }
    }
    model = lm(as.formula(paste("songHotttness ~", terms)), data=df, na.action = na.exclude)    
    summary(model)
  })
}

shinyApp(ui = ui, server = server)