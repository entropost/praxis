import numpy as np
from .models import simGame, Company, CommonComponent, Market
from decimal import Decimal


def simulateNewMarket(marketHandler):
    game = marketHandler.simgame
    p1 = 500
    p2 = 300
    p3 = 150
    nMarket = Market(simgame=game, month = game.month, globalDemandP1 = p1, globalDemandP2 = p2, globalDemandP3 = p3)
    return nMarket


def constructNewCompanies(companies):
    new_companies = []
    
    for company in companies:
        f = {'simgame': company.simgame, 'owner': company.owner, 'month': company.month + 1, 'name': company.name,
             'priceP1': company.priceP1, 'priceP2': company.priceP2, 'priceP3': company.priceP3, 'pubBrand': company.pubBrand, 
             'pubP1': company.pubP1, 'pubP2': company.pubP2, 'pubP3': company.pubP3, 'payDelP1': company.payDelP1,
             'payDelP2': company.payDelP2, 'payDelP3': company.payDelP3}
        newCompany = Company(**f)
        new_companies.append(newCompany)
    return new_companies


# List of companies, globalDemand, Products_i -> List of Sales
def simulateSales(companies, globalDemandPi, oldCompanies):
    pricesPi = getPrices(companies)   # PricesP1, P2, P3, for all companies
    products = ('P1', 'P2', 'P3')
    QAPi = {}
    scorePubBrand = {}
    scorePubPi = {}
    scoreDPPi = {}
    QPPi = {}
    satPi = {}
    salesPi = {}
    marketPartsPi = {}
    salesPi = {}
    

    
    pubPi = getPubPi(companies)
    pubBrand = getPubBrand(companies)
    payDelayPi = getPayDelayPi(companies)

    for product in products:
        QAPi[product] = ArrLogNorm(pricesPi[product])
        scorePubPi[product] = ArrLogNorm(pubPi[product])
        scoreDPPi[product] = ArrLogNorm(payDelayPi[product])
        scorePubBrand[product] = ArrLogNorm(pubBrand[product])
        QPPi[product] = matMean(scoreDPPi[product], scorePubBrand[product], scorePubPi[product], companies)
        satPi[product] = getSatPi(QPPi[product], QAPi[product], companies)
        marketPartsPi[product] = getMarketPartsPi(satPi[product], companies)
        salesPi[product] = getSalesPi(marketPartsPi[product], globalDemandPi[product], companies)

    
    for company in companies:
        company.scoreQAP1 = QAPi['P1'][company]
        company.scoreQAP2 = QAPi['P2'][company]
        company.scoreQAP3 = QAPi['P3'][company]

        company.scoreQPP1 = QPPi['P1'][company]
        company.scoreQPP2 = QPPi['P2'][company]
        company.scoreQPP3 = QPPi['P3'][company]

        company.scoreSatP1 = satPi['P1'][company]
        company.scoreSatP2 = satPi['P2'][company]
        company.scoreSatP3 = satPi['P3'][company]

        company.scorePubP1 = scorePubPi['P1'][company]
        company.scorePubP2 = scorePubPi['P2'][company]
        company.scorePubP3 = scorePubPi['P3'][company]

        company.scorePubBrandP1 = scorePubBrand['P1'][company]
        company.scorePubBrandP2 = scorePubBrand['P2'][company]
        company.scorePubBrandP3 = scorePubBrand['P3'][company]

        company.scorePayDelP1 = scoreDPPi['P1'][company]
        company.scorePayDelP2 = scoreDPPi['P2'][company]
        company.scorePayDelP3 = scoreDPPi['P3'][company]

        company.salesP1 = int(salesPi['P1'][company])
        company.salesP2 = int(salesPi['P2'][company])
        company.salesP3 = int(salesPi['P3'][company])
        company.salesGlob = company.salesP1 + company.salesP2 + company.salesP3

        company.revenueP1 = company.salesP1 * company.priceP1
        company.revenueP2 = company.salesP2 * company.priceP2
        company.revenueP3 = company.salesP3 * company.priceP3
        company.revenueGlob = company.revenueP1 + company.revenueP2 + company.revenueP3

        oldCompany = Company.objects.filter(simgame=company.simgame, owner=company.owner, month=company.month - 1)[0]
        salesVariation = (company.salesP1 + company.salesP2 + company.salesP3) / (oldCompany.salesP1 + oldCompany.salesP2 + oldCompany.salesP3) - 1
        revenueVariation = (company.revenueP1 + company.revenueP2 +company.revenueP3) / (oldCompany.revenueP1 + oldCompany.revenueP2 + oldCompany.revenueP3) - 1
        company.salesVariations = Decimal(salesVariation) * 100
        company.revenueVariations = Decimal(revenueVariation) * 100
        company.marketPartP1 = marketPartsPi['P1'][company] * 100
        company.marketPartP2 = marketPartsPi['P2'][company] * 100
        company.marketPartP3 = marketPartsPi['P3'][company] * 100

    for company in companies:
        company.marketPartGlob = 100 * company.revenueGlob / sum([comp.revenueGlob for comp in companies])
        oldCompany = Company.objects.filter(simgame=company.simgame, owner=company.owner, month=company.month - 1)[0]
        mpartVar = company.marketPartGlob - oldCompany.marketPartGlob
        company.marketPartVar = mpartVar
    


    

    #satPi = getSatPi(QPPi, QAPi)

    

    #salesPi = getSalesPi(marketPartsPi, globalDemandPi)

    return companies


