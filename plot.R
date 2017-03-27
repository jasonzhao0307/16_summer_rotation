
library(ggplot2)
library(Rmisc)


# here we used sd for error bar. We can also use se.


# it seems that t=8 & dilution = 1:5 has large bias
# Raw data F8 is an error
# delete that data point and plot again

raw = read.csv("output_od600.txt", header = TRUE, sep = "\t")
# to change the order of legend
raw$dilution <- factor(raw$dilution, levels = c("1:1(before)", "1:1", "1:2", "1:5", "1:10", "1:20"))
raw_summary <- summarySE(raw, measurevar="od600", groupvars=c("time","dilution"))

ggplot(raw_summary, aes(x=time, y=od600, colour=dilution)) + 
  geom_errorbar(aes(ymin=od600-sd, ymax=od600+sd), width=.1) +
  geom_line() + ggtitle("OD600 timeseries for E.coli") + 
  geom_point() + scale_x_continuous(breaks=seq(1,9,1), labels = seq(1,9,1)) + xlab("time(h)")
ggsave("OD600.pdf", width = 10, height = 7)


# spec1
# my idea ONE is to plot 9 figures, each hour with 6 curves(5 dilution + 1:1 before)

raw_spec <- read.csv("output_spec.txt", header = TRUE, sep = "\t")
raw_spec <- raw_spec[raw_spec$obsorb != "OVRFLW",]
raw_spec$obsorb <- (as.numeric(raw_spec$obsorb) / 1000)

raw_spec$dilution <- factor(raw_spec$dilution, levels = c("1:1(before)", "1:1", "1:2", "1:5", "1:10", "1:20"))

for (i in seq(1,9,1)) {
   data <- raw_spec[raw_spec$time == i,]
   data_summary <- summarySE(data, measurevar="obsorb", groupvars=c("od","dilution"))
   ggplot(data_summary, aes(x=od, y=obsorb, colour=dilution)) + 
     geom_errorbar(aes(ymin=obsorb-sd, ymax=obsorb+sd), width=.1) +
     geom_line() + ggtitle(paste("Spectrum for E.coli, Time:", i, "hour", sep = " ")) +
     geom_point()  + scale_x_continuous(breaks=seq(220,900,40), labels = seq(220,900,40)) + xlab("OD(nm)")
   name <- paste("time", i, ".pdf", sep = "")
   ggsave(name, width = 10, height = 7)
 
}


###
# spec2
# my idea TWO is to plot 6 figures, each dilution with 9 curves(9 hours)


raw_spec <- read.csv("output_spec.txt", header = TRUE, sep = "\t")
raw_spec <- raw_spec[raw_spec$obsorb != "OVRFLW",]
raw_spec$obsorb <- (as.numeric(raw_spec$obsorb) / 1000)

name_list <- c("1_1_before","1_1", "1_2", "1_5", "1_10", "1_20")
n = 1
raw_spec$time <- as.character(raw_spec$time)
for (i in c("1:1(before)", "1:1", "1:2", "1:5", "1:10", "1:20")) {
  data <- raw_spec[raw_spec$dilution == i,]
  data_summary <- summarySE(data, measurevar="obsorb", groupvars=c("od","time"))
  ggplot(data_summary, aes(x=od, y=obsorb, colour=time)) + 
    geom_errorbar(aes(ymin=obsorb-sd, ymax=obsorb+sd), width=.1) +
    geom_line() + ggtitle(paste("Spectrum for E.coli, Dilution", i)) + labs(fill = "Time (h)") + 
    geom_point()  + scale_x_continuous(breaks=seq(220,900,40), labels = seq(220,900,40)) + xlab("OD(nm)")
  name <- paste("Dilution", name_list[n], ".pdf", sep = "")
  n = n + 1
  ggsave(name,width = 10, height = 7)
}




