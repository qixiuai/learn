#install.packages("dplyr")


a <- c(1,2,3,4,5,6,7,8,9,10)
diff <- rnorm(10,0.3,0.1)
b <- a + diff

t.test(b,a,paired = TRUE)
