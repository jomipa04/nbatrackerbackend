from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView,Response
from .models import  Details, Games
from .serializers import  DetailsSerializer, GamesSerializer

@api_view(['GET'])
def getMe(request):
    games = Games.objects.all()
    games_data=GamesSerializer(games, many=True).data

    lastTen = games.order_by('-id')[:10]
    lastTen_data =GamesSerializer(lastTen, many=True).data
    if len(games_data)==0:
        return Response({"data":{"message":"No games yet"}},status=status.HTTP_200_OK)
    numOfGames = len(games_data)
    def checkStreak():
        streak=1
        itr=0
        rev_data = list(reversed(games_data))
       
        for i in range(1, len(rev_data)):
            print(rev_data[i]['winner'])
            if(rev_data[itr]['winner']==rev_data[i]['winner']):
                streak+=1
            else:
                return {
                    "streak":streak,
                    "streakBy":rev_data[0]['winner']
                }
        return {
                    "streak":streak,
                    "streakBy":rev_data[0]['winner']
                }
        
    response_data = {"data":{
        "streakStat":checkStreak(),
        "numOfGames": numOfGames,
        "games": lastTen_data,
       
        }}
    # return Response({"hello":"Hello world"})
    return Response(response_data,status=status.HTTP_200_OK)

@api_view(['GET'])
def getArchive(request):
    games = Games.objects.all()
    games_data=GamesSerializer(games, many=True).data
    if len(games_data)==0:
        return Response({"data":{"message":"No games yet"}},status=status.HTTP_200_OK)
    response_data = {"data":{
        "games": reversed(games_data),
        }}
    # return Response({"hello":"Hello world"})
    return Response(response_data,status=status.HTTP_200_OK)



@api_view(['POST'])
def postMe(request):
    serializer = GamesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # name=request.data.get("name")
    # Item.objects.create(name=name)
    # response_data = {"response":"Item created"}
    # return Response(response_data,status=status.HTTP_200_OK)

@api_view(['GET'])
def getMichaelStats(request):
    games = Games.objects.all()
    games_data = GamesSerializer(games, many=True).data
    lastTen = games.order_by('-id')[:10]
    lastTen_data =GamesSerializer(lastTen, many=True).data
    if len(games_data)==0:
        return Response({"data":{"message":"No games yet"}},status=status.HTTP_200_OK)
    numOfGames = len(games_data)
    numOfWins = len([x for x in games_data if x['winner']=='JM'])
    
   
    def getTeams():
        teams = []
        for x in games_data:
            teams.append(x['details']['michaelTeam'])
        return teams
   
    def mostUsed():
        return max(set(getTeams()), key=getTeams().count)
    def getDiffArray():
        diffArray=[]
        for x in games_data:
            diffArray.append(x['details']['michaelScore']-x['details']['geoScore'])
     
        return diffArray
    def getTotalDiff():
        return sum(getDiffArray())
    def getAveDiff():
        return round(getTotalDiff()/len(getDiffArray()),2)
    def maxPosDiff():
        sorted_diff = sorted(getDiffArray())
        return sorted_diff[len(sorted_diff)-1]
    def maxNegDiff():
        sorted_diff = sorted(getDiffArray())
        return sorted_diff[0]
    def numQuit():
        quit_count=0
        for x in games_data:
            if x['quit'] and x['winner']=='GD':
                quit_count+=1

        return quit_count
 
    # Check best streak
    def bestStreak():
        bestStreak=0
        currStreak=0
        # current dapat napapagitnaan para magkaroon ng streak
        if len(games_data)==1 and games_data[0]['winner']=='JM':
            bestStreak=1
            return bestStreak
        for x in games_data:
            if x['winner']=='JM':
                currStreak+=1
                print(currStreak)
            elif x['winner']!='JM':
                print(currStreak)
                bestStreak=max([bestStreak, currStreak])         
                currStreak =0
        return bestStreak

    response_data = {"data":{
        
        "numOfGames": numOfGames,
        "numOfWins":numOfWins,

        "bestStreak": bestStreak(),
        "mostUsedTeam":mostUsed(),
        "averageDiff": getAveDiff(),
        "maxPositiveDiff":maxPosDiff(),
        "maxNegativeDiff":maxNegDiff(),
        "totalDiff":getTotalDiff(),
        "numQuit":numQuit(),
        "games":lastTen_data,
    }}
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getGeoStats(request):
    games = Games.objects.all()
    games_data = GamesSerializer(games, many=True).data
    lastTen = games.order_by('-id')[:10]
    lastTen_data =GamesSerializer(lastTen, many=True).data
    if len(games_data)==0:
        return Response({"data":{"message":"No games yet"}},status=status.HTTP_200_OK)
    numOfGames = len(games_data)
    numOfWins = len([x for x in games_data if x['winner']=='GD'])
    
   
    def getTeams():
        teams = []
        for x in games_data:
            teams.append(x['details']['geoTeam'])
        return teams
   
    def mostUsed():
        return max(set(getTeams()), key=getTeams().count)
    def getDiffArray():
        diffArray=[]
        for x in games_data:
            diffArray.append(x['details']['geoScore']-x['details']['michaelScore'])
     
        return diffArray
    def getTotalDiff():
        return sum(getDiffArray())
    def getAveDiff():
        return round(getTotalDiff()/len(getDiffArray()),2)
    def maxPosDiff():
        sorted_diff = sorted(getDiffArray())
        return sorted_diff[len(sorted_diff)-1]
    def maxNegDiff():
        sorted_diff = sorted(getDiffArray())
        return sorted_diff[0]
    def numQuit():
        quit_count=0
        for x in games_data:
            if x['quit'] and x['winner']=='JM':
                quit_count+=1

        return quit_count
    def bestStreak():
        bestStreak=0
        currStreak=0
        if len(games_data)==1 and games_data[0]['winner']=='GD':
            bestStreak=1
            return bestStreak
        for x in games_data:
            if x['winner']=='GD':
                currStreak+=1
            else:
                bestStreak=max([bestStreak, currStreak])
                currStreak =0
        return bestStreak

    response_data = {"data":{
        
        "numOfGames": numOfGames,
        "numOfWins":numOfWins,
        "bestStreak": bestStreak(),
        "mostUsedTeam":mostUsed(),
        "averageDiff": getAveDiff(),
        "maxPositiveDiff":maxPosDiff(),
        "maxNegativeDiff":maxNegDiff(),
        "totalDiff":getTotalDiff(),
        "numQuit":numQuit(),
        "games":lastTen_data,
    }}
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['POST'])
def deleteGameByID(request, game_id):
    try:
        game = Games.objects.get(id=game_id)
    except Games.DoesNotExist:
        return Response({"data":{"message":"Game not found"}}, status=status.HTTP_400_BAD_REQUEST) 
    game.delete()
    return Response({"data":{"message":f"Deleted game with ID:{game_id}"}},status=status.HTTP_200_OK)
