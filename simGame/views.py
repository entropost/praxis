from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import simGame, Company, Market, CommonComponent, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import HrForm
from .helpers import simulateSales, constructNewCompanies, simulateNewMarket

# Create your views here.
def monthToString(month):
    months = ['December', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    return 'Y' + str((month - 1)//12) + ' ' + months[month % 12]

def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit= False)
            user.username = user.username.lower()
            user.save()
            userProfile = UserProfile(user=user, experience=0, level=1, elo=800)
            userProfile.save()
            login(request, user)
            return redirect('index')

    return render(request, 'login-register.html', {'form': form})

@login_required(login_url='login')
def mysimgames(request):
    allCompanies = Company.objects.filter(owner = request.user)
    return render(request, 'sessions.html', {'companies':allCompanies})

def index(request):
    return render(request, 'base.html')

@login_required(login_url='login')
def playSimGame(request, pk):
    if request.method == 'POST':
        game = simGame.objects.get(pk=pk)
        companies = Company.objects.filter(simgame=game, month = game.month)
        oldCompanies = Company.objects.filter(simgame=game, month = game.month - 1)
        market = Market.objects.filter(simgame=game, month= game.month)[0]
        globalDemandPi = {'P1':market.globalDemandP1, 'P2':market.globalDemandP2, 'P3':market.globalDemandP3}
        companies = simulateSales(companies, globalDemandPi, oldCompanies)
        for company in companies:
            company.save()
        newCompanies = constructNewCompanies(companies)

        for newCompany in newCompanies:
            newCompany.save()
            #print(newCompany.name, '   month:  ', newCompany.month)
        game.month += 1
        game.save()
        marketHandler = CommonComponent.objects.get(simgame=game)
        newMarket = simulateNewMarket(marketHandler)
        newMarket.save()
        print('Simulated')
        print(companies[0].salesP1)
        sgame = simGame.objects.get(id=pk)
        player = request.user
        company = Company.objects.filter(simgame = sgame, owner = player, month = sgame.month)[0]
        context = {'company':company, 'game':sgame}
        return redirect('play-simgame',pk)
        #return render(request, 'play.html', context)
        
    sgame = simGame.objects.get(id=pk)
    player = request.user
    company = Company.objects.filter(simgame = sgame, owner = player, month = sgame.month)[0]
    prevCompany = Company.objects.filter(simgame = sgame, owner = player, month = sgame.month - 1)[0]
    prevSales = prevCompany.salesP1 + prevCompany.salesP2 + prevCompany.salesP3
    prevRevenue = prevCompany.salesP1*prevCompany.priceP1 + prevCompany.salesP2*prevCompany.priceP2 + prevCompany.salesP3*prevCompany.salesP3
    lastYearCompaniesSalesP1 = {}
    lastYearCompaniesSalesP2 = {}
    lastYearCompaniesSalesP3 = {}
    months = {}
    i = 0
    for month in range(sgame.month - 12, sgame.month):
        lastYearCompaniesSalesP1['month' + str(i)] = Company.objects.filter(simgame=sgame, owner=player, month=month)[0].salesP1
        lastYearCompaniesSalesP2['month' + str(i)] = Company.objects.filter(simgame=sgame, owner=player, month=month)[0].salesP2
        lastYearCompaniesSalesP3['month' + str(i)] = Company.objects.filter(simgame=sgame, owner=player, month=month)[0].salesP3
        months['month' + str(i)] = monthToString(month=month)
        i += 1
        # lastYearCompaniesSalesP2.append(Company.objects.filter(simgame=sgame, owner=player, month=month)[0].salesP2)
        # lastYearCompaniesSalesP3.append(Company.objects.filter(simgame=sgame, owner=player, month=month)[0].salesP3)
    #lastYearCompany = Company.objects.filter(simgame=sgame, owner=player)
    context = {'company':company, 'game':sgame, 'prevSales': prevSales, 'prevRevenue':prevRevenue, 'lastYearCompaniesSalesP1':lastYearCompaniesSalesP1, 'months':months,
               'lastYearCompaniesSalesP2':lastYearCompaniesSalesP2,
               'lastYearCompaniesSalesP3':lastYearCompaniesSalesP3, 'prevCompany':prevCompany}
    return render(request, 'play.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            print()
        user = authenticate(request,username = username, password =  password)
        if user is not None:
            login(request, user)
            return redirect('index')
        
    page = 'login'
    return render(request, "login-register.html", {'page':page})

def logoutPage(request):
    logout(request)
    return redirect('index')

@login_required(login_url='login')
def createGame(request):
    if request.method == 'POST':
        maxPlayers = request.POST.get("numberOfPlayers")
        duration = request.POST.get("gameDuration")
        simGameName = str(request.user.username) + "'s simulation"
        newGame = simGame(name = simGameName, status = 'pending', month = 1, host = request.user, maxCompanies = maxPlayers, duration = duration)
        newGame.save()
        return redirect('my-sessions')
    context = {}
    return render(request, 'create-game.html', context)

@login_required(login_url='login')
def pendingGames(request):
    allPendingGames = simGame.objects.filter(status='pending')
    context = {"games": allPendingGames, "page": "allGames"}
    return render(request,"sessions.html" , context)

@login_required(login_url='login')
def joinSession(request, pk):
    if request.method == 'POST':
        user = request.user
        game = simGame.objects.get(pk=pk)
        name = request.POST.get("company-name")
        candidates = Company.objects.filter(simgame=game)
        anass = User.objects.get(username='maalmianass')
        flag = request.user not in [candidate.owner for candidate in candidates]
        if anass in [candidate.owner for candidate in candidates]:
            if user.username == 'asano':
                message = "Asano cannot join session where maalmianass is a participant"
                return render(request, 'join-session.html', context = {"session":game, "candidates":candidates, "message":message, "maxplayers":game.maxCompanies, 'flag':flag})
        if request.user in [candidate.owner for candidate in candidates]:
            message = "you already joined this session"
            return render(request, 'join-session.html', context = {"session":game, "candidates":candidates, "message":message,
            "maxplayers" : game.maxCompanies, "remaining":game.maxCompanies - candidates.count()})
        company = Company(simgame=game, owner=user, month= 1, name=name)
        company.save()
    game = simGame.objects.get(pk=pk)
    candidates = Company.objects.filter(simgame=game)
    message = None
    flag = request.user not in [candidate.owner for candidate in candidates]
    context = {"session":game, "candidates":candidates, "message":message, "remaining":game.maxCompanies - candidates.count(), "maxplayers" : game.maxCompanies, "flag":flag}
    
    return render(request, "join-session.html", context)

@login_required(login_url='login')
def marketDecisions(request, pk):
    user = request.user
    game = simGame.objects.get(pk=pk)
    company = Company.objects.filter(simgame=game, owner=user, month=game.month)[0]
    candidates = Company.objects.filter(simgame=game)
    flag = request.user not in [candidate.owner for candidate in candidates]
    context = {'user':user, 'game':game, 'company':company}
    if flag:
        # User not in session
        pass
    if request.method == 'POST':
        PriceP1 = request.POST.get("price-P1")
        PriceP2 = request.POST.get("price-P2")
        PriceP3 = request.POST.get("price-P3")
        BrandPub = request.POST.get("brand-pub")
        PubP1 = request.POST.get("pub-P1")
        PubP2 = request.POST.get("pub-P2")
        PubP3 = request.POST.get("pub-P3")
        company.priceP1 = PriceP1
        company.priceP2 = PriceP2
        company.priceP3 = PriceP3
        company.pubBrand = BrandPub
        company.pubP1 = PubP1
        company.pubP2 = PubP2
        company.pubP3 = PubP3
        company.save()
        return render(request, "marketing-decisions.html", context)


    context = {'user':user, 'game':game, 'company':company}
    return render(request, "marketing-decisions.html", context)

@login_required(login_url='login')
def prodDecisions(request, pk):
    user = request.user
    game = simGame.objects.get(pk=pk)
    company = Company.objects.filter(simgame=game, owner=user, month=game.month)[0]
    candidates = Company.objects.filter(simgame=game)
    flag = request.user not in [candidate.owner for candidate in candidates]
    context = {'user':user, 'game':game, 'company':company}
    if flag:
        # User not in session
        pass
    if request.method == 'POST':
        prodP1 = request.POST.get("prod-P1")
        prodP2 = request.POST.get("prod-P2")
        prodP3 = request.POST.get("prod-P3")
        acqMoul = request.POST.get("acq-moulage")
        cesMoul = request.POST.get("ces-moulage")
        acqFin = request.POST.get("acq-finition")
        cesFin = request.POST.get("ces-finition")
        newLeasingFin = request.POST.get("leasing-finition")
        newLeasingMoul = request.POST.get("leasing-moulage")
        #Company.objects.filter(pk=company.id).update(prodOrderP1=prodP1, prodOrderP2=prodP2,prodOrderP3=prodP3, acqMoul=acqMoul, cesMoul=cesMoul, acqFin=acqFin, cesFin=cesFin, newLeasingMoul=newLeasingMoul,
        #newLeasingFin=newLeasingFin)
        company.prodOrderP1 = prodP1
        company.prodOrderP2 = prodP2
        company.prodOrderP3 = prodP3
        company.acqMoul = acqMoul
        company.acqFin = acqFin
        company.cesMoul = cesMoul
        company.cesFin = cesFin
        company.newLeasingFin = newLeasingFin
        company.newLeasingMoul = newLeasingMoul
        company.save()
        return render(request, "production-decisions.html", context)


    context = {'user':user, 'game':game, 'company':company}
    return render(request, "production-decisions.html", context)


@login_required(login_url='login')
def supplyDecisions(request, pk):
    user = request.user
    game = simGame.objects.get(pk=pk)
    company = Company.objects.filter(simgame=game, owner=user, month=game.month)[0]
    candidates = Company.objects.filter(simgame=game)
    flag = request.user not in [candidate.owner for candidate in candidates]
    context = {'user':user, 'game':game, 'company':company}
    if flag:
        # User not in session
        pass
    if request.method == 'POST':
        plas1 = request.POST.get("plas1")
        plas2 = request.POST.get("plas2")
        plas3 = request.POST.get("plas3")
        wood1 = request.POST.get("wood1")
        wood2 = request.POST.get("wood2")
        wood3 = request.POST.get("wood3")
        company.comWood1 = wood1
        company.comWood2 = wood2
        company.comWood3 = wood3
        company.comPlastic1 = plas1
        company.comPlastic2 = plas2
        company.comPlastic3 = plas3

        company.save()
        return render(request, "supply-decisions.html", context)
    context = {'user':user, 'game':game, 'company':company}
    return render(request, "supply-decisions.html", context)


@login_required(login_url='login')
def adminFinDecisions(request, pk):
    user = request.user
    game = simGame.objects.get(pk=pk)
    company = Company.objects.filter(simgame=game, owner=user, month=game.month)[0]
    candidates = Company.objects.filter(simgame=game)
    flag = request.user not in [candidate.owner for candidate in candidates]
    context = {'user':user, 'game':game, 'company':company}
    if flag:
        # User not in session
        pass
    if request.method == 'POST':
        savingsInvestment = request.POST.get("savings-investment")
        savingsWithdrawal = request.POST.get("savings-withdrawal")
        company.savingsInvestment = savingsInvestment
        company.savingsWithdrawal = savingsWithdrawal


        company.save()
        return render(request, "adminfin-decisions.html", context)


    context = {'user':user, 'game':game, 'company':company}
    return render(request, "adminfin-decisions.html", context)


@login_required(login_url='login')
def HrDecisions(request, pk):
    user = request.user
    game = simGame.objects.get(pk=pk)
    company = Company.objects.filter(simgame=game, owner=user, month=game.month)[0]
    candidates = Company.objects.filter(simgame=game)
    flag = request.user not in [candidate.owner for candidate in candidates]
    form = HrForm()    
    context = {'user':user,'game':game, 'company':company, 'form':form, 'flag':flag}
    if request.method == 'POST':
        form = HrForm(request.POST)
        return 0
    
    return render(request, 'hr-decisions.html', context)

