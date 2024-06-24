require(dplyr)
require(readr)

col <- cols(
  uid = col_double(),
  posX = col_double(),
  posY = col_double(),
  posZ = col_double()
)

df <- read_tsv("../results/positionResults_0.csv", col_types = col)

summary(df)
plt.lwd = c(2)
plt.col = (palette(gray(seq(0,0.9,len = length(distinct(df, uid)$uid))))) #grey scale

pdf("plotPosition.pdf") 
	par(mar=c(3,4.0,1,1.0))
	plot.new()
	plot.window(xlim=c(0,3000), ylim=c(0,3000), xaxs="i", yaxs="i")
	#plot.window(xlim=c(10,12), ylim=c(10,12), xaxs="i", yaxs="i")
	i <- 1
	for (n in distinct(df, uid)$uid) {
	  dfTmp      <- filter(df, uid == n) 
	  lines(dfTmp$posX,   dfTmp$posY,   lwd = plt.lwd[i], col=plt.col[i])
	  i <- i + 1
	}
	  
	
	axis(1)
	axis(2, las=1)
	title(ylab="Position Y-Axis (in m)", line=3)
	title(xlab="Position X-Axis (in m)", line=2)
	legend("bottomleft", legend = unlist(distinct(df, uid)),  lwd=plt.lwd, col=plt.col, bty="n", y.intersp=0.8)

dev.off()
