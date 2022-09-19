import pandas as pd

df = pd.DataFrame({
    "name":         ["alan","beth","charlie","david", "edward"],
    "p1" :         [34,    12,     43,      32,      77],
    "p2": [18,     70,      22,       51,      36],
    "p3":     [13,     80,      31,       72,      20],
    "pathogenic": [14, 17,   10,   150,    30.0]})

print(df)

def highlight_color(row):

    
 
    highlight = 'background-color: darkorange;'
    default = ''
    print([ highlight if i  > row["pathogenic"] else default for i in row    ])
    return [ highlight if i  > row["pathogenic"] else default for i in row    ]

#df.style.apply(highlight_color, axis=1, subset=["p1", "p2", "p3", "pathogenic"])

df.style.apply(highlight_color, axis=1, subset= df.select_dtypes(include=['int', 'float']).columns )
