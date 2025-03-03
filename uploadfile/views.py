from django.shortcuts import render
from django.shortcuts import redirect
 
# app主页
def index_in(request):
    # print("index")
    global time_monitor
    time_monitor=3
    return render(request, "createcourse/index.html")

# 加载文件上传表单
def upload(request):
    # print("upload")
    return render(request, "uploadfile/upload.html",{"timeget":time_monitor})

def showresult(request):
    return render(request, "uploadfile/result.html")

# 执行文件上传处理
def doupload(request):
    global recordflag
    print("output")
    # # 接收
    # if not recordflag:
    #     myfile = request.FILES.get("doc", None)
    #     if not myfile:
    #         return HttpResponse("file not find")

    #     filename = str(time.time())+"."+myfile.name.split('.').pop()
    #     destination = open("./static/docs/"+filename, "wb+")
    # # 将文件流分块读取文件内容并写入目标文件
    #     for chunk in myfile.chunks():
    #         destination.write(chunk)
    #     destination.close

    # else:
    #     recordflag = False
    #     filename = "input.wav"

    # host = "http://10.108.17.152:"
    # endpoint = "5000"
    # url = ''.join([host, endpoint])

    # # r = requests.post(url, json=json.dumps(address))
    # # response = r.json()
    # # print(response)

    # # print("________________________________________________________________________")
    # # print(filename)
    # with open("./static/docs/"+filename, 'rb') as f:
    #     resp = requests.post(url, files={'voice_file': f})
    # response = resp.json()
    # # print(response)
    # # print("________________________________________________________________________")

    # # 将json存入 session 中传递
    # jdata = {"data":"data", "img_src":"img_src"}
    # jdata = response
    # # jdata = { "mention_data": [{"offset": "19","mention": "nasa","kb_id": "Q23548","wikidata_url": "https://www.wikidata.org/wiki/Q23548", "description": "independent agency of the United States Federal Government"},{"offset": "42", "mention": "new york city","kb_id": "Q60","wikidata_url": "https://www.wikidata.org/wiki/Q60", "description": "largest city in the United States"}], "text": "BrittaRiley _ 2011X 1 BrittaRiley _ 2011X 261.89 271.48 < NA > what we ' re doing is what nasa or a large corporation would call r & d < unk > or research and development but what we call it is r new york city"}
    
    # request.session['jdata'] = json.dumps(jdata)
    return redirect('/output')




def settime(request):
    global time_monitor
    ssq=request.POST.get('mytime')
    if(ssq==""):
        print(ssq+"123")
        ssq=3
    print(ssq+"123")
    time_monitor=int(ssq)       
    print(time_monitor) 
    # time_monitor=mytime
    return render(request,'createcourse/upload.html',{"timeget":time_monitor})



        

        

