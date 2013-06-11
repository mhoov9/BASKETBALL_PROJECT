#data acquired from NBA statistics website
#I normalized Field Goal Efficiency(eFG), Offensive Rebound Percentage(OR),
#Turnover Percentage(TO), and Rate of Free Throw Attempts(FTA) to values between
#O and 1 so that I can later create weighted values of these statistics based
#on how important they are to generating wins. 
wins = [66,
60,
58,
57,
56,
56,
54,
49,
49,
47,
45,
45,
45,
44,
43,
41,
41,
38,
34,
34,
33,
31,
29,
29,
28,
27,
25,
24,
21,
20]

eFG = [1,
0.945736434,
0.891472868,
0.666666667,
0.759689922,
0.480620155,
0.550387597,
0.457364341,
0.697674419,
0.651162791,
0.441860465,
0.674418605,
0.620155039,
0.658914729,
0.426356589,
0.658914729,
0.604651163,
0.372093023,
0.387596899,
0.403100775,
0.387596899,
0.534883721,
0.356589147,
0.434108527,
0.294573643,
0.255813953,
0.201550388,
0.108527132,
0,
0.317829457]

TO = [0.672727273,
0.272727273,
0.436363636,
0.509090909,
0.690909091,
0.709090909,
1,
0.163636364,
0.072727273,
0.090909091,
0.290909091,
0.090909091,
0,
0.454545455,
0.4,
0.509090909,
0.527272727,
0.818181818,
0.654545455,
0.509090909,
0.109090909,
0.618181818,
0.145454545,
0.309090909,
0.436363636,
0.163636364,
0.363636364,
0.672727273,
0.418181818,
0]

OR= [0.151260504,
0.56302521,
0.168067227,
0.823529412,
0.74789916,
1,
0.579831933,
0.941176471,
0.966386555,
0.630252101,
0.806722689,
0.68907563,
0.663865546,
0.201680672,
0.722689076,
0,
0.12605042,
0.487394958,
0.411764706,
0.462184874,
0.43697479,
0.672268908,
0.663865546,
0.487394958,
0.352941176,
0.857142857,
0.462184874,
0.613445378,
0.285714286,
0.554621849]

FTA = [0.539267016,
0.795811518,
0.476439791,
0.586387435,
0.251308901,
0.261780105,
0.209424084,
0.67539267,
0.528795812,
0.214659686,
0.256544503,
0.643979058,
1,
0.392670157,
0.267015707,
0.204188482,
0.041884817,
0.204188482,
0.020942408,
0.057591623,
0.366492147,
0.654450262,
0.397905759,
0.261780105,
0.256544503,
0.219895288,
0.146596859,
0.151832461,
0.596858639,
0]

teams = ["Miami Heat",
"Oklahoma City Thunder",
"San Antonio Spurs",
"Denver Nuggets",
"Los Angeles Clippers",
"Memphis Grizzlies",
"New York Knicks",
"Brooklyn Nets",
"Indiana Pacers",
"Golden State Warriors",
"Chicago Bulls",
"Houston Rockets",
"Los Angeles Lakers",
"Atlanta Hawks",
"Utah Jazz",
"Boston Celtics",
"Dallas Mavericks",
"Milwaukee Bucks",
"Philadelphia 76ers",
"Toronto Raptors",
"Portland Trail Blazers",
"Minnesota Timberwolves",
"Detroit Pistons",
"Washington Wizards",
"Sacramento Kings",
"New Orleans Hornets",
"Phoenix Suns",
"Cleveland Cavaliers",
"Charlotte Bobcats",
"Orlando Magic"]


#list of grouped statistics separated by team
def stat_list(eFG,TO,OR,FTA):
	stats = []
	for i in range(0,len(eFG)):
		stats.append([eFG[i],TO[i],OR[i],FTA[i]])
	return stats

#returns a list of possible multipliers
#i will later extract the group of multipliers that best correlates with actual wins
def multiplier(A,B,C,D):
	mult_list = []
	weights = [A,B,C,D]
	for D in range(1,24):
		while C < B:
			B = C + 1
			A = 100-(B+C+D)
			while B < A:
				weights = [A,B,C,D]
				mult_list.append(weights)
				A -= 1
				B += 1
			B = weights[1]
			C += 1
		C = D + 2
		B = D + 3
	return mult_list

#creates a list corresponding to every multiplier of predicted win percentages
#for every team pcts_per_multiplier 
def win_pct_lists(eFG,TO,OR,FTA):
    win_pcts = []
    pcts_per_multiplier = []
    for j in range(0, len(multiplier(94,3,2,1))):
            weights = multiplier(94,3,2,1)[j]
            for k in range(0, len(stat_list(eFG, TO, OR, FTA))):
                    factors = stat_list(eFG, TO, OR, FTA)[k]
                    win_pct = (factors[0]*weights[0]+factors[1]*weights[1]+factors[2]*weights[2]+factors[3]*weights[3])
                    pcts_per_multiplier.append(win_pct)
            win_pcts.append(pcts_per_multiplier)
            pcts_per_multiplier = []
    return win_pcts

#function for to find the correlation coefficient between two sets of data
#in this case I am comparing each group in the list win_pcts with acual data for wins
def corr_coef(x,y,n):
	sumxy = 0
	sumx = 0
	sumy = 0
	sumx2 = 0
	sumy2 = 0
	for i in range(0,n):
		sumxy += x[i]*y[i]
		sumx += x[i]
		sumy += y[i]
		sumx2 += (x[i])**2
		sumy2 += (y[i])**2
	r = (n*sumxy - (sumx*sumy))/(((n*sumx2 - sumx**2)*(n*sumy2 - sumy**2))**.5)
	return r
    
#correlates each set of win_pcts with actual wins
#returns the best highest correlation coefficient and the corresponding multiplier
def best_guess(W):
	coef_list = []
	for n in range(0,len(W)):
		guess = W[n]
		coef_list.append(corr_coef(guess, wins, 30))
	best_correlation = max(coef_list)
	best_multiplier = multiplier(94,3,2,1)[coef_list.index(best_correlation)]
	mult_and_corr = [best_correlation,best_multiplier]
	return mult_and_corr

#using the multiplier that best weights the importance of the four statistic groups
#the function returns a list of predicted wins for the teams involved
def predicted_wins(stats,multiplier):
	hyp_wins = []
	for k in range(0, len(stats)):
		factors = stats[k]
		win_pct = (factors[0]*multiplier[0]+factors[1]*multiplier[1]+factors[2]*multiplier[2]+factors[3]*multiplier[3])
		hyp_wins.append((win_pct/100)*82)
	return hyp_wins

#assigns predicted wins with each team and displays how important
#each of the four factors are for winning in the league during this year
def fourfactorseason(team,wins):
    four_factors = best_guess(win_pct_lists(eFG,TO,OR,FTA))[1]
    for i in range(0,len(team)):
        print(teams[i]+":"+ str(predicted_wins(stat_list(eFG,TO,OR,FTA),best_guess(win_pct_lists(eFG,TO,OR,FTA))[1])[i])+ " wins")
    print("Importance of the Four Factors:")
    print("eFG%: " + str(four_factors[0]) + "%, TO%: " + str(four_factors[1]) +"%, OR%: " + str(four_factors[2]) + "%, FTA RATE: " +str(four_factors[3]) + "%")
    

#Prints function fourfactorseason
fourfactorseason(teams,predicted_wins(stat_list(eFG,TO,OR,FTA),best_guess(win_pct_lists(eFG,TO,OR,FTA))[1]))
