set terminal png
set output 'plot.png'
set title "Bot performance"
set xlabel "Days"
set ylabel "Hive"
set key at screen 0.42, 0.87
#set grid

f1(x) = a1*x + b1
f2(x) = a2*x + b2

fit [0:18] f1(x) 'data.txt' using ($0):1 via a1, b1
fit [18:59] f2(x) 'data.txt' using ($0):1 via a2, b2

highlight_x = 18
highlight_y = 151  # y-Wert aus der ersten Fit-Funktion

set style arrow 1 head filled size screen 0.03,15,25 ls 1
set arrow from highlight_x, highlight_y-30 to highlight_x, highlight_y arrowstyle 1 lt rgb "black" lw 1
set label 'Publication on Github' at screen 0.34, 0.4

plot 'data.txt' using 0:1 with linespoints title 'Hive in Account' lt rgb "black", \
     [0:23] f1(x) title 'Start' lt rgb "red" lw 2, \
     [18:59] f2(x) title 'After publication' lt rgb "blue" lw 2