def getPrices(companies):
    pricesP1 = {}
    pricesP2 = {}
    pricesP3 = {}
    for company in companies:
        pricesP1[company] = company.priceP1
        pricesP2[company] = company.priceP2
        pricesP3[company] = company.priceP3
    pricesPi = {'P1':pricesP1, 'P2':pricesP2, 'P3':pricesP3}
    return pricesPi


def ArrLogNorm(context):
    mu = Decimal(np.mean(list(context.values())))
    std = Decimal(np.std(list(context.values())))
    nContext = {}
    for company_element in context:
        nContext[company_element] = logistic((context[company_element] - mu) / (std + Decimal(0.5)))
    return nContext

def logistic(x):
    return 1 / (1 + np.exp(-x))

def getPubPi(companies):
    pubP1 = {}
    pubP2 = {}
    pubP3 = {}
    for company in companies:
        pubP1[company] = company.pubP1
        pubP2[company] = company.pubP2
        pubP3[company] = company.pubP3
    pubPi = {'P1':pubP1, 'P2':pubP2, 'P3':pubP3}
    return pubPi

def getPubBrand(companies):
    pubBrand = {}
    for company in companies:
        pubBrand[company] = company.pubBrand
    return {'P1': pubBrand, 'P2': pubBrand, 'P3': pubBrand}

def getPayDelayPi(companies):
    payDelayP1 = {}
    payDelayP2 = {}
    payDelayP3 = {}
    for company in companies:
        payDelayP1[company] = company.payDelP1
        payDelayP2[company] = company.payDelP2
        payDelayP3[company] = company.payDelP3
    payDelayPi = {'P1':payDelayP1, 'P2':payDelayP2, 'P3':payDelayP3}
    return payDelayPi

def matMean(scoreDPPi, scorePubBrand, scorePubPi, companies):
    QPPi = {}
    for company in companies:
        QPPi[company] = (scoreDPPi[company] + scorePubBrand[company] + scorePubPi[company]) / 3
    return QPPi

def getSatPi(QPPi, QAPi, companies):
    satPi = {}
    for company in companies:
        satPi[company] = QPPi[company] / QAPi[company] * 100
    return satPi

def getMarketPartsPi(satPi, companies):
    marketPartsPi = {}
    satSum = np.sum(list(satPi.values()))
    for company in companies:
        marketPartsPi[company] = satPi[company] / satSum
    return marketPartsPi

def getSalesPi(marketPartsPi, globalDemandPi, companies):
    salesPi = {}
    for company in companies:
        salesPi[company] = marketPartsPi[company] * globalDemandPi
    return salesPi




# PricesP1T = {}
# PricesP1T['company1'] = 100
# PricesP1T['company2'] = 50
# PricesP1T['company3'] = 100
# PricesP1T['company4'] = 77
# PricesP1T['company5'] = 1000
# PricesP1T['company6'] = 15



# if __name__ == "__main__":
#     print(ArrLogNorm(PricesP1T))