
library(shiny)

ui <- fluidPage(
   "Hello,world!",
   sliderInput(inputId="num", 
               label="Choose a number",
               value=25, min=1, max=100),
   textOutput("val")
)

server <- function(input, output) {
  output$val = renderText({
    text <- paste("Your number is: ", input$num)
    })
}

shinyApp(ui = ui, server = server)