# @api_view(['PATCH'])
# def patchMe(request,id):
#         name = request.data.get('name')
#         item = Item.objects.filter(id=id).first()
#         if item is None:
#             response_data = {"response":"Item doesnot exists"}
#             return Response(response_data,status=status.HTTP_404_NOT_FOUND)
#         item.name = name
#         item.save()
#         response_data = {"response":"item Updated"}
#         return Response(response_data,status=status.HTTP_200_OK)

# @api_view(['DELETE'])
# def deleteMe(request):
#     id = request.data.get('id')
#     print(id)
#     item = Item.objects.filter(id=id).first()
#     if item is None:
#         response_data={"response":"Item does not exist"}
#         return Response(response_data, status=status.HTTP_404_NOT_FOUND)
#     item.delete()
#     response_data = {"response": "Successfully deleted"}
#     return Response(response_data, status=status.HTTP_200_OK)
    

# class DumpItAPI(APIView): 
    # def get(self,request):
    #     items = Item.objects.all()
    #     items_data=ItemSerializer(items, many=True).data
    #     response_data = {"datas":items_data}
    #     return Response(response_data,status=status.HTTP_200_OK)
    # def post(self,request):
    #     name=request.data.get("name")
    #     Item.objects.create(name=name)
    #     response_data = {"response":"Item created"}
    #     return Response(response_data,status=status.HTTP_200_OK)
    # def patch(self,request,id):
    #     name = request.data.get('name')
    #     item = Item.objects.filter(id=id).first()
    #     if item is None:
    #         response_data = {"response":"Item doesnot exists"}
    #         return Response(response_data,status=status.HTTP_404_NOT_FOUND)
    #     item.name = name
    #     item.save()
    #     response_data = {"response":"item Updated"}
    #     return Response(response_data,status=status.HTTP_200_OK)
    
    # def delete(seld, request):
    #     id = request.data.get('id')
    #     item = Item.objects.filter(id=id).first()
    #     if item is None:
    #         response_data={"response":"Item does not exist"}
    #         return Response(response_data, status=status.HTTP_404_NOT_FOUND)
    #     item.delete()
    #     response_data = {"response": "Successfully deleted"}
    #     return Response(response_data, status=status.HTTP_200_OK)
    