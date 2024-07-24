
##############
#  Parameters
##############

chocolate_color="672f0a"
special_chocolate_color="FFD700"
zero_chocolate_color="684fa3"
border_color="000000"

n_cols=3
scale="0.35"


##############
#    Main
##############
size=1

# Print latex code showing the nim_value of current tablet
nim-value() {
    old_IFS="$IFS"
    IFS=","

    # Get nim value
    value=$(head -n1 "$1")

    # Get winning play
    if [ "$value" -ne 0 ]; then
        win_play=$(tail -n1 "$1")
        win_row=$(echo "$win_play" | cut -d',' -f1 )
        win_col=$(echo "$win_play" | cut -d',' -f2 )
    else
        win_row="-1"
        win_col="-1"
    fi;

    # Print latex code
    tablet="${1#db_zero/*}"
    echo "\begin{wrapfigure}{c}{0.7\linewidth}"
    echo "\centering"
    echo "\begin{tikzpicture}[scale=$scale]"

    pos_x_end=0
    curr_col=0
    for col in $tablet; do
        let "curr_col = curr_col + 1"

        pos_x_start="$pos_x_end"
        let "pos_x_end = pos_x_end + size"

        pos_y_end=0
        for row in $(seq -s',' "$col"); do
            pos_y_start="$pos_y_end"
            let "pos_y_end = pos_y_end + size"

            if [ "$row" = "$win_row" ] && [ "$curr_col" = "$win_col" ]; then
                curr_color="special_chocolate_color"
            elif [ "$value" = 0 ]; then
                curr_color="zero_chocolate_color"
            else
                curr_color="chocolate_color"
            fi

            echo "\filldraw [fill=$curr_color,draw=border_color, thick] ($pos_x_start, $pos_y_start) rectangle ($pos_x_end, $pos_y_end);"
        done
    done
    echo "\end{tikzpicture}"
    echo "\caption{\small ${tablet#db_zero/*} = $value}"
    echo "\end{wrapfigure}"
    IFS="$old_IFS"
}

# Generate tex file
{
    echo "\input{tex/preamble.tex}"

    echo "\definecolor{border_color}{HTML}{$border_color}"
    echo "\definecolor{chocolate_color}{HTML}{$chocolate_color}"
    echo "\definecolor{special_chocolate_color}{HTML}{$special_chocolate_color}"
    echo "\definecolor{zero_chocolate_color}{HTML}{$zero_chocolate_color}"

    echo "\begin{multicols}{$n_cols}"

    #nim-value "db/2,2,2"   # Not zero example
    #nim-value "db/2,2,1"   # Zero example
    #for file in db/?,2,1*; do
        #nim-value "$file"
    #done
    for file in db_zero/*; do
        nim-value "$file"
    done

    echo "\end{multicols}"
    echo "\end{document}"

} > tex/main.tex

# Compile it
pdflatex -interaction=nonstopmode -output-directory=tex tex/main.tex &> /dev/null
cp tex/main.pdf some_chocolates_milka.pdf
