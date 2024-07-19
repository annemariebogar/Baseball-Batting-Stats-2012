import psycopg2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import math
plt.style.use('seaborn-v0_8')

#Connect to Postgres server
def connect():
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(dbname="Baseball", user="postgres", password="password") as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (Exception. psycopg2.DatabaseError ) as error:
        print(error)

#Connect to database
def connectDB():
    conn = connect()
    return conn

#Close connection to Postgres database
def closeDB(conn):
    conn.commit()
    conn.close()

#Query Database
def sqlQuery(cur, query):
    cur.execute(query)
    rows = cur.fetchall()
    colnames = [desc.name for desc in cur.description]
    return rows, colnames

#Access and Query database and then close connection
def getTable(query):
    conn = connectDB()
    cur = conn.cursor()
    table, colnames = sqlQuery(cur, query)
    closeDB(conn)
    return table, colnames

if __name__ == '__main__':
    #Retrieve weight, throws, bats, throws, all birth-related and all name-related columns from the "Master" table and retrieve all columns from the "Batting" table for all players who have played at least 50 games and are still active
    query = 'SELECT m."nameFirst" || \' \' || m."nameLast" AS name, m."weight", m."height", m."bats", m."throws", m."birthYear", m."birthMonth", m."birthDay", b.* FROM "Master" AS m JOIN public."Batting" as b on m."playerID" = b."playerID" WHERE m."playerID" IN (SELECT m."playerID" FROM public."Master" AS m JOIN public."Batting" AS b on m."playerID" = b."playerID" WHERE m."finalGame" IS NULL AND m."birthYear" > 1900 GROUP BY m."playerID" HAVING SUM(b."G") >= 50) ORDER BY b."playerID"'
    table, colnames = getTable(query)

    #Turn queried table into Pandas DataFrame
    df = pd.DataFrame(table, columns=colnames)

    #Create datetime object using players' birth year,month,day
    #Determine age by subtracting birthdate from today, divide number of days by 365
    df = df.dropna(subset=["birthDay"])
    birthdate = pd.to_datetime(df.loc[:,'birthYear':'birthDay'].rename(columns={"birthYear": "year", "birthMonth": "month", "birthDay":"day"}))
    df.insert(6, "age", [int(math.floor((datetime.today()-x).days/365)) for x in birthdate])
    df.drop(columns=['battingID', 'birthYear', 'birthMonth', 'birthDay'], inplace=True)

    #Create DataFrame of each player with the batting stats summed up
    bat_sum_df = df.drop(columns=['name', 'weight', 'height', 'bats', 'throws', 'age', 'yearID', 'stint', 'teamID', 'lgID'])
    bat_sum_df = bat_sum_df.groupby(['playerID'], dropna=False).sum(min_count=1).reset_index()
    master_df = df.drop(columns=['yearID', 'teamID', 'lgID', 'stint', 'G',	'G_batting',	'AB',	'R',	'H',	'2B',	'3B',	'HR',	'RBI',	'SB',	'CS',	'BB',	'SO',	'IBB',	'HBP',	'SH',	'SF',	'GIDP',	'G_old'])
    master_df = master_df.groupby(['playerID']).first()
    players = pd.merge(master_df, bat_sum_df, on='playerID', how='inner')

    #Batting Stats Explained:
    #G=num games, G_batting=num games as batter, AB=at bats, R=runs, H=hits, 2B=doubles, 3B=triples,
    #HR=homeruns, RBI=rbi, SB=stolen bases, CS=caught stealing, BB=base on balls, SO=strikeouts,
    #IBB=intentional walks', HBP=hit by pitch, SH=sacrifice hits, SF=sacrifice flies, GIDP=ground into double play', G_old=old version

    #Drop all rows with any Null value
    df = df.dropna()

    #Which active player had the most runs batted in (“RBI” from the Batting table) from 2005-2008?
    maxRBIs = df[df['yearID'].isin([2005, 2006, 2007, 2008])].groupby(['playerID'])['RBI'].sum().reset_index(name='total RBIs').max()
    print()
    print("Which active player had the most runs batted in from 2005-2008?")
    print("Player:", str(df[df['playerID'] == maxRBIs['playerID']]['name'].iloc[0]), "\nTotal RBIs:", int(maxRBIs['total RBIs']))
    print()


    #How many double plays did Albert Pujols ground into (“GIDP” from Batting table) in 2006?
    print('How many double plays did Albert Pujols ground into in 2006?')
    print(int(df[(df['name'] == 'Albert Pujols') & (df['yearID'] == 2006)]['GIDP'].iloc[0]))
    print()

    #A histogram of triples (3B) per year
    triples_by_year = df.groupby(['yearID'])['3B'].sum().reset_index(name='total triples')
    #print(triples_by_year)
    plt.figure(figsize=(10,4))
    ax = plt.subplot(111)
    ax.set_title("Yearly Triples")
    ax.set_xlabel("Triples")
    ax.set_ylabel('Number of Years')
    ax = sns.histplot(x='total triples', data=triples_by_year)
    ax.bar_label(ax.containers[0])
    plt.savefig('images/Yearly_Triples_Histogram.png', dpi=400)
    plt.show()

    #A scatter plot relating triples (3B) and steals (SB)
    triples_steals = df.groupby(['playerID']).agg(
         sum_3B = ('3B','sum'),
         sum_SB = ('SB','sum'),
         ).reset_index()
    plt.figure(figsize=(5,5))
    ax = plt.subplot(111)
    ax = sns.regplot(x='sum_3B', y='sum_SB', data=triples_steals, ax=ax, order=2)
    ax.set_title('Correlation Between Triples and Steals')
    ax.set_xlabel('Triples')
    ax.set_ylabel('Steals')
    plt.savefig('images/Triples_Steals_Scatterplot.png', dpi=400)
    plt.show()

    #Create new calculated column for On Base Percentage
    #On Base Percentage = (hits + walks + hit by pitch) / (at bats + walks + hitt by pitch + sacrifice flies)
    players['OBP'] = (players['H'] + players['BB'] + players['IBB'] + players['HBP']) / (players['BB'] + players['IBB'] + players['HBP'] + players['SF'] + players['AB'])

    #Scatterplot Subplots comparing On Base Percentage to Walks, Strikeouts, At Bats, and Sacrifice Hits (sacrifice bunts) to determine which stat has the highest correlation
    fig, axes = plt.subplots(2, 4, figsize=(16,8))
    fig.suptitle('On Base Percentage versus Batting Stats', fontsize=15)
    sns.scatterplot(x='BB', y='OBP', data=players, ax=axes[0,0])
    axes[0,0].set_title('Walks')
    sns.scatterplot(x='BB', y='OBP', data=players, ax=axes[1,0])
    axes[1,0].set_ylim(0.25,0.45)
    sns.scatterplot(x='SO', y='OBP', data=players, ax=axes[0,1], color='red')
    axes[0,1].set_title('Strikeouts')
    axes[0,1].set_ylabel('')
    sns.scatterplot(x='SO', y='OBP', data=players, ax=axes[1,1], color='red')
    axes[1,1].set_ylim(0.25,0.45)
    axes[1,1].set_ylabel('')
    sns.scatterplot(x='AB', y='OBP', data=players, ax=axes[0,2], color='green')
    axes[0,2].set_title('At Bat')
    axes[0,2].set_ylabel('')
    sns.scatterplot(x='AB', y='OBP', data=players, ax=axes[1,2], color='green')
    axes[1,2].set_ylim(0.25,0.45)
    axes[1,2].set_ylabel('')
    sns.scatterplot(x='SH', y='OBP', data=players, ax=axes[0,3], color='orange')
    axes[0,3].set_title('Sacrifice Hits')
    axes[0,3].set_ylabel('')
    sns.scatterplot(x='SH', y='OBP', data=players, ax=axes[1,3], color='orange')
    axes[1,3].set_ylim(0.05,0.4)
    axes[1,3].set_ylabel('')
    plt.savefig('images/OBP_Scatterplots.png', dpi=400)
    plt.show()

    #Scatterplot Subplots comparing Intentional Walks to Homeruns, Hits and Runs to see which has the highest correlation
    plt.figure(figsize=(14,5))
    ax = plt.subplot(131)
    ax = sns.regplot(x='HR', y='IBB', data=players, ax=ax, order=2)
    ax.set_title('Homeruns v Intentional Walks')
    ax.set_xlabel('Homers')
    ax.set_ylabel('Intentional Walks')
    ax = plt.subplot(132)
    ax = sns.regplot(x='RBI', y='IBB', data=players, ax=ax, order=2)
    ax.set_title('RBI v Intentional Walks')
    ax.set_xlabel('RBI')
    ax.set_ylabel('')
    ax = plt.subplot(133)
    ax = sns.regplot(x='3B', y='IBB', data=players, ax=ax)
    ax.set_title('Triples v Intentional Walks')
    ax.set_xlabel('Triples')
    ax.set_ylabel('')
    plt.savefig('images/Intentional_Walks_Scatterplots.png', dpi=400)
    plt.show()

    #Create new DataFrame grouping by bat preference (left, right, both (ambidexterous))
    bats_stats = players.groupby(['bats']).agg(
        avg_OBP = ('OBP', 'mean'),
        total_HR = ('HR', 'sum'),
        total_walks = ('BB', 'sum'),
        total_hits = ('H', 'sum'),
        total_triples = ('3B', 'sum'),
        total_doubles = ('2B', 'sum'),
        total_rbi = ('RBI', 'sum'),
        total_strikeouts = ('SO', 'sum'),
        total_stolen = ('SB', 'sum'),
        total_intentionals = ('IBB', 'sum'),
        total_batters = ('bats', 'count')
        ).reset_index()
    bats_stats['batter_percent'] = bats_stats['total_batters']/bats_stats['total_batters'].sum() * 100
    bats_stats['HR_per_batter'] = round(bats_stats['total_HR'] / bats_stats['total_batters'], 1)
    bats_stats['walk_per_batter'] = round(bats_stats['total_walks'] / bats_stats['total_batters'], 1)
    bats_stats['hit_per_batter'] = round(bats_stats['total_hits'] / bats_stats['total_batters'], 1)
    bats_stats['triples_per_batter'] = round(bats_stats['total_triples'] / bats_stats['total_batters'], 1)
    bats_stats['doubles_per_batter'] = round(bats_stats['total_doubles'] / bats_stats['total_batters'], 1)
    bats_stats['rbi_per_batter'] = round(bats_stats['total_rbi'] / bats_stats['total_batters'], 1)
    bats_stats['strikeouts_per_batter'] = round(bats_stats['total_strikeouts'] / bats_stats['total_batters'], 1)
    bats_stats['stolen_per_batter'] = round(bats_stats['total_stolen'] / bats_stats['total_batters'], 1)
    bats_stats['intentionals_per_batter'] = round(bats_stats['total_intentionals'] / bats_stats['total_batters'], 1)

    #Create and customize scatterplot
    def customize_subplot(ax, column, x_label):
      sns.barplot(ax=ax, data=bats_stats, y=bats_stats['bats'], x=bats_stats[column], hue=bats_stats['bats'])
      for container in ax.containers:
        ax.bar_label(container)
      ax.set(xlabel=x_label, ylabel='')

    #Subplots, with the first being a pie chart showing the percentage of batters that bat right/left/both, and the rest showing the number of Homeruns, Walks, Hits, RBI, Triples, Doubles, Stolen Bases, and Intentional Walks per batter for each batting preference
    fig, axes = plt.subplots(2, 4, figsize=(16,8))
    fig.suptitle('How Batting Preference Affects Batting Stats', fontsize=15)
    explode = (.1,0,0)
    wedges, labels, texts = axes[0,0].pie(bats_stats['batter_percent'], autopct='%1.1f%%', explode=explode)
    axes[0,0].legend(wedges, ['Both', 'Left', 'Right'], frameon=True, loc='upper left')
    axes[0,0].set_title('Batting Preference Percentage')
    customize_subplot(axes[0,1], 'walk_per_batter', 'Number of Walks per Batter')
    customize_subplot(axes[0,2], 'hit_per_batter', 'Number of Hits per Batter')
    customize_subplot(axes[0,3], 'rbi_per_batter', 'Number of RBI per Batter')
    customize_subplot(axes[1,0], 'doubles_per_batter', 'Number of Doubles per Batter')
    customize_subplot(axes[1,1], 'triples_per_batter', 'Number of Triples per Batter')
    customize_subplot(axes[1,2], 'stolen_per_batter', 'Number of Stolen Bases per Batter')
    customize_subplot(axes[1,3], 'intentionals_per_batter', 'Number of Intentional Walks per Batter')
    plt.savefig('images/Batting_Preference_Scatterplots.png', dpi=400)
    plt.show()