#!/bin/sh
mkdir dryer-plots
cd dryer-plots

TERM='set terminal png size 1280,960;'
#TERM='set term svg;'
cat ../dryer-regular.txt | grep "R" | gnuplot -p -e "$TERM set output 'roll-x.png'; set timefmt '%s'; set xdata time; set grid ytics lt 0 lw 1 lc rgb '#bbbbbb'; plot '<cat' using 1:3 title 'Roll(x)'"
cat ../dryer-regular.txt | grep "R" | gnuplot -p -e "$TERM set output 'roll-y.png'; set timefmt '%s'; set xdata time; set grid ytics lt 0 lw 1 lc rgb '#bbbbbb'; plot '<cat' using 1:4 title 'Roll(y)'"
cat ../dryer-regular.txt | grep "R" | gnuplot -p -e "$TERM set output 'roll-z.png'; set timefmt '%s'; set xdata time; set grid ytics lt 0 lw 1 lc rgb '#bbbbbb'; plot '<cat' using 1:5 title 'Roll(z)'"

cat ../dryer-regular.txt | grep "A" | gnuplot -p -e "$TERM set output 'accel-x.png'; set timefmt '%s'; set xdata time; set grid ytics lt 0 lw 1 lc rgb '#bbbbbb'; plot '<cat' using 1:3 title 'Accel(x)'"
cat ../dryer-regular.txt | grep "A" | gnuplot -p -e "$TERM set output 'accel-y.png'; set timefmt '%s'; set xdata time; set grid ytics lt 0 lw 1 lc rgb '#bbbbbb'; plot '<cat' using 1:4 title 'Accel(y)'"
cat ../dryer-regular.txt | grep "A" | gnuplot -p -e "$TERM set output 'accel-z.png'; set timefmt '%s'; set xdata time; set grid ytics lt 0 lw 1 lc rgb '#bbbbbb'; plot '<cat' using 1:5 title 'Accel(z)"

cat ../dryer-regular.txt | grep "G" | gnuplot -p -e "$TERM set output 'gyro-x.png'; set timefmt '%s'; set xdata time; set grid ytics lt 0 lw 1 lc rgb '#bbbbbb'; plot '<cat' using 1:3 title 'Gyro(x)'"
cat ../dryer-regular.txt | grep "G" | gnuplot -p -e "$TERM set output 'gyro-y.png'; set timefmt '%s'; set xdata time; set grid ytics lt 0 lw 1 lc rgb '#bbbbbb'; plot '<cat' using 1:4 title 'Gyro(y)'"
cat ../dryer-regular.txt | grep "G" | gnuplot -p -e "$TERM set output 'gyro-z.png'; set timefmt '%s'; set xdata time; set grid ytics lt 0 lw 1 lc rgb '#bbbbbb'; plot '<cat' using 1:5 title 'Gyro(z)'"

cat ../dryer-regular.txt | grep "M" | gnuplot -p -e "$TERM set output 'mag-x.png'; set timefmt '%s'; set xdata time; set grid ytics lt 0 lw 1 lc rgb '#bbbbbb'; plot '<cat' using 1:3 title 'Mag(x)'"
cat ../dryer-regular.txt | grep "M" | gnuplot -p -e "$TERM set output 'mag-y.png'; set timefmt '%s'; set xdata time; set grid ytics lt 0 lw 1 lc rgb '#bbbbbb'; plot '<cat' using 1:4 title 'Mag(y)'"
cat ../dryer-regular.txt | grep "M" | gnuplot -p -e "$TERM set output 'mag-z.png'; set timefmt '%s'; set xdata time; set grid ytics lt 0 lw 1 lc rgb '#bbbbbb'; plot '<cat' using 1:5 title 'Mag(z)'"
