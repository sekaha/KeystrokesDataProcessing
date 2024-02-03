# help making a latex table
matrix = []

for y in range(1, 5):
    matrix = [[]] + matrix
    for x in list(range(-5, 0)) + list(range(1, 6)):
        matrix[0].append(f"$({x},{y})$")
    # matrix[0].append("\multicolumn{1}{|c|}{" + f"${x},{y}$" + "}")

print((r"\\ \hline" + "\n").join([" & ".join(row) for row in matrix]))

"""\begin{table}[h]
\centering
\begin{tabular}{|*{10}{p{10cm}|}} % Adjust the width as needed
\hline
\multicolumn{1}{|c|}{$-5,4$} & \multicolumn{1}{|c|}{$-4,4$} & \multicolumn{1}{|c|}{$-3,4$} & \multicolumn{1}{|c|}{$-2,4$} & \multicolumn{1}{|c|}{$-1,4$} & \multicolumn{1}{|c|}{$1,4$} & \multicolumn{1}{|c|}{$2,4$} & \multicolumn{1}{|c|}{$3,4$} & \multicolumn{1}{|c|}{$4,4$} & \multicolumn{1}{|c|}{$5,4$}\\ \hline
\multicolumn{1}{|c|}{$-5,3$} & \multicolumn{1}{|c|}{$-4,3$} & \multicolumn{1}{|c|}{$-3,3$} & \multicolumn{1}{|c|}{$-2,3$} & \multicolumn{1}{|c|}{$-1,3$} & \multicolumn{1}{|c|}{$1,3$} & \multicolumn{1}{|c|}{$2,3$} & \multicolumn{1}{|c|}{$3,3$} & \multicolumn{1}{|c|}{$4,3$} & \multicolumn{1}{|c|}{$5,3$}\\ \hline
\multicolumn{1}{|c|}{$-5,2$} & \multicolumn{1}{|c|}{$-4,2$} & \multicolumn{1}{|c|}{$-3,2$} & \multicolumn{1}{|c|}{$-2,2$} & \multicolumn{1}{|c|}{$-1,2$} & \multicolumn{1}{|c|}{$1,2$} & \multicolumn{1}{|c|}{$2,2$} & \multicolumn{1}{|c|}{$3,2$} & \multicolumn{1}{|c|}{$4,2$} & \multicolumn{1}{|c|}{$5,2$}\\ \hline
\multicolumn{1}{|c|}{$-5,1$} & \multicolumn{1}{|c|}{$-4,1$} & \multicolumn{1}{|c|}{$-3,1$} & \multicolumn{1}{|c|}{$-2,1$} & \multicolumn{1}{|c|}{$-1,1$} & \multicolumn{1}{|c|}{$1,1$} & \multicolumn{1}{|c|}{$2,1$} & \multicolumn{1}{|c|}{$3,1$} & \multicolumn{1}{|c|}{$4,1$} & \multicolumn{1}{|c|}{$5,1$}\\ \hline
\multicolumn{1}{|c|}{$-5,0$} & \multicolumn{1}{|c|}{$-4,0$} & \multicolumn{1}{|c|}{$-3,0$} & \multicolumn{1}{|c|}{$-2,0$} & \multicolumn{1}{|c|}{$-1,0$} & \multicolumn{1}{|c|}{$1,0$} & \multicolumn{1}{|c|}{$2,0$} & \multicolumn{1}{|c|}{$3,0$} & \multicolumn{1}{|c|}{$4,0$} & \multicolumn{1}{|c|}{$5,0$} \\ \hline
\multicolumn{10}{|c|}{$(0,0)$} \\ \hline
\end{tabular}
\end{table}"""
