import bar_chart_race as bcr
import pandas as pd
import numpy as np

df = pd.read_csv("epl-2021-GMTStandardTime.csv")
teams = df['Home Team'].drop_duplicates()
teams = sorted(np.array(teams))
df2 = pd.DataFrame(columns=teams)

for team in teams:
    dfteam = df[df['Home Team'].isin([team]) | df['Away Team'].isin([team])]

    conditions = [
        (dfteam['Home Team'] == team) & (dfteam['Result'].str[0].astype(int) > dfteam['Result'].str[4].astype(int)),
        (dfteam['Away Team'] == team) & (dfteam['Result'].str[0].astype(int) < dfteam['Result'].str[4].astype(int)),
        (dfteam['Home Team'] == team) & (dfteam['Result'].str[0].astype(int) < dfteam['Result'].str[4].astype(int)),
        (dfteam['Away Team'] == team) & (dfteam['Result'].str[0].astype(int) > dfteam['Result'].str[4].astype(int)),
        (dfteam['Result'].str[0].astype(int) == dfteam['Result'].str[4].astype(int))
    ]

    values = [3, 3, 0, 0, 1]
    df2[team] = np.select(conditions, values)

df3 = df2.cumsum(axis=0)

dates = []
for x in range(1,39):
    df2 = df[df['Round Number'] == x]
    dates.append(df2['Date'].iloc[-6])

df3.insert(0,column= 'Date', value=dates)
df3['Date'] = pd.to_datetime(df3['Date'],dayfirst=True).dt.strftime('%d/%m/%y')
df3.to_csv('Cumulative Points.csv', index=False)

df = pd.read_csv('Cumulative Points.csv', index_col='Date')

bcr.bar_chart_race(
    df = df,
    filename="Video.mp4",
    img_label_folder = "bar_images",
    fig_kwargs = {
        'figsize':(40,23),
        'dpi':120,
        'facecolor': '#F8FAFF'
    },
    n_bars=20,
    fixed_max=False,
    steps_per_period=45,
    period_length=1500,
    colors=[
        '#EF0107','#670E36','#e8e4d9','#97d9f6','#005daa','#034694','#1b458f','#274488','#FFCD00','#0053a0',
        '#d00027','#97c1e7','#da020e','#bbbdbf','#00a650','#ed1a3b','#132257','#fbee23','#7c2c3b','#fdb913'
    ],
    title={
        'label':'Premier League 21/22 season',
        'size':52,
        'weight':'bold',
        'pad':40
    },
    period_label={
        'x':0.95,'y':0.15,
        'ha':'right','va':'center',
        'size':72,'weight':'semibold'
    },
    bar_label_font={'size':27},
    tick_label_font={'size':27},
    bar_kwargs={
        'alpha':0.99,
        'lw':0
    },
)


