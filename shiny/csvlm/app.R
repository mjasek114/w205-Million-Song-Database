#install.packages("car")
#library(car)
library(shiny)
df = read.csv("/data/Happiness_edit.csv")

#plot(df$Appreciate, df$Outdoors)
#scatterplot(df$Appreciate~df$Outdoors,jitter=list(x=.7,y=.7)) 
var1="Outdoors"
var2="Love_And_Support"
model = lm(Appreciate~Outdoors+Love_And_Support, df)
model1 = lm(Appreciate~get(var2), df)
#plot(model1, which=1)
#model
#summary(model)
#plot(model, which=1)

ui <- fluidPage(
  checkboxGroupInput(inputId = "vars", 
              label = "Choose the variables for regression", 
              c("Outdoors", "Love_And_Support")),
  sliderInput(inputId = "lmmodel", 
              label = "Choose an lm model", 
              value = 1, min = 1, max = 6, step=1),
#  plotOutput("hist1"),
  textOutput("text1"),
  plotOutput("hist2")
)

server <- function(input, output) {
#  output$hist1 <- renderPlot({
#    scatterplot(df$Appreciate~df$Outdoors,jitter=list(x=.7,y=.7))
#  })
  output$text1 <- renderText({
    "This is text"
  })
  output$hist2 <- renderPlot({
    if (!is.na(input$vars[1])) {
      var1=input$vars[1]
      if (!is.na(input$vars[2])) {
        var2=input$vars[2]
        model = lm(Appreciate~get(var1)+get(var2), df)
      } else {
        model = lm(Appreciate~get(var1), df)
      }
    } else if (!is.na(input$vars[2])) {
      var2=input$vars[2]
      model = lm(Appreciate~get(var2), df)
    }
    plot(model, which=input$lmmodel)
  })
}

shinyApp(ui = ui, server = server)