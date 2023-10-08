Search.setIndex({docnames:["api/elmax_api","api/elmax_api.model","api/elmax_api.push","api/modules","basic","examples/quickstart","index"],envversion:{"sphinx.domains.c":2,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":4,"sphinx.domains.index":1,"sphinx.domains.javascript":2,"sphinx.domains.math":2,"sphinx.domains.python":3,"sphinx.domains.rst":2,"sphinx.domains.std":2,sphinx:56},filenames:["api/elmax_api.rst","api/elmax_api.model.rst","api/elmax_api.push.rst","api/modules.rst","basic.rst","examples/quickstart.rst","index.rst"],objects:{"":{elmax_api:[0,0,0,"-"]},"elmax_api.exceptions":{ElmaxApiError:[0,1,1,""],ElmaxBadLoginError:[0,1,1,""],ElmaxBadPinError:[0,1,1,""],ElmaxError:[0,1,1,""],ElmaxNetworkError:[0,1,1,""],ElmaxPanelBusyError:[0,1,1,""]},"elmax_api.exceptions.ElmaxApiError":{status_code:[0,2,1,""]},"elmax_api.model":{actuator:[1,0,0,"-"],alarm_status:[1,0,0,"-"],area:[1,0,0,"-"],command:[1,0,0,"-"],cover:[1,0,0,"-"],cover_status:[1,0,0,"-"],endpoint:[1,0,0,"-"],goup:[1,0,0,"-"],panel:[1,0,0,"-"],scene:[1,0,0,"-"],zone:[1,0,0,"-"]},"elmax_api.model.actuator":{Actuator:[1,3,1,""]},"elmax_api.model.actuator.Actuator":{from_api_response:[1,4,1,""],opened:[1,2,1,""]},"elmax_api.model.alarm_status":{AlarmArmStatus:[1,3,1,""],AlarmStatus:[1,3,1,""]},"elmax_api.model.alarm_status.AlarmArmStatus":{ARMED_P1:[1,5,1,""],ARMED_P1_P2:[1,5,1,""],ARMED_P2:[1,5,1,""],ARMED_TOTALLY:[1,5,1,""],NOT_ARMED:[1,5,1,""]},"elmax_api.model.alarm_status.AlarmStatus":{ARMED_STANDBY:[1,5,1,""],NOT_ARMED_NOT_ARMABLE:[1,5,1,""],NOT_ARMED_NOT_TRIGGERED:[1,5,1,""],TRIGGERED:[1,5,1,""]},"elmax_api.model.area":{Area:[1,3,1,""]},"elmax_api.model.area.Area":{armed_status:[1,2,1,""],available_arm_statuses:[1,2,1,""],available_statuses:[1,2,1,""],from_api_response:[1,4,1,""],status:[1,2,1,""]},"elmax_api.model.command":{AreaCommand:[1,3,1,""],Command:[1,3,1,""],CoverCommand:[1,3,1,""],SceneCommand:[1,3,1,""],SwitchCommand:[1,3,1,""]},"elmax_api.model.command.AreaCommand":{ARM_P1:[1,5,1,""],ARM_P1_P2:[1,5,1,""],ARM_P2:[1,5,1,""],ARM_TOTALLY:[1,5,1,""],DISARM:[1,5,1,""]},"elmax_api.model.command.CoverCommand":{DOWN:[1,5,1,""],UP:[1,5,1,""]},"elmax_api.model.command.SceneCommand":{TRIGGER_SCENE:[1,5,1,""]},"elmax_api.model.command.SwitchCommand":{TURN_OFF:[1,5,1,""],TURN_ON:[1,5,1,""]},"elmax_api.model.cover":{Cover:[1,3,1,""]},"elmax_api.model.cover.Cover":{from_api_response:[1,4,1,""],position:[1,2,1,""],status:[1,2,1,""]},"elmax_api.model.cover_status":{CoverStatus:[1,3,1,""]},"elmax_api.model.cover_status.CoverStatus":{DOWN:[1,5,1,""],IDLE:[1,5,1,""],UP:[1,5,1,""]},"elmax_api.model.endpoint":{DeviceEndpoint:[1,3,1,""]},"elmax_api.model.endpoint.DeviceEndpoint":{endpoint_id:[1,2,1,""],from_api_response:[1,4,1,""],index:[1,2,1,""],name:[1,2,1,""],visible:[1,2,1,""]},"elmax_api.model.goup":{Group:[1,3,1,""]},"elmax_api.model.goup.Group":{from_api_response:[1,4,1,""]},"elmax_api.model.panel":{EndpointStatus:[1,3,1,""],PanelEntry:[1,3,1,""],PanelStatus:[1,3,1,""]},"elmax_api.model.panel.EndpointStatus":{accessory_release:[1,2,1,""],accessory_type:[1,2,1,""],actuators:[1,2,1,""],all_endpoints:[1,2,1,""],areas:[1,2,1,""],cover_feature:[1,2,1,""],covers:[1,2,1,""],from_api_response:[1,4,1,""],groups:[1,2,1,""],push_feature:[1,2,1,""],release:[1,2,1,""],scene_feature:[1,2,1,""],scenes:[1,2,1,""],zones:[1,2,1,""]},"elmax_api.model.panel.PanelEntry":{from_api_response:[1,4,1,""],get_name_by_user:[1,4,1,""],hash:[1,2,1,""],online:[1,2,1,""]},"elmax_api.model.panel.PanelStatus":{accessory_release:[1,2,1,""],accessory_type:[1,2,1,""],actuators:[1,2,1,""],all_endpoints:[1,2,1,""],areas:[1,2,1,""],cover_feature:[1,2,1,""],covers:[1,2,1,""],from_api_response:[1,4,1,""],groups:[1,2,1,""],panel_id:[1,2,1,""],push_feature:[1,2,1,""],release:[1,2,1,""],scene_feature:[1,2,1,""],scenes:[1,2,1,""],user_email:[1,2,1,""],zones:[1,2,1,""]},"elmax_api.model.scene":{Scene:[1,3,1,""]},"elmax_api.model.scene.Scene":{from_api_response:[1,4,1,""]},"elmax_api.model.zone":{Zone:[1,3,1,""]},"elmax_api.model.zone.Zone":{excluded:[1,2,1,""],from_api_response:[1,4,1,""],opened:[1,2,1,""]},elmax_api:{constants:[0,0,0,"-"],exceptions:[0,0,0,"-"],model:[1,0,0,"-"],push:[2,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","exception","Python exception"],"2":["py","property","Python property"],"3":["py","class","Python class"],"4":["py","method","Python method"],"5":["py","attribute","Python attribute"]},objtypes:{"0":"py:module","1":"py:exception","2":"py:property","3":"py:class","4":"py:method","5":"py:attribute"},terms:{"0":[1,5],"000000":5,"1":[1,5],"168":5,"192":5,"2":1,"249":5,"3":1,"4":1,"5":5,"60":5,"7":5,"case":4,"class":[1,4],"enum":1,"function":4,"import":5,"int":[0,1],"new":1,"return":[0,1,4],"static":1,"switch":[4,5],"try":4,A:4,As:4,For:4,If:4,In:[4,5],Is:4,It:4,ON:5,The:[5,6],To:4,__main__:5,__name__:5,_panel_upd:5,about:4,accept:4,accessory_releas:1,accessory_typ:1,accomplish:4,action:4,activ:[4,6],actuat:[0,3,5,6],again:4,against:4,alarm:[1,4],alarm_statu:[0,3],alarmarmstatu:1,alarmstatu:1,all_endpoint:1,although:4,an:[0,1,4,5],ani:4,api:[0,1,4,5],append:5,ar:4,area:[0,3,4],areacommand:1,arg:1,argument:4,arm:[1,4],arm_p1:1,arm_p1_p2:1,arm_p2:1,arm_tot:1,armed_p1:1,armed_p1_p2:1,armed_p2:1,armed_standbi:1,armed_statu:1,armed_tot:1,associ:4,async:5,asynchron:4,asyncio:[4,5],attempt:[0,4],authent:6,autom:4,autonom:4,avail:[1,4],available_arm_status:1,available_status:1,awai:4,await:[4,5],back:5,bad:[0,4],base:[0,1],basic:6,being:4,bit:5,block:4,bool:1,busi:0,cach:4,call:4,callback:5,can:[4,5],cannot:0,cert_non:5,check:4,check_hostnam:5,client:[0,5,6],close:4,cloud:[0,4,5],code:[0,4,5],command:[0,3,5,6],common:4,comput:4,concept:6,configur:1,connect:4,constant:3,construct:4,constructor:4,contain:4,content:3,context:5,control:[1,4,6],control_panel_id:[4,5],core:4,coroutin:5,cover:[0,3,4],cover_featur:1,cover_statu:[0,3],covercommand:1,coverstatu:1,creat:[1,4],create_default_context:5,credenti:4,current:[1,4,5],data:4,deal:4,def:5,describ:4,design:4,develoepr:4,develop:[4,6],devic:[4,6],deviceendpoint:1,devicehash:1,dict:1,dirti:4,disabl:4,disarm:[1,4],discoveri:0,done:5,door:4,down:[1,4],due:0,easili:5,elmax:[0,5],elmax_api:[4,5,6],elmax_password:5,elmax_usernam:5,elmaxapierror:0,elmaxbadloginerror:[0,4],elmaxbadpinerror:0,elmaxerror:0,elmaxloc:5,elmaxnetworkerror:0,elmaxpanelbusyerror:0,els:5,encount:0,endpoint:[0,3,4],endpoint_id:[1,4,5],endpointstatu:1,entiti:4,entri:4,enumer:1,error:0,etc:4,event:5,everytim:4,exampl:5,except:[3,4],exclud:1,execut:0,execute_command:[4,5],exit:5,expir:4,explicitli:4,f:[4,5],facil:4,fail:0,fals:5,familiar:4,fetch:[5,6],first:[4,5],follow:[4,5],former:4,found:[4,5],from:[1,4,5],from_api_respons:1,full:4,gener:0,get:[4,5],get_authenticated_usernam:[4,5],get_event_loop:5,get_name_by_us:1,get_panel_statu:[4,5],getenv:5,given:4,global:5,goup:[0,3],group:[1,4],ha:[4,5],hand:4,handl:4,handler:5,hash:[1,4,5],have:4,he:4,helper:5,home:4,hous:4,how:5,hte:4,http:[3,5,6],i:[4,5],id:4,idl:1,illustr:5,implement:4,index:[1,6],inform:4,instal:6,instanc:4,instanti:[4,5],invalid:4,invok:4,issu:4,its:4,json:1,jtw:4,just:5,jwt:4,kitchen:4,kwarg:1,later:4,latter:4,leav:4,len:[4,5],librari:[4,5,6],like:4,list:[1,5,6],list_control_panel:[4,5],listen:6,live:4,logic:4,login:[0,5,6],look:4,m:4,magnet:4,mai:4,main:[4,5],manag:5,mandatori:4,mean:4,memori:4,method:4,might:4,minimum:4,mode:4,model:[0,3,5,6],modul:[3,4,6],more:4,much:4,multipl:4,must:4,my_password:[4,5],my_usernam:[4,5],name:[1,4,5],name_by_us:1,necessari:5,need:4,network:0,not_arm:1,not_armed_not_arm:1,not_armed_not_trigg:1,noth:4,notif:6,object:[1,4,5],obtain:4,occur:[0,5],off:[1,4,5],offlin:[4,5],old_statu:5,onc:4,one:4,onli:[4,5],onlin:[1,4,5],online_panel:5,open:[1,4,5],oper:4,option:4,order:[4,5],origin:5,os:5,own:4,p:[4,5],packag:[3,6],packet:5,page:6,panel:[0,3,5,6],panel_api_url:5,panel_cod:5,panel_endpoint:5,panel_id:1,panel_statu:[4,5],panelentri:[1,4],panelstatu:[1,4,5],paramet:4,password:[4,5],pattern:4,per:4,perimet:4,pin:[0,4],pip3:5,posit:1,possibl:4,print:[4,5],program:4,project:6,properti:[0,1,4],provid:4,push:6,push_endpoint:5,push_featur:1,pushnotificationhandl:5,pypi:5,python:[4,6],quick:[4,6],rais:4,rang:5,re:4,read:4,reason:4,refer:4,refus:4,regist:5,register_push_notification_handl:5,releas:1,reli:4,remot:4,renew:4,repres:4,represent:1,respons:1,response_entri:1,result:4,retriev:4,reus:4,revert:5,right:4,run:5,scene:[0,3,4],scene_featur:1,scenecommand:1,search:6,section:4,send:6,sensor:4,servic:0,show:5,simpli:4,sleep:5,slept:5,snippet:5,so:5,some:[4,5],sorri:5,specic:4,specif:4,ssl:5,ssl_context:5,start:[4,6],state:4,statu:[0,1,5,6],status:1,status_cod:0,statut:1,stop:[1,5],store:4,str:1,submodul:3,subpackag:3,succe:4,support:[1,4],switchcommand:[1,5],t:4,take:4,talk:4,than:4,thi:[4,5,6],thread:4,thrown:4,thu:4,toggl:5,token:4,trigger:[1,4],trigger_scen:1,turn:4,turn_off:[1,5],turn_on:[1,5],two:4,type_here_your_password:5,type_here_your_usernam:5,under:6,unexpect:0,unregister_push_notification_handl:5,up:[1,4],us:[0,4,5],user:[4,5],user_email:1,usernam:[1,4,5],usual:4,v2:5,valid:4,valu:1,verify_mod:5,verifymod:5,version:4,via:[4,5],visibl:1,volumetr:4,wa:5,wait:5,want:4,we:4,web:4,when:0,whenev:4,which:4,window:4,within:4,won:4,work:[4,5],wss:5,you:4,your:[4,5],z:5,zone:[0,3,4,5]},titles:["elmax_api package","elmax_api.model package","elmax_api.push package","elmax_api","Basic Concepts","Installation","Welcome to Elmax API\u2019s documentation!"],titleterms:{The:4,actuat:[1,4],alarm_statu:1,api:6,area:1,authent:4,basic:4,client:4,command:[1,4],concept:4,constant:0,content:[0,1,2],cover:1,cover_statu:1,document:6,elmax:[4,6],elmax_api:[0,1,2,3],endpoint:1,except:0,fetch:4,goup:1,http:[0,4],indic:6,instal:5,list:4,listen:5,login:4,model:[1,4],modul:[0,1,2],notif:5,packag:[0,1,2],panel:[1,4],push:[2,5],quick:5,refer:6,s:6,scene:1,send:4,start:5,statu:4,submodul:[0,1,2],subpackag:0,tabl:6,welcom:6,zone:1}})