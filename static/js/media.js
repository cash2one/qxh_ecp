/**
 * Created with PyCharm.
 * User: seandong
 * Date: 13-2-22
 * Time: 下午4:09
 * To change this template use File | Settings | File Templates.
 */

M1="请选择";
M2="请选择";
M3="请选择";
ShowT=1;		//提示文字 0:不显示 1:显示
//MMMD="卫视$河南卫视|四川卫视|山东卫视|西藏卫视|山西卫视|黑龙江卫视|未知频道#四川$电视广告,川2,川3,川4,川5,川3晚间,川4晚间,川5晚间,成都公交（华视10秒）,四川星空长虹20秒,网络,不说,多台|分众楼宇广告|公交车广告,车体广告|报纸,成都商报|宣传单|他人推荐|网络,健客网,康爱多,其他#四川芪枣$电视广告,成都1-新闻晚间,成都3-都市,成都4-影视,成都5-公共 晚间,网络,不说,多台,成都商报|分众,分众楼宇广告|公交车广告,公交移动电视,车体广告|华西都市报|晚间一套|生活周刊报|宣传单|楼宇电梯|药店宣传|餐饮宣传|他人推荐#山东$电视广告,齐鲁,不说,多台|分众楼宇广告|公交车广告,车体广告,移动电视|报纸|宣传单|他人推荐|网络,健客网,康爱多,其他#广东$电视广告,南方经济,南方综艺,南方影视,广东新闻,广东公共,广州影视,广东珠江,广东移动频道,东莞公共,多台|网络,健客网,康爱多,其他|分众楼宇广告|公交车广告,车体广告,广东公交|报纸|宣传单|不说|他人推荐#陕西$电视广告|分众楼宇广告|公交车广告,车体广告,移动电视|报纸|宣传单|他人推荐|网络,健客网,康爱多,其他#黑龙江$电视广告,黑龙江影视,多台|分众楼宇广告|公交车广告|报纸|宣传单|他人推荐|网络,康爱多,健客网,其他#浙江$电视广告,影视频道-晚间,少儿频道,民生频道,温州公共民生,网络,不说,多台|分众楼宇广告|公交车广告,车体广告,移动电视|报纸|宣传单|他人推荐|网络,健客网,康爱多,其他";
//MMMD="卫视$河南卫视|四川卫视|山东卫视|未知频道|黑龙江卫视|山西卫视|西藏卫视|内蒙卫视|陕西卫视|新疆卫视#四川$电视广告,川2,川3,川4,川5,川3晚间,川4晚间,川5晚间,成都公交（华视10秒）,四川星空长虹20秒,网络,不说,多台,川9  公共|分众楼宇广告|公交车广告,车体广告|报纸,成都商报|宣传单|他人推荐|网络,健客网,康爱多,其他#四川芪枣$电视广告,四川4台,成都1-新闻晚间,成都3-都市,成都4-影视,成都5-公共 晚间,网络,不说,多台,陕西5套,陕西7套,成都2-经济频道|分众,分众楼宇广告|公交车广告,公交移动电视,车体广告|华西都市报|晚间一套|生活周刊报|宣传单|楼宇电梯|药店宣传|餐饮宣传|他人推荐|成都商报#山东$电视广告,齐鲁,不说,多台|分众楼宇广告|公交车广告,车体广告,移动电视|报纸|宣传单|他人推荐|网络,健客网,康爱多,其他#广东$电视广告,南方经济,南方综艺,南方影视,广东新闻,广东公共,广州影视,广东珠江,广东移动频道,东莞公共,多台,广州公交移动电视|网络,健客网,康爱多,其他|分众楼宇广告|公交车广告,车体广告,广东公交|报纸|宣传单|不说|他人推荐#陕西$电视广告,陕西二套,陕西五套,陕西三套晚间,多台|分众楼宇广告|公交车广告,车体广告,移动电视|报纸|宣传单|他人推荐|网络,健客网,康爱多,其他#黑龙江$电视广告,黑龙江影视,多台|分众楼宇广告|公交车广告|报纸|宣传单|他人推荐|网络,康爱多,健客网,其他#浙江$电视广告,教科频道,钱江频道,影视频道-白天,影视频道-晚间,少儿频道,民生频道,温州公共民生,网络,不说,多台|分众楼宇广告|公交车广告,车体广告,移动电视|报纸|宣传单|他人推荐|网络,健客网,康爱多,其他";
//MMMD="卫视$河南卫视|未知频道|陕西卫视|#四川$电视广告,多台,四川5-晚间,四川4-晚间,四川3-晚间,四川9,四川5,四川4,四川2|分众楼宇|成都公交|报纸|宣传单|健客网|未知|康爱多|他人推荐|其它|#四川芪枣$电视广告,成都4-晚间,多台,四川5-晚间,四川4,成都3-晚间,四川5,四川4-晚间,成都1-晚间,成都5,成都3,四川9频道|分众楼宇|公交|宣传单|报纸|药店宣传|餐饮宣传|他人推荐|其它|未知|小报|#山东$电视广告,齐鲁,不说,多台|分众楼宇广告|公交车广告,车体广告,移动电视|报纸|宣传单|他人推荐|网络,健客网,康爱多,其他|#广东$电视广告,南方经济,南方综艺,南方影视,广东新闻,广东公共,广州影视,广东珠江,广东移动频道,东莞公共,多台,广州公交移动电视,广东省网翡翠,深圳都市频道|网络,健客网,康爱多,其他|分众楼宇广告|公交车广告,车体广告,广东公交|报纸|宣传单|不说|他人推荐|深圳公交|#陕西$电视广告,陕西二套,陕西五套,多台,陕西7套|分众楼宇广告|公交车广告,车体广告,移动电视|报纸|宣传单|他人推荐|网络,健客网,康爱多,其他|#黑龙江$电视广告,黑龙江影视,多台|分众楼宇广告|公交车广告|报纸|宣传单|他人推荐|网络,康爱多,健客网,其他|#黑龙江芪枣$黑龙江影视|黑龙江新闻|未知|他人推荐|药房宣传单|#陕西芪枣$他人推荐|陕西七套|陕西五套|未知|药房宣传单|陕西1套|小报|#湖北芪枣$湖北综合|湖北经视|湖北体育|湖北教育|未知|他人推荐|药房宣传单|湖北电视台|#山东芪枣$山东齐鲁|宣传单|他人推荐|未知|小报|#陕西卫视$#频道未知$"//john20131115
//MMMD="卫视$河南卫视|未知频道|陕西卫视|#四川$电视广告,多台,四川5-晚间,四川4-晚间,四川3-晚间,四川9,四川5,四川4,四川2|分众楼宇|成都公交|报纸|宣传单|健客网|未知|康爱多|他人推荐|其它|#四川芪枣$电视广告,成都4-晚间,多台,四川5-晚间,四川4,成都3-晚间,四川5,四川4-晚间,成都1-晚间,成都5,成都3,SC-5 摩能,星空公交,四川9频道|分众楼宇|公交|宣传单|报纸|药店宣传|餐饮宣传|他人推荐|其它|未知|小报|#山东$电视广告,山东公共频道,齐鲁,不说,多台|分众楼宇广告|公交车广告,车体广告,移动电视|报纸|宣传单|他人推荐|网络,健客网,康爱多,其他|#广东$电视广告,南方经济,南方综艺,南方影视,广东新闻,广东公共,广州影视,广东珠江,广东移动频道,东莞公共,多台,广州公交移动电视,广东省网翡翠,深圳都市频道|网络,健客网,康爱多,其他|分众楼宇广告|公交车广告,车体广告,广东公交|报纸|宣传单|不说|他人推荐|深圳公交|#陕西$电视广告,陕西二套,陕西五套,多台,陕西7套|分众楼宇广告|公交车广告,车体广告,移动电视|报纸|宣传单|他人推荐|网络,健客网,康爱多,其他|#黑龙江$电视广告,黑龙江影视,多台|分众楼宇广告|公交车广告|报纸|宣传单|他人推荐|网络,康爱多,健客网,其他|#黑龙江芪枣$黑龙江影视|黑龙江新闻|未知|他人推荐|药房宣传单|#陕西芪枣$他人推荐|陕西4套|陕西七套|陕西五套|未知|药房宣传单|陕西1套|小报|#湖北芪枣$湖北综合|湖北经视|湖北体育|湖北教育|未知|他人推荐|药房宣传单|湖北电视台|#山东芪枣$山东齐鲁|宣传单|他人推荐|未知|小报|#陕西卫视$#频道未知$"//john20140103
//MMMD="卫视$河南卫视|未知频道|陕西卫视|#四川$电视广告,多台,四川5,SC-4 云视,华视公交 环纵,SC-5 云视,SC-5摩能,SC-科教 雅润|分众楼宇|成都公交|报纸|宣传单|健客网|未知|康爱多|他人推荐|其它|#心力健快乐老人报（山东）$#心力健全国$快乐老人报|老年日报|中国老年报|文萃报|文摘周刊|家庭医生|#四川芪枣$电视广告,多台,四川5|分众楼宇|公交|宣传单|报纸|药店宣传|餐饮宣传|他人推荐|其它|未知|小报|#心力健扬子晚报$#山东$电视广告,山东公共频道,齐鲁,不说,多台|分众楼宇广告|公交车广告,车体广告,移动电视|报纸|宣传单|他人推荐|网络,健客网,康爱多,其他|#广东$电视广告,南方经济,南方综艺,南方影视,广东新闻,广东公共,广州影视,广东珠江,广东移动频道,东莞公共,多台,广州公交移动电视,广东省网翡翠,深圳都市频道|网络,健客网,康爱多,其他|分众楼宇广告|公交车广告,车体广告,广东公交|报纸|宣传单|不说|他人推荐|深圳公交|#陕西$电视广告,陕西二套,陕西五套,多台,陕西7套|分众楼宇广告|公交车广告,车体广告,移动电视|报纸|宣传单|他人推荐|网络,健客网,康爱多,其他|#黑龙江$电视广告,黑龙江影视,多台|分众楼宇广告|公交车广告|报纸|宣传单|他人推荐|网络,康爱多,健客网,其他|#黑龙江芪枣$黑龙江影视|黑龙江新闻|未知|他人推荐|药房宣传单|#心力健新安晚报$#心力健燕赵晚报$#心力健青岛早报$#心力健长沙晚报$#心力健扬州晚报$#陕西芪枣$他人推荐|陕西4套|陕西七套|陕西五套|未知|药房宣传单|陕西2套|陕西1套|小报|#湖北芪枣$湖北综合|湖北经视|湖北体育|湖北教育|未知|他人推荐|药房宣传单|#心力健福建老年报$#心力健厦门晚报$#心力健楚天都市报$#心力健北京晨报$#心力健老年生活报$#山东芪枣$山东齐鲁|宣传单|他人推荐|未知|小报|#陕西卫视$#频道未知$#心力健江南保健报$"//john20140218
MMMD="卫视$未知频道|陕西卫视|#四川$电视广告,多台,四川5,SC-4 云视,四川3套,华视公交 环纵,SC-5 云视,SC-5摩能,SC-科教 雅润|分众楼宇|成都公交|报纸|宣传单|健客网|未知|康爱多|他人推荐|其它|#心力健快乐老人报（山东）$#心力健全国$快乐老人报|老年日报|中国老年报|文萃报|文摘周刊|老年文摘5月8日|老年生活报5月7日|快乐老人报（产品版）|家庭医生|#四川芪枣$电视广告,川8科教频道,多台,四川5|分众楼宇|公交|宣传单|报纸|药店宣传|餐饮宣传|他人推荐|其它|未知|小报|#心力健扬子晚报$#山东$电视广告,山东公共频道,齐鲁,不说,多台,青岛影视（晚间）,山东生活频道|分众楼宇广告|公交车广告,车体广告,移动电视|报纸|宣传单|他人推荐|网络,健客网,康爱多,其他|#广东$电视广告,南方经济,南方综艺,南方影视,广东新闻,广东公共,广州影视,广东珠江,广东移动频道,东莞公共,多台,少儿频道,南方5套,广州公交移动电视,广东省网翡翠,深圳都市频道|网络,健客网,康爱多,其他|分众楼宇广告|公交车广告,车体广告,广东公交|报纸|宣传单|不说|他人推荐|深圳公交|#陕西$电视广告,陕西二套,陕西五套,多台,陕西4套,陕西7套|分众楼宇广告|公交车广告,车体广告,移动电视|报纸|宣传单|他人推荐|网络,健客网,康爱多,其他|#黑龙江$电视广告,黑龙江影视,多台,黑龙江文艺频道,黑龙江新闻频道|分众楼宇广告|公交车广告|报纸|宣传单|他人推荐|网络,康爱多,健客网,其他|#黑龙江芪枣$黑龙江影视|黑龙江新闻|未知|他人推荐|药房宣传单|#心力健新安晚报$#心力健燕赵晚报$#心力健青岛早报$#心力健长沙晚报$#心力健扬州晚报$#陕西芪枣$他人推荐|陕西4套|陕西4套|陕西七套|陕西五套|未知|药房宣传单|陕西2套|陕西1套|小报|#心力健福建老年报$#心力健厦门晚报$#心力健楚天都市报$#心力健北京晨报$#心力健老年生活报$#山东芪枣$山东齐鲁|宣传单|他人推荐|未知|小报|#陕西卫视$#频道未知$#心力健江南保健报$"//john20140403
if(ShowT)MMMD=M1+"$"+M2+","+M3+"#"+MMMD;MMMArea=[];MMMP=[];MMMC=[];MMMA=[];MMMN=MMMD.split("#");for(i=0;i<MMMN.length;i++){MMMA[i]=[];TArea=MMMN[i].split("$")[1].split("|");for(j=0;j<TArea.length;j++){MMMA[i][j]=TArea[j].split(",");if(MMMA[i][j].length==1)MMMA[i][j][1]=M3;TArea[j]=TArea[j].split(",")[0]}MMMArea[i]=MMMN[i].split("$")[0]+","+TArea.join(",");MMMP[i]=MMMArea[i].split(",")[0];MMMC[i]=MMMArea[i].split(',')}function MMMS(){this.SelP=document.getElementsByName(arguments[0])[0];this.SelC=document.getElementsByName(arguments[1])[0];this.SelA=document.getElementsByName(arguments[2])[0];this.DefP=this.SelA?arguments[3]:arguments[2];this.DefC=this.SelA?arguments[4]:arguments[3];this.DefA=this.SelA?arguments[5]:arguments[4];this.SelP.MMM=this;this.SelC.MMM=this;this.SelP.onchange=function(){MMMS.SetC(this.MMM)};if(this.SelA)this.SelC.onchange=function(){MMMS.SetA(this.MMM)};MMMS.SetP(this)};MMMS.SetP=function(MMM){for(i=0;i<MMMP.length;i++){MMMPT=MMMPV=MMMP[i];if(MMMPT==M1)MMMPV="";MMM.SelP.options.add(new Option(MMMPT,MMMPV));if(MMM.DefP==MMMPV)MMM.SelP[i].selected=true}MMMS.SetC(MMM)};MMMS.SetC=function(MMM){PI=MMM.SelP.selectedIndex;MMM.SelC.length=0;for(i=1;i<MMMC[PI].length;i++){MMMCT=MMMCV=MMMC[PI][i];if(MMMCT==M2)MMMCV="";MMM.SelC.options.add(new Option(MMMCT,MMMCV));if(MMM.DefC==MMMCV)MMM.SelC[i-1].selected=true}if(MMM.SelA)MMMS.SetA(MMM)};MMMS.SetA=function(MMM){PI=MMM.SelP.selectedIndex;CI=MMM.SelC.selectedIndex;MMM.SelA.length=0;for(i=1;i<MMMA[PI][CI].length;i++){MMMAT=MMMAV=MMMA[PI][CI][i];if(MMMAT==M3)MMMAV="";MMM.SelA.options.add(new Option(MMMAT,MMMAV));if(MMM.DefA==MMMAV)MMM.SelA[i-1].selected=true}}
