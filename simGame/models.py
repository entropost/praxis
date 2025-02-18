from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class simGame(models.Model):
    name = models.CharField(max_length=100)
    host = models.ForeignKey(User, on_delete = models.RESTRICT, null = True)
    status = models.CharField(max_length=10)
    scenario = models.CharField(max_length=15)
    month = models.IntegerField(null = True)
    maxCompanies = models.IntegerField(null = True)
    duration = models.IntegerField(null = True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class CommonComponent(models.Model):
    '''A class that handles many aspects of the game. Each time the game simulates a month and moves to the next one, this handler, determines the global demand for each product
    using seasonal coefficients and phase factors.'''
    simgame = models.ForeignKey(simGame, on_delete = models.RESTRICT)
    #seasonal coefs
    seasonalCoefM1P1 = models.DecimalField(max_digits=4, decimal_places=2)
    seasonalCoefM2P1 = models.DecimalField(max_digits=4, decimal_places=2)
    seasonalCoefM3P1 = models.DecimalField(max_digits=4, decimal_places=2)
    seasonalCoefM4P1 = models.DecimalField(max_digits=4, decimal_places=2)
    seasonalCoefM5P1 = models.DecimalField(max_digits=4, decimal_places=2)
    seasonalCoefM6P1 = models.DecimalField(max_digits=4, decimal_places=2)
    seasonalCoefM7P1 = models.DecimalField(max_digits=4, decimal_places=2)
    seasonalCoefM8P1 = models.DecimalField(max_digits=4, decimal_places=2)
    seasonalCoefM9P1 = models.DecimalField(max_digits=4, decimal_places=2)
    seasonalCoefM10P1 = models.DecimalField(max_digits=4, decimal_places=2)
    seasonalCoefM11P1 = models.DecimalField(max_digits=4, decimal_places=2)
    seasonalCoefM12P1 = models.DecimalField(max_digits=4, decimal_places=2)

    seasonalCoefM1P2 = models.DecimalField(max_digits=4, decimal_places=2)
    seasonalCoefM2P2 = models.DecimalField(max_digits=4, decimal_places=2)
    seasonalCoefM3P2 = models.DecimalField(max_digits=4, decimal_places=2)
    seasonalCoefM4P2 = models.DecimalField(max_digits=4, decimal_places=2)
    seasonalCoefM5P2 = models.DecimalField(max_digits=4, decimal_places=2)
    seasonalCoefM6P2 = models.DecimalField(max_digits=4, decimal_places=2)
    seasonalCoefM7P2 = models.DecimalField(max_digits=4, decimal_places=2)
    seasonalCoefM8P2 = models.DecimalField(max_digits=4, decimal_places=2)
    seasonalCoefM9P2 = models.DecimalField(max_digits=4, decimal_places=2)
    seasonalCoefM10P2 = models.DecimalField(max_digits=4, decimal_places=2)
    seasonalCoefM11P2 = models.DecimalField(max_digits=4, decimal_places=2)
    seasonalCoefM12P2 = models.DecimalField(max_digits=4, decimal_places=2)
    
    seasonalCoefM1P3 = models.DecimalField(max_digits=4, decimal_places=2)
    seasonalCoefM2P3 = models.DecimalField(max_digits=4, decimal_places=2)
    seasonalCoefM3P3 = models.DecimalField(max_digits=4, decimal_places=2)
    seasonalCoefM4P3 = models.DecimalField(max_digits=4, decimal_places=2)
    seasonalCoefM5P3 = models.DecimalField(max_digits=4, decimal_places=2)
    seasonalCoefM6P3 = models.DecimalField(max_digits=4, decimal_places=2)
    seasonalCoefM7P3 = models.DecimalField(max_digits=4, decimal_places=2)
    seasonalCoefM8P3 = models.DecimalField(max_digits=4, decimal_places=2)
    seasonalCoefM9P3 = models.DecimalField(max_digits=4, decimal_places=2)
    seasonalCoefM10P3 = models.DecimalField(max_digits=4, decimal_places=2)
    seasonalCoefM11P3 = models.DecimalField(max_digits=4, decimal_places=2)
    seasonalCoefM12P3 = models.DecimalField(max_digits=4, decimal_places=2)

    initPhaseP1 = models.CharField(max_length=10)
    initPhaseP2 = models.CharField(max_length=10)
    initPhaseP3 = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    phasefactors = {'phase0':1,'phase1': 1.2, 'phase2':0.8,'phase3':1.05,'phase4':1.45}
    phaseDuration = {'phase0':12,'phase1': 9, 'phase2':18,'phase3':24,'phase4':6}

class Market(models.Model):
    month = models.IntegerField()
    simgame = models.ForeignKey(simGame, on_delete = models.CASCADE)

    globalDemandP1 = models.IntegerField()
    globalDemandP2 = models.IntegerField()
    globalDemandP3 = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Company(models.Model):
    simgame = models.ForeignKey(simGame, on_delete = models.RESTRICT)
    owner = models.ForeignKey(User, on_delete = models.RESTRICT, null = True)
    month = models.IntegerField()
    name = models.CharField(max_length=100)
    #lDecisions
    #lDecisions.lMarketDec
    priceP1 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True)
    priceP2 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True)
    priceP3 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True)
    pubBrand = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True)
    pubP1 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True)
    pubP2 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True)
    pubP3 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True)
    payDelP1 = models.IntegerField(null = True, blank = True)
    payDelP2 = models.IntegerField(null = True, blank = True)
    payDelP3 = models.IntegerField(null = True, blank = True)
    #lDecisions.lProdDec
    prodOrderP1 = models.IntegerField(null = True, blank = True)
    prodOrderP2 = models.IntegerField(null = True, blank = True)
    prodOrderP3 = models.IntegerField(null = True, blank = True)
    acqMoul = models.IntegerField(null = True, blank = True)
    acqFin = models.IntegerField(null = True, blank = True)
    cesMoul = models.IntegerField(null = True, blank = True)
    cesFin = models.IntegerField(null = True, blank = True)
    newLeasingMoul = models.IntegerField(null = True, blank = True)
    newLeasingFin = models.IntegerField(null = True, blank = True)
    #lDecisions.lAppDec
    comWood1 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True)
    comWood2 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True)
    comWood3 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True)
    comPlastic1 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True)
    comPlastic2 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True)
    comPlastic3 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True)
    #lDecisions.lHrDec
    commercialRepHirings = models.IntegerField(null = True, blank = True)
    commercialRepDismissals = models.IntegerField(null = True, blank = True)
    commercialRepBaseSalary = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True)
    commercialRepCommisions = models.DecimalField(max_digits=4, decimal_places=2, null = True, blank = True)

    productionDirHirings = models.IntegerField(null = True, blank = True)
    productionDirDismissals = models.IntegerField(null = True, blank = True)
    productionDirBaseSalary = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True)

    productionExecHirings = models.IntegerField(null = True, blank = True)
    productionExecDismissals = models.IntegerField(null = True, blank = True)
    productionExecBaseSalary = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True)

    productionEmpHirings = models.IntegerField(null = True, blank = True)
    productionEmpDismissals = models.IntegerField(null = True, blank = True)
    productionEmpBaseSalary = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True)

    supplyDirHirings = models.IntegerField(null = True, blank = True)
    supplyDirDismissals = models.IntegerField(null = True, blank = True)
    supplyDirBaseSalary = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True)

    supplyExecHirings = models.IntegerField(null = True, blank = True)
    supplyExecDismissals = models.IntegerField(null = True, blank = True)
    supplyExecBaseSalary = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True)

    supplyEmpHirings = models.IntegerField(null = True, blank = True)
    supplyEmpDismissals = models.IntegerField(null = True, blank = True)
    supplyEmpBaseSalary = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True)

    administrationDirHirings = models.IntegerField(null = True, blank = True)
    administrationDirDismissals = models.IntegerField(null = True, blank = True)
    administrationDirBaseSalary = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True)

    administrationExecHirings = models.IntegerField(null = True, blank = True)
    administrationExecDimissals = models.IntegerField(null = True, blank = True)
    administrationExecBaseSalary = models.IntegerField(null = True, blank = True)

    administrationEmpHirings = models.IntegerField(null = True, blank = True)
    administrationEmpDismissals = models.IntegerField(null = True, blank = True)
    administrationEmpBaseSalary = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True)
        
    #lDecisions.lAdminDec
    savingsInvestment = models.DecimalField(max_digits=10, decimal_places=2, null = True, blank = True)
    savingsWithdrawal = models.DecimalField(max_digits=10, decimal_places=2, null = True, blank = True)
    insuranceSubscription = models.BooleanField(null = True, blank = True)

    #lIndicators
        ##score sat clt ?
    scoreQAP1 = models.DecimalField(max_digits=5, decimal_places=2, null = True, blank = True)
    scoreQAP2 = models.DecimalField(max_digits=5, decimal_places=2, null = True, blank = True)
    scoreQAP3 = models.DecimalField(max_digits=5, decimal_places=2, null = True, blank = True)

    scoreQPP1 = models.DecimalField(max_digits=5, decimal_places=2, null = True, blank = True)
    scoreQPP2 = models.DecimalField(max_digits=5, decimal_places=2, null = True, blank = True)
    scoreQPP3 = models.DecimalField(max_digits=5, decimal_places=2, null = True, blank = True)

    scoreSatP1 = models.DecimalField(max_digits=5, decimal_places=2, null = True, blank = True)
    scoreSatP2 = models.DecimalField(max_digits=5, decimal_places=2, null = True, blank = True)
    scoreSatP3 = models.DecimalField(max_digits=5, decimal_places=2, null = True, blank = True)

    scorePubBrandP1 = models.DecimalField(max_digits=5, decimal_places=2, null = True, blank = True)
    scorePubBrandP2 = models.DecimalField(max_digits=5, decimal_places=2, null = True, blank = True)
    scorePubBrandP3 = models.DecimalField(max_digits=5, decimal_places=2, null = True, blank = True)

    scorePubP1 = models.DecimalField(max_digits=5, decimal_places=2, null = True, blank = True)
    scorePubP2 = models.DecimalField(max_digits=5, decimal_places=2, null = True, blank = True)
    scorePubP3 = models.DecimalField(max_digits=5, decimal_places=2, null = True, blank = True)

    scorePayDelP1 = models.DecimalField(max_digits=5, decimal_places=2, null = True, blank = True)
    scorePayDelP2 = models.DecimalField(max_digits=5, decimal_places=2, null = True, blank = True)
    scorePayDelP3 = models.DecimalField(max_digits=5, decimal_places=2, null = True, blank = True)

    scoreSellingForceP1 = models.DecimalField(max_digits=5, decimal_places=2, null = True, blank = True)
    scoreSellingForceP2 = models.DecimalField(max_digits=5, decimal_places=2, null = True, blank = True)
    scoreSellingForceP3 = models.DecimalField(max_digits=5, decimal_places=2, null = True, blank = True)

    salesP1 = models.IntegerField(null = True, blank = True)
    salesP2 = models.IntegerField(null = True, blank = True)
    salesP3 =  models.IntegerField(null = True, blank = True)
    salesGlob = models.IntegerField(null = True, blank = True)

    revenueP1 = models.DecimalField(max_digits=12, decimal_places=2, null = True, blank = True)
    revenueP2 = models.DecimalField(max_digits=12, decimal_places=2, null = True, blank = True)
    revenueP3 = models.DecimalField(max_digits=12, decimal_places=2, null = True, blank = True)
    revenueGlob = models.DecimalField(max_digits=12, decimal_places=2, null = True, blank = True)

    decisionsSaved = models.BooleanField(default=False)
    is_simulated = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    revenueVariations = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    salesVariations = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    marketPartP1 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    marketPartP2 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    marketPartP3 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    marketPartGlob = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    marketPartVar = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Accounting fields
    # Assets
    intangibleAssets = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    land = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    constructions = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    machines = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    rawMaterials = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    finishedProducts = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    accountsReceivable = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    defferedTaxAssets = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    taxDeposit = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    savingsAccount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    cash = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    # Equity
    capital = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    legalReserves = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    optionalReserves = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    retainedEarnings = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    # Liabilities
    riskProvisons = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    loans = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    accountsPayable = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    defferedTaxLiabilities = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    incomeTaxLiabilities = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    otherLiabilities = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)



class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete = models.RESTRICT, null = True)
    experience = models.FloatField()
    level = models.IntegerField(null=True)
    elo = models.IntegerField()
    #friends = models.ManyToManyField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